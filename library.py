import os
import pickle
import xml.etree.ElementTree as ET

def getPaths():
    if(os.path.isfile("paths.config")):
        paths = pickle.load(open("paths.config", "rb"))
    else:
        paths = ["","",""]
        pickle.dump(paths, open("paths.config", "wb"))
    return paths

def savePaths(paths):
    pickle.dump(paths, open("paths.config", "wb"))

def indexSteamMods(steamModsDir):
    #index all installed mods
    MHT = {}
    if(not os.path.exists(steamModsDir)):
        print("Steam Mods Directory not found make sure you enterd the right path in paths.config")
        return
    content = os.listdir(steamModsDir)
    #for mod in content:
    for mod in content:
        #steam workshop id
        id = mod
        #data path for about..xml
        modDataPath = os.path.join(steamModsDir, mod)
        modDataPath = os.path.join(modDataPath, "About")
        modDataPath = os.path.join(modDataPath, "About.xml")
        if(os.path.exists(modDataPath)):
            tree = ET.parse(modDataPath)
            root = tree.getroot()
            name = ""
            packageID = ""
            #extracting name / packageID to compare to master list and modsconfig.xml
            for child in root:
                if(child.tag == "name"):
                    name = child.text
                if(child.tag == "packageId"):
                    packageID = child.text
            MHT[packageID.lower()] = [name, id]
    return MHT