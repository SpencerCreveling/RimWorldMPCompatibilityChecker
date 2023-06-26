import tkinter as tk
from tkinter import filedialog
from library import *

class modGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RimWorld MP compatibility manager")
        self.root.geometry("600x800")

        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=0)

        self.Paths = tk.Button(self.root, text="Paths", height=1,command=self.displayPaths)
        self.Paths.grid(row=0, column=0,sticky="nw")

        self.SortButton = tk.Button(self.root, text="Sort Numericaly", height=1,command=self.updateAllModList)
        self.SortButton.grid(row=0, column=1,sticky="ne")

        self.alphabeticSort = True

        self.Modlist = tk.Listbox(self.root)
        self.mods = indexSteamMods(getPaths()[0])
        self.updateAllModList()
        self.Modlist.grid(row=1, column=0,sticky="nsew")
        


        self.root.mainloop()

    def displayPaths(self):

        self.PathPopup = tk.Tk()
        self.PathPopup.title("Paths")
        self.PathPopup.geometry("600x100")

        self.PathPopup.rowconfigure(0, weight=1)
        self.PathPopup.rowconfigure(1, weight=1)
        self.PathPopup.rowconfigure(2, weight=1)

        self.PathPopup.columnconfigure(0, weight=0)
        self.PathPopup.columnconfigure(1, weight=4)
        self.PathPopup.columnconfigure(2, weight=0)
        
        self.paths = getPaths()
        self.steamModsDir = tk.StringVar(self.PathPopup, value= self.paths[0])
        self.configDIR = tk.StringVar(self.PathPopup, value= self.paths[1])
        self.rimworldDir = tk.StringVar(self.PathPopup, value= self.paths[2])

        steamLabel = tk.Label(self.PathPopup, text="Steam Mods Directory",font=("Arial", 8))
        configLabel = tk.Label(self.PathPopup, text="Config Directory",font=("Arial", 8))
        rimworldLabel = tk.Label(self.PathPopup, text="RimWorld Directory",font=("Arial", 8))

        steamEntry = tk.Label(self.PathPopup, textvariable=self.steamModsDir,font=("Arial", 8),relief="sunken",anchor="w")
        configEntry = tk.Label(self.PathPopup, textvariable=self.configDIR,font=("Arial", 8),relief="sunken",anchor="w")
        rimworldEntry = tk.Label(self.PathPopup, textvariable=self.rimworldDir,font=("Arial", 8),relief="sunken",anchor="w")

        steamButton = tk.Button(self.PathPopup, text="Select", height=1,command= self.selectSteamPath)
        configButton = tk.Button(self.PathPopup, text="Select", height=1,command= self.selectConfigPath)
        rimworldButton = tk.Button(self.PathPopup, text="Select", height=1,command= self.selectRimworldPath)

        steamLabel.grid(row=0, column=0, sticky="nw")
        configLabel.grid(row=1, column=0, sticky="nw")
        rimworldLabel.grid(row=2, column=0, sticky="nw")

        steamEntry.grid(row=0, column=1, sticky="new")
        configEntry.grid(row=1, column=1, sticky="new")
        rimworldEntry.grid(row=2, column=1, sticky="new")

        steamButton.grid(row=0, column=2, sticky="new")
        configButton.grid(row=1, column=2, sticky="new")
        rimworldButton.grid(row=2, column=2, sticky="new")

        self.PathPopup.mainloop()

    def selectSteamPath(self):
        filename = filedialog.askdirectory(parent= self.PathPopup,initialdir=self.steamModsDir.get())
        self.steamModsDir.set(filename)
        self.paths[0] = filename
        savePaths(self.paths)

    def selectConfigPath(self):
        filename = filedialog.askdirectory(parent= self.PathPopup,initialdir=self.configDIR.get())
        self.configDIR.set(filename)
        self.paths[1] = filename
        savePaths(self.paths)

    def selectRimworldPath(self):
        filename = filedialog.askdirectory(parent= self.PathPopup,initialdir=self.rimworldDir.get())
        self.rimworldDir.set(filename)
        self.paths[2] = filename
        savePaths(self.paths)

    def updateAllModList(self):
        self.Modlist.delete(0, tk.END)
        if(self.alphabeticSort):
            self.SortButton.config(text="Sort Numericaly")
            self.mods.sort(key=lambda x: x.name)
            for mod in self.mods:
                self.Modlist.insert(tk.END, mod)
                self.Modlist.itemconfig(tk.END, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
        else:
            self.SortButton.config(text="Sort Alphabeticaly")
            self.mods.sort(key=lambda x: x.compatibility)
            for mod in self.mods:
                self.Modlist.insert(0, mod)
                self.Modlist.itemconfig(0, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
        self.alphabeticSort = not self.alphabeticSort



__imit__ = modGUI()
