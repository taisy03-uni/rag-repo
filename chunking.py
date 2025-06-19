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
        self.file_paths = self.data.get_file_paths()
        self.chunks = []


    def clean_text(self, text: str) -> str:
        text = re.sub(r'\n{2,}', '\n', text)
        text = re.sub(r' +', ' ', text)
        text = text.strip()
        #remove any line that begins with #judgment
        text = re.sub(r'(?m)^#judgment.*\n?', '', text)
        return text
    
    def get_metadata(self, soup, path):
        frbr_expression = soup.find('FRBRWork')
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

            frbr_name = frbr_expression.find('FRBRname')
            if frbr_name and 'value' in frbr_name.attrs:
                metadata['name'] = frbr_name['value']

            frbr_author = frbr_expression.find('FRBRauthor')
            if frbr_author and 'href' in frbr_author.attrs:
                metadata['author'] = frbr_author['href']
            
        return metadata
    
    def chunking(self, text):
        if len(text) < 1000:
            return [text]
        
        # First split by the separator pattern
        chunks = []
        parts = text.split('- - - - - - -')
        for part in parts:
            if part.strip():  # Skip empty/whitespace-only parts
                chunks.append(part.strip())
        new_chunks = []

        for chunk in chunks:
            if len(chunk) < 1000:
                new_chunks.append(chunk)
                continue
            # Find all matches of numbered items (e.g., "\n3. " or "\n3.\n")
            number_pattern = r'\n(\d+)\.\s*\n?'
            matches = list(re.finditer(number_pattern, chunk))
            
            # Filter valid sequential numbers (1, 2, 3, ...)
            valid_starts = []
            expected_num = 1
            for match in matches:
                current_num = int(match.group(1))
                if current_num == expected_num:
                    valid_starts.append(match.start())
                    expected_num += 1

            # Extract chunks between valid numbers
            prev_end = 0
            for start in valid_starts:
                chunk1 = chunk[prev_end:start].strip()
                if chunk1:
                    new_chunks.append(chunk1)
                prev_end = start
            # Add the remaining text after the last number
            if prev_end < len(chunk):
                new_chunks.append(chunk[prev_end:].strip())
        
        #if any chunk is still larger than 1000 characters, split it further
        final_chunks = []
        for chunk in new_chunks:
            if len(chunk) < 1000:
                final_chunks.append(chunk)
            else:
                # Split the chunk into smaller parts of max 1000 characters
                for i in range(0, len(chunk), 1000):
                    final_chunks.append(chunk[i:i + 1000])
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
    random_file = random.choice(files)
    print(f"Randomly selected file: {random_file}")
    metadata, data = chunker.get_file_text(random_file)
    # output metadata and chunks to output.txt
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(f"Metadata: {metadata}\n")
        f.write("Chunks:\n")
        for chunk in data:
            print('Chunk length:', len(chunk))  
            f.write(chunk + "\n\n\n\n\n\n\n\n\n\n")

    """pc = Pinecone(api_key="pcsk_3YbV67_G3gZeawEgTBxZr28MfvtG1DUcgeoqVHjZshkLbyxpcigKizCTsKHMNCLZyd9dhC")
    index = pc.Index(host="https://ragproject-kjuem0t.svc.aped-4627-b74a.pinecone.io")
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
        breakpoint()"""
        
