from data.data_retrieval import DataDownload
from bs4 import BeautifulSoup
import re
import random  
from pinecone import Pinecone
import os

class Chunker():
    def __init__(self, method):
        self.data = DataDownload()
        self.methods = ["fixed_size", "overlap"]
        self.file_paths = self.data.get_file_paths(court = "ewfc")
        self.chunks = []


    def clean_text(self, text: str) -> str:
        text = re.sub(r'\n{2,}', '\n', text)
        text = re.sub(r' +', ' ', text)
        text = text.strip()
        #remove any line that begins with #judgment
        text = re.sub(r'(?m)^#judgment.*\n?', '', text)
        return text
    
    def get_metadata(self, soup, path):
        frbr_expression = soup.find('FRBRExpression')
        metadata = {}
        metadata["path"] = path  # Store the file path in metadata
        if frbr_expression:
            # Extract values from child tags
            frbr_uri = frbr_expression.find('FRBRuri')
            if frbr_uri and 'value' in frbr_uri.attrs:
                metadata['uri'] = frbr_uri['value']
            
            frbr_date = frbr_expression.find('FRBRdate')
            if frbr_date and 'date' in frbr_date.attrs:
                metadata['judgment_date'] = frbr_date['date']
                if 'name' in frbr_date.attrs:
                    metadata['type'] = frbr_date['name']
            
            frbr_author = frbr_expression.find('FRBRauthor')
            if frbr_author and 'href' in frbr_author.attrs:
                metadata['author'] = frbr_author['href']
            
        return metadata

    def chunking(self, text):
        """Chunk text by xml file structure with smart splitting for large sections"""
        if len(text) < 1000:
            return [text]
        
        # First split by the separator pattern
        chunks = []
        parts = text.split('- - - - - - -')
        for part in parts:
            if part.strip():  # Skip empty/whitespace-only parts
                chunks.append(part.strip())
        
        # Process chunks that are still too large
        final_chunks = []
        for chunk in chunks:
            if len(chunk) <= 1000:
                final_chunks.append(chunk)
                continue
                
            # Try to split by structural markers (ordered by priority)
            split_points = []
            
            # 1. Look for numbered points (1., 2., etc.) with whitespace
            numbered_points = re.finditer(r'\n\s*\d+\.\s', chunk)
            for match in numbered_points:
                split_points.append(match.start())
            
            # 2. Look for section headers (Introduction, Judgment, Conclusion)
            section_headers = re.finditer(r'\n\s*(Introduction|Judgment|Conclusion)\s*\n', chunk, re.IGNORECASE)
            for match in section_headers:
                split_points.append(match.start())
            
            # Sort split points and add end of text
            split_points = sorted(list(set(split_points)))  # Remove duplicates and sort
            split_points.append(len(chunk))  # Add end of text as final split point
            
            # Create sub-chunks using the split points
            prev_split = 0
            for split in split_points:
                if split - prev_split > 1000 or split == split_points[-1]:
                    sub_chunk = chunk[prev_split:split].strip()
                    if sub_chunk:  # Only add non-empty chunks
                        # If still too big, split by nearest newline to 1000 chars
                        if len(sub_chunk) > 1000:
                            optimal_split = prev_split + 1000
                            # Find nearest newline before optimal split
                            newline_pos = chunk.rfind('\n', prev_split, optimal_split)
                            if newline_pos != -1:
                                final_chunks.append(chunk[prev_split:newline_pos].strip())
                                prev_split = newline_pos + 1
                                continue
                        final_chunks.append(sub_chunk)
                    prev_split = split
        
        return final_chunks


    def get_file_text(self, path):
        """Open and parse XML file, extracting both text content and metadata."""
        try:
            with open(path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'xml')  # Use 'xml' parser for XML files
                # Extract metadata
                metadata = self.get_metadata(soup,path)
                # Get the main text content (excluding metadata)
                text = self.clean_text(soup.get_text())

                #chunk text
                chunks = self.chunking(text)
                return metadata, chunks
                
                
        except Exception as e:
            print(f"Error reading file {path}: {e}")
            return None

    
    def get_largest_tokensize(self) -> int:
        filepaths = self.data.get_file_paths()
        max = 0 
        for path in filepaths:
            text = self.get_file_text(path)
            if len(text)/4 > max:
                print(f"Processing file: {path}")
                max = len(text)/4
                print(f"Current max token size: {max}")
        return max

if __name__ == "__main__":
    chunker = Chunker("fixed_size")
    files = chunker.file_paths
    print(len(chunker.file_paths))
    #choose rnadom file from file_paths  list
    pc = Pinecone(api_key="API KEY HERE")
    index = pc.Index(host="https://ragproject-.......")
    for i, file in enumerate(files): 
        print(file)
        id1 = "file" + str(i+1)
        metadata, data = chunker.get_file_text(file)
        print(metadata)
        print(data)
        if not data:
            print(f"Skipping empty file: {file}")
            continue
        for j,chunk in enumerate(data):
            index.upsert_records(
                "chunks",
                [
                {
                "_id": str(id1) + "#" + str(j+1),
                "text": chunk,
                "file_path": metadata["path"],
                "judgment_date": metadata.get("judgment_date", ""),
                "author": metadata.get("author", ""),
                "uri": metadata.get("uri", ""),
                }]
            )
        breakpoint()
        
