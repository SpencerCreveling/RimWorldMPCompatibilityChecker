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
        print("Please enter the path for your Rimworld install location")
        dir3 = input("for WINDOWS the default diretory is (SteamLibrary\\steamapps\\common\\RimWorld)")
        f = open("paths.config", "x")
        f.write(dir1 + "\n" + dir2 + "\n" + dir3)
        f.close()
    
    rimworldDir, steamModsDir, configURL,  NHT, IHT, MHT = updateData()
    printOptions()
    LoadedXML = None
    while(True):
        command = input("Enter Command: ").strip().lower()
        commandTokens = command.split(" ")
        match commandTokens[0]:
            case "help":
                printOptions()
            case "update":
                rimworldDir, steamModsDir, configURL,  NHT, IHT, MHT = updateData()
            case "check":
                match commandTokens[1]:
                    case "all":
                        compatibility = downloadedCompatibility(MHT, IHT, NHT)
                        printCompatibility(compatibility)
                    case "active":
                        configURL = os.path.join(configURL, "ModsConfig.xml")
                        activeMods, root = indexModList(configURL)
                        compatibility = loadedCompatibility(activeMods, MHT, IHT, NHT)
                        printCompatibility(compatibility)
                    case "modlist":
                        path = commandTokens[2]
                        activeMods, root = indexModList(path)
                        compatibility = loadedCompatibility(activeMods, MHT, IHT, NHT)
                        printCompatibility(compatibility)
                    case "mod":
                        modArg = ""
                        for i in range(2, len(commandTokens)):
                            modArg += " " + commandTokens[i]
                        modCompatibility(modArg.strip(), IHT, NHT)
                    case "loaded":
                        if(LoadedXML != None):
                            compatibility = loadedCompatibility(LoadedXML, MHT, IHT, NHT)
                            printCompatibility(compatibility)
                        else:
                            print("no list loaded to check")
                    case _:
                        print("Invalid Command")
            case "load":
                match commandTokens[1]:
                    case "all":
                        LoadedXML = loadAllMods(MHT,os.path.join(configURL, "ModsConfig.xml"),rimworldDir)
                    case "active":
                        LoadedXML = ET.parse(os.path.join(configURL, "ModsConfig.xml"))
                        LoadedXML = LoadedXML.getroot()
                    case "modlist":
                        path = commandTokens[2]
                        LoadedXML = ET.parse(path)
                        LoadedXML = LoadedXML.getroot()
                    case _:
                        print("Invalid Command")
            case "add":
                if(LoadedXML != None):
                    modArg = ""
                    for i in range(1, len(commandTokens)):
                        modArg += " " + commandTokens[i]
                    LoadedXML = addMod(modArg.strip(), LoadedXML, MHT)
                else:
                    print("no list loaded to modify")
            case "remove":
                if(LoadedXML != None):
                    if(commandTokens[1].isdigit() and int(commandTokens[1]) < 4):
                        LoadedXML = removeModRange(int(commandTokens[1]), LoadedXML,MHT,NHT,IHT)
                    else:   
                        modArg = ""
                        for i in range(1, len(commandTokens)):
                            modArg += " " + commandTokens[i]
                        LoadedXML = removeMod(modArg.strip(), LoadedXML, MHT)
                else:
                    print("no list loaded to modify")
            case "save":
                if(LoadedXML == None):
                    if(len(commandTokens) == 1):
                        saveDir = os.path.join(configURL, "ModsConfig.xml")
                    else: 
                        saveDir = commandTokens[1]
                    ET.ElementTree(LoadedXML).write(saveDir)
                else:
                    print("no list loaded to save")
            case _:
                print("Invalid Command")

                        
def printOptions():
    print("Commands:")
    print("check all - checks combatibility of all downloaded mods")
    print("check active - checks combatibility of all active mods")
    print("check modList <Mod list Path> - checks combatibility of a specific mod list from RimPy")
    print("check mod <Mod Name> - checks combatibility of a specific mod")
    print("check mod <Steam ID> - checks combatibility of a specific mod")
    print("check loaded - lists all loaded mods and their status")
    print("load all - loads all subscibed mods from the workshop")
    print("load active - loads all active mods")
    print("load modlist <Mod list Path> - loads a specific mod list from RimPy")
    print("add <Mod Name> - adds a mod to the loaded list")
    print("add <Steam ID> - adds a mod to the loaded list")
    print("remove <Mod Name> - removes a mod from the loaded list")
    print("remove <Steam ID> - removes a mod from the loaded list")
    print("remove <status 0-4> - removes all mod from the loaded list of provided status")
    print("save - saves the loaded list to Rimworld (Warning: this will overwrite your current loaded list and may not be a good load order)")
    print("save <Mod list Path> <fileName> - saves the loaded list to a specific path (Note: can then be loaded into RimPy for sorting / editing)")
    print("update - updates all data (Note: run this if you have added or removed mods from the workshop or activated / deactivated mods)")
    print("change path - changes the paths for Rimworld install, Steam Mods, and Rimworld config")
    print("help - prints this menu")
    print("")


