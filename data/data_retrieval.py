import requests
import os
import time

class DataDownload():
    def __init__(self):
        self.main_url = "https://caselaw.nationalarchives.gov.uk"
        self.tags_court = [
            {"uksc": "United Kingdom Supreme Court"}, 
            {"ukpc": "United Kingdom Privy Council"},
            {"ewca": [
                {"ewca%2Fciv": "Court of Appeal (Civil Division)"},
                {"ewca%2Fcrim" : "Court of Appeal (Criminal Division)"}
                ]},
            {"ewhc": [
                {"ewhc%2Fadmin": "High Court (Administrative Court)"},
                {"ewhc%2Fadmlty": "High Court (Admiralty Division)"},
                {"ewhc%2Fch": "High Court (Chancery Division)"},
                {"ewhc%2Fcomm": "High Court (Commercial Court)"},
                {"ewhc%2Ffam": "High Court (Family Division)"},
                {"ewhc%2Fipec": "High Court (Intellectual Property Enterprise Court)"},
                {"ewhc%2Fkb": "High Court (King's Bench Division)"},
                {"ewhc%2Fmercantile": "High Court (Mercantile Court)"},
                {"ewhc%2Fpat": "High Court (Patents Court)"},
                {"ewhc%2Fscco": "High Court (Senior Court Costs Office)"},
                {"ewhc%2Ftcc": "High Court (Technology and Construction Court)"}
                ]},
            {"ewcr": "Crown Court"},
            {"ewcc": "County Court"},
            {"ewfc": "Family Court"},
            {"ewcop": "Court of Protection"}]

        self.tags_tribunals = [
            {"ukiptrib": "Investigatory Powers Tribunal"},
            {"eat": "Employment Appeal Tribunal"},
            {"ukut": [
                {"ukut%2Faac": "Upper Tribunal (Administrative Appeals Chamber)"},
                {"ukut%2Fiac": "Upper Tribunal (Immigration and Asylum Chamber)"},
                {"ukut%2Flc": "Upper Tribunal (Lands Chamber)"},
                {"ukut%2Ftcc": "Upper Tribunal (Tax and Chancery Chamber)"}
                ]},
            {"ukftt": [
                {"ukftt%2Fgrc": "First-tier Tribunal (General Regulatory Chamber)"},
                {"ukftt%2Ftc": "First-tier Tribunal (Tax Chamber)"}
                ]},
            {"ukist": "Immigration Services Tribunal"}]
        self.years = [str(year) for year in range(2000, 2025)]  
        self.make_folders_court()
        self.make_folders_tribunal()
    
    def make_folders_court(self):
        print("Making folders for the courts...")
        for tag in self.tags_court:
            #make the folder for the court
            court = list(tag.keys())[0]
            #make folder
            folder_name = f"data/court/{court}"
            try:
                os.makedirs(folder_name)
            except FileExistsError:
                print(f"Folder {folder_name} already exists")
            # if tag value is a list, iterate through the list
            if isinstance(tag[list(tag.keys())[0]], list):
                for sub_tag in tag[list(tag.keys())[0]]:
                        subtag = list(sub_tag.keys())[0]
                        folder_name = f"data/court/{court}/{subtag}"
                        try:
                            os.makedirs(folder_name)
                        except FileExistsError:
                            print(f"Folder {folder_name} already exists")

    def make_folders_tribunal(self):
        print("Making folders for tribunals...")
        for tag in self.tags_tribunals:
            court = list(tag.keys())[0]
            #make folder
            folder_name = f"data/tribunals/{court}"
            try:
                os.makedirs(folder_name)
            except FileExistsError:
                print(f"Folder {folder_name} already exists")
            # if tag value is a list, iterate through the list
            if isinstance(tag[list(tag.keys())[0]], list):
                for sub_tag in tag[list(tag.keys())[0]]:
                        subtag = list(sub_tag.keys())[0]
                        folder_name = f"data/tribunals/{court}/{subtag}"
                        try:
                            os.makedirs(folder_name)
                        except FileExistsError:
                            print(f"Folder {folder_name} already exists")
            

    def get_data(self, court, year, c_or_t = "court"):
        if c_or_t == "court":
            self.get_court_data(court, year)
        elif c_or_t == "tribunal":
            self.get_tribunal_data(court, year)

    def get_court_data(self, court, year):
        print(f"Getting data for {court} in {year}")
        url = f"{self.main_url}/atom.xml?court={court}&from_date_2={year}&to_date_2={year}"

        folder = f"data/court/{court}/{year}"
        data = requests.get(url).text
        

        # Save the data to a file
        with open(f"data/court/{court}/{year}.xml", "w") as file:
            file.write(data)
        





main_url = "https://caselaw.nationalarchives.gov.uk"

data = requests.get("https://caselaw.nationalarchives.gov.uk/atom.xml?court=uksc&from_date_2=2025&to_date_2=2025").text

data2 = requests.get("https://caselaw.nationalarchives.gov.uk/uksc/2025/15/data.xml").text

# Save the data to a file
with open("data/aatom.xml", "w") as file:
    file.write(data)





