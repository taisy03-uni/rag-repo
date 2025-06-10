
class Embedder():
    def __init__(self, model):
        self.model = model 

    def get_file_paths(self, court = "", year = ""):
        paths = []
        if court == "" and year == "":
            court = "data/court"
            
            #return list of all file paths
        elif court != "" and year == "":
            return None
            #return list of file paths for the given court/tribunal
        elif court == "" and year != "":
            return None
            #return list of file paths for the given year
