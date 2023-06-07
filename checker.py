import pandas as pd
import xml.etree.ElementTree as ET
import os

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

#fetch all mods in the config file
configURL = "C:\\Users\\Spencer\\AppData\\LocalLow\\Ludeon Studios\\RimWorld by Ludeon Studios\\Config\\ModsConfig.xml"
tree = ET.parse(configURL)   
root = tree.getroot()
activeMods = root[1]

#index all installed mods
MHT = {}
steamModsDir = "E:\\SteamLibrary\\steamapps\\workshop\\content\\294100"
content = os.listdir(steamModsDir)
#for mod in content:
for mod in content:
    #steam workshop id
    id = mod
    #data path for about..xml
    modDataPath = os.path.join(steamModsDir, mod)
    modDataPath = os.path.join(modDataPath, "About")
    modDataPath = os.path.join(modDataPath, "About.xml")
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

compatibility = [[],[],[],[],[]]
#compare modsconfig.xml to master list using HMT as a middleman
for mod in activeMods:
    if(mod.text in MHT):
        if(MHT[mod.text][1] in IHT):
            compatibility[IHT[MHT[mod.text][1]]].append(MHT[mod.text][0])
        elif(MHT[mod.text][0].lower() in NHT):
            compatibility[NHT[MHT[mod.text][0].lower()]].append(MHT[mod.text][0])
        else:
            compatibility[0].append(MHT[mod.text][0])

#output results
for i in range(len(compatibility)):
    for mod in compatibility[i]:
        print(str(i) + " | " + mod)
    print("--------------------")





    
