import tkinter as tk
from tkinter import filedialog
from library import getPaths, savePaths

class paths:
    def __init__(self, root):
        #path pop up to let user specifie install diretories
        self.PathPopup = tk.Tk()
        self.PathPopup.title("Paths")
        self.PathPopup.geometry("600x100")

        self.PathPopup.rowconfigure(0, weight=1)
        self.PathPopup.rowconfigure(1, weight=1)
        self.PathPopup.rowconfigure(2, weight=1)

        self.PathPopup.columnconfigure(0, weight=0)
        self.PathPopup.columnconfigure(1, weight=4)
        self.PathPopup.columnconfigure(2, weight=0)
        #get paths from file and populate the lables
        self.paths = getPaths()
        self.steamModsDir = tk.StringVar(self.PathPopup, value= self.paths[0])
        self.configDIR = tk.StringVar(self.PathPopup, value= self.paths[1])
        self.rimworldDir = tk.StringVar(self.PathPopup, value= self.paths[2])
        #the labels themselves
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