import requests

# Court cases around for 61,000 cases
tags_court = [{"uksc": "United Kingdom Supreme Court"}, 
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

# Tribunals only account for around 5,000 casses in the database
tags_tribunals = [
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

years = [str(year) for year in range(2000, 2025)]
#First, downloading all of the data in the courts
for tag in tags_court:


main_url = "https://caselaw.nationalarchives.gov.uk"

data = requests.get("https://caselaw.nationalarchives.gov.uk/atom.xml?court=uksc").text

data2 = requests.get("https://caselaw.nationalarchives.gov.uk/uksc/2025/15/data.xml").text

# Save the data to a file
with open("data/aatom.xml", "w") as file:
    file.write(data)