def updateData():
    f = open("paths.config", "r")
    #data that will always be used
    steamModsDir = f.readline().strip()
    configURL = f.readline().strip()
    rimworldDir = f.readline().strip()
    NHT, IHT = grabCompList()
    MHT =IndexSteamMods(steamModsDir)
    f.close()
    print("data updated successfully")
    return rimworldDir,steamModsDir, configURL,  NHT, IHT, MHT

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
    if(not os.path.exists(configURL)):
        print("Config file not found make sure you enterd the right path in paths.config")
        return
    #fetch all mods in the config file
    tree = ET.parse(configURL)   
    root = tree.getroot()
    activeMods = root[1]
    return activeMods, root

def IndexSteamMods(steamModsDir):
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

def loadedCompatibility(loadedXML,MHT,IHT,NHT):
    compatibility = [[],[],[],[],[]]
    #compare loaded xml with the compatability list
    for mod in loadedXML[1]:
        if("ludeon" not in mod.text):
            name = MHT[mod.text][0]
            id = MHT[mod.text][1]

            if(id in IHT):
                compatibility[IHT[id]].append(name)
            elif(name.lower() in NHT):
                compatibility[NHT[name.lower()]].append(name)
            else:
                compatibility[0].append(name)
    return compatibility

def loadAllMods(MHT,configURL,rimworldDir):
    rimworldDir = os.path.join(rimworldDir, "Data")
    #load in sample xml
    loadedXML = ET.parse(configURL)
    loadedXML = loadedXML.getroot()
    #removes exisitng mods
    for mod in loadedXML[1].findall("li"):
        loadedXML[1].remove(mod)
    for mod in loadedXML[2].findall("li"):
        loadedXML[2].remove(mod)
    #add all worshop mods
    for mod in MHT:
        newMod = ET.fromstring("<li>" + mod + "</li>")
        loadedXML[1].append(newMod)
    #add all relevent DLC
    if(os.path.exists(os.path.join(rimworldDir, "Core"))):
        newMod = ET.fromstring("<li>" + "ludeon.rimworld" + "</li>")
        loadedXML[2].append(newMod)
        loadedXML[1].append(newMod)
    if(os.path.exists(os.path.join(rimworldDir, "Royalty"))):
        newMod = ET.fromstring("<li>" + "ludeon.rimworld.royalty" + "</li>")
        loadedXML[2].append(newMod)
        loadedXML[1].append(newMod)
    if(os.path.exists(os.path.join(rimworldDir, "Ideology"))):
        newMod = ET.fromstring("<li>" + "ludeon.rimworld.ideology" + "</li>")
        loadedXML[2].append(newMod)
        loadedXML[1].append(newMod)
    if(os.path.exists(os.path.join(rimworldDir, "Biotech"))):
        newMod = ET.fromstring("<li>" + "ludeon.rimworld.biotech" + "</li>")
        loadedXML[2].append(newMod)
        loadedXML[1].append(newMod)
    print("All mods loaded successfully")
    return loadedXML

def addMod(modArg, LoadedXML, MHT):
    for keys in MHT:
        if(MHT[keys][0].lower() == modArg.lower()):
            newMod = ET.fromstring("<li>" + keys + "</li>")
            LoadedXML[1].append(newMod)
            print("Mod loaded successfully")
            return LoadedXML
    print("Mod not found")
    return LoadedXML
        
def removeMod(modArg, LoadedXML, MHT):
    for keys in MHT:
        if(MHT[keys][0].lower() == modArg.lower()):
            for mod in LoadedXML[1].findall("li"):
                if(mod.text == keys):
                    LoadedXML[1].remove(mod)
                    print("Mod removed successfully")
                    return LoadedXML
    print("Mod not found")
    return LoadedXML

def removeModRange(range, LoadedXML,MHT,NHT,IHT):
    for mod in LoadedXML[1]:
        if("ludeon" not in mod.text):
            name = MHT[mod.text][0]
            id = MHT[mod.text][1]
            if(id in IHT):
                if(IHT[id] == range):
                    LoadedXML[1].remove(mod)
            elif(name.lower() in NHT):
                if(NHT[name.lower()] == range):
                    LoadedXML[1].remove(mod)
            else:
                if(0 == range):
                    LoadedXML[1].remove(mod)
    return LoadedXML

def printCompatibility(compatibility):
    #output results
    print("Status" + " | " + "Mod name")
    for i in range(len(compatibility)):
        for mod in compatibility[i]:
            print(str(i) + " | " + mod)
        print("--------------------")






    
