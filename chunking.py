from data.data_retrieval import DataDownload
from bs4 import BeautifulSoup
import re
import random  

class Chunker():
    def __init__(self, method):
        self.data = DataDownload()
        self.methods = ["fixed_size", "overlap"]
        self.file_paths = self.data.get_file_paths(court = "ewca%2Fciv")

    def clean_text(self, text: str) -> str:
        text = re.sub(r'\n{2,}', '\n', text)
        text = re.sub(r' +', ' ', text)
        text = text.strip()
        #remove any line that begins with #judgment
        text = re.sub(r'(?m)^#judgment.*\n?', '', text)
        return text
    
    def get_file_text(self, path):
        """Open and parse XML file using BeautifulSoup, returning the text content."""
        try:
            with open(path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'xml')
                return self.clean_text(soup.get_text())
        except Exception as e:
            print(f"Error reading file {path}: {e}")
            return None

    def chunk(self, data: list) -> list:
        """Chunk a list into smaller lists of specified size."""
        return [data[i:i + self.chunk_size] for i in range(0, len(data), self.chunk_size)]
    
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
    print(type(chunker.file_paths))
    #choose rnadom file from file_paths  list
    n = random.randint(0, len(chunker.file_paths) - 1)
    file = chunker.file_paths[n:n+1]  # Get a single file path
    print(f"Processing file: {file[0]}")
    data = chunker.get_file_text(path = file[0])
    #save to new file
    if data:
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(data)
    else:
        print("No data to write.")
    print("character count:", len(data))
    print("token count:", len(data)/4)  # Rough estimate of token count