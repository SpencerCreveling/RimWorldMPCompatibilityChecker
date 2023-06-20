import os
import pickle
def getPaths():
    if(os.path.isfile("paths.config")):
        paths = pickle.load(open("paths.config", "rb"))
    else:
        paths = ["","",""]
        pickle.dump(paths, open("paths.config", "wb"))
    return paths

def savePaths(paths):
    pickle.dump(paths, open("paths.config", "wb"))