import os
import pickle
import xml.etree.ElementTree as ET
import pandas as pd
from mod import *

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
    mods = []
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
            mods.append(Mod(name, packageID, id))
    mods = downloadedCompatibility(mods)
    return mods

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

def downloadedCompatibility(mods):
    NHT, IHT = grabCompList()
    for mod in mods:
        if(mod.id in IHT):
           mod.compatibility = IHT[mod.id]
        elif(mod.name.lower() in NHT):
            mod.compatibility = NHT[mod.name.lower()]
    return mods

def updateLoadedMods(mods):
    #update loaded mods from modsconfig.xml
    modsConfigPath = os.path.join(getPaths()[1], "ModsConfig.xml")
    if(not os.path.exists(modsConfigPath)):
        print("ModsConfig.xml not found make sure you enterd the right path in paths.config")
        return
    tree = ET.parse(modsConfigPath)
    root = tree.getroot()
    for mod in mods:
        for child in root[1]:
            if(mod.packageId.lower() == child.text.lower()):
                mod.loaded = True
    return mods