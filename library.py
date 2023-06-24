import os
import pickle
import xml.etree.ElementTree as ET
import pandas as pd

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

def grabCompList():
    #grab compatibility data from master coompatibility list
    SHEET_ID = "1jaDxV8F7bcz4E9zeIRmZGKuaX7d0kvWWq28aKckISaY"
    SHEET_NAME = 'MasterCompatibilityList'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    df = pd.read_csv(url)

    NHT = {}
    IHT = {}
    for i in range(len(df)):
        grabber = df.iloc[i,0]
        NHT[str(df.loc[i,"Mod name"]).lower()] = grabber #NAME HASH TABLE
        IHT[str(df.loc[i,"Steam ID"])] = grabber  #ID HASH TABLE
    return NHT, IHT

def downloadedCompatibility(MHT, IHT, NHT):
    compatibility = [[],[],[],[],[]]
    #compare MHT to master list
    for mod in MHT:
        if(MHT[mod][1] in IHT):
            compatibility[IHT[MHT[mod][1]]].append(MHT[mod][0])
        elif(MHT[mod][0].lower() in NHT):
            compatibility[NHT[MHT[mod][0].lower()]].append(MHT[mod][0])
        else:
            compatibility[0].append(MHT[mod][0])
    return compatibility