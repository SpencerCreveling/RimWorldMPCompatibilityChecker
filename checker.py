import pandas as pd
import xml.etree.ElementTree as ET
import os



def main():
    #initial start up the get important paths
    if(not os.path.isfile("paths.config")):
        print("Running First time setup... Please enter the path for you Rimworld workshop folder")
        dir1 = input("for WINDOWS the default diretory is (SteamLibrary\\steamapps\\workshop\\content\\294100)")
        print("Please enter the path for your Rimworld config folder")
        dir2 = input("for WINDOWS the default diretory is (Users\\\{USER\}\\AppData\\LocalLow\\Ludeon Studios\\RimWorld by Ludeon Studios\\Config)")
        f = open("paths.config", "x")
        f.write(dir1 + "\n" + dir2)
        f.close()
    
    steamModsDir, configURL,  NHT, IHT, MHT = updateData()
    printOptions()

    while(True):
        command = input("Enter Command: ").strip().lower()
        commandTokens = command.split(" ")
        match commandTokens[0]:
            case "help":
                printOptions()
            case "check":
                match commandTokens[1]:
                    case "all":
                        compatibility = downloadedCompatibility(MHT, IHT, NHT)
                        printCompatibility(compatibility)
                    case "active":
                        activeMods, root = indexModList(configURL)
                        compatibility = loadedCompatibility(activeMods, MHT, IHT, NHT)
                        printCompatibility(compatibility)
                    case "modList":
                        path = commandTokens[2]
                        activeMods, root = indexModList(path)
                        compatibility = loadedCompatibility(activeMods, MHT, IHT, NHT)
                        printCompatibility(compatibility)
                    case "mod":
                        modArg = ""
                        for i in range(2, len(commandTokens)):
                            modArg += " " + commandTokens[i]
                        modCompatibility(modArg.strip(), IHT, NHT)
                        




    


def printOptions():
    print("Commands:")
    print("check all - checks combatibility of all downloaded mods")
    print("check active - checks combatibility of all active mods")
    print("check modList <Mod list Path> - checks combatibility of a specific mod list from RimPy")
    print("check mod <Mod Name> - checks combatibility of a specific mod")
    print("check <Steam ID> - checks combatibility of a specific mod")
    print("loaded list - lists all loaded mods")
    print("remove <Mod Name> - removes a mod from the loaded list")
    print("remove <status 0-4> - removes all mod from the loaded list of provided status")
    print("save - saves the loaded list to Rimworld (Warning: this will overwrite your current loaded list and may not be a good load order)")
    print("save <Mod list Path> <fileName> - saves the loaded list to a specific path")
    print("help - prints this menu")
    print("")


def updateData():
    f = open("paths.config", "r")
    #data that will always be used
    steamModsDir = f.readline().strip()
    configURL = f.readline().strip()
    NHT, IHT = grabCompList()
    MHT =IndexSteamMods(steamModsDir)
    f.close()
    return steamModsDir, configURL,  NHT, IHT, MHT

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

def indexModList(configURL):
    #fetch all mods in the config file
    configURL = os.path.join(configURL, "ModsConfig.xml")
    tree = ET.parse(configURL)   
    root = tree.getroot()
    activeMods = root[1]
    return activeMods, root

def IndexSteamMods(steamModsDir):
    #index all installed mods
    MHT = {}
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
    return MHT

def loadedCompatibility(activeMods, MHT, IHT, NHT):
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
    return compatibility

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

def modCompatibility(modArg, IHT, NHT):
    if(modArg in IHT):
        statuse = IHT[modArg]
    elif(modArg in NHT):
        statuse = NHT[modArg.lower()]
    else:
        statuse = 0

    print("Status" + " | " + "Mod name")
    print(str(statuse) + " | " + modArg)

def printCompatibility(compatibility):
    #output results
    print("Status" + " | " + "Mod name")
    for i in range(len(compatibility)):
        for mod in compatibility[i]:
            print(str(i) + " | " + mod)
        print("--------------------")

main()





    
