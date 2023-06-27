import tkinter as tk
from library import *
from mod import *

class ModList():
    def __init__(self,LoadedStatuse,root):

        self.masterBox = tk.Frame(root)
        self.masterBox.columnconfigure(0, weight=1)
        self.masterBox.rowconfigure(0, weight=0)
        self.masterBox.rowconfigure(1, weight=1)

        self.LoadedStatuse = LoadedStatuse

        #mod list sort / search frame
        self.ModOptionFrame = tk.Frame(self.masterBox)
        self.ModOptionFrame.grid(row=0, column=0,sticky="nsew")
        self.ModOptionFrame.rowconfigure(0, weight=1)
        self.ModOptionFrame.columnconfigure(0, weight=0)
        self.ModOptionFrame.columnconfigure(1, weight=1)

        #sort button to sort the list either by compatibility or aplpabaticly 
        self.SortButton = tk.Button(self.ModOptionFrame, text="Sort Numericaly", height=1,command=self.Sortlists)
        self.SortButton.grid(row=0, column=0 ,sticky="nsew")
        self.AlphabeticSort = True

        #search bar to search for  mods
        self.SearchBar = tk.Entry(self.ModOptionFrame, relief="sunken",)
        self.SearchBar.grid(row=0, column=1,sticky="nsew")
        self.SearchBar.bind("<KeyRelease>", self.filter)

        #unloaded mod list
        self.ModList = tk.Listbox(self.masterBox)
        self.mods = indexSteamMods(getPaths()[0])
        self.mods = updateLoadedMods(self.mods)
        self.updateModList()
        self.ModList.grid(row=1, column=0,sticky="nsew")

    def Sortlists(self):
        self.AlphabeticSort = not self.AlphabeticSort
        if(self.AlphabeticSort):
            self.SortButton.config(text="Sort Numericaly")
        else:
            self.SortButton.config(text="Sort Alphabeticaly")
        self.updateModList()

    def filter(self,e):
        self.updateModList()

    def updateModList(self):
        self.ModList.delete(0, tk.END)
        if(self.AlphabeticSort):
            self.mods.sort(key=lambda x: x.name)
            for mod in self.mods:
                if(self.LoadedStatuse == mod.loaded):
                    if(not self.SearchBar.get() == "" and self.SearchBar.get().lower() in mod.name.lower()):
                        self.ModList.insert(tk.END, mod)
                        self.ModList.itemconfig(tk.END, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
                    elif(self.SearchBar.get() == ""):
                        self.ModList.insert(tk.END, mod)
                        self.ModList.itemconfig(tk.END, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
        else:
            self.mods.sort(key=lambda x: x.compatibility)
            for mod in self.mods:
                if(self.LoadedStatuse == mod.loaded):
                    if(not self.SearchBar.get() == "" and self.SearchBar.get().lower() in mod.name.lower()):
                        self.ModList.insert(0, mod)
                        self.ModList.itemconfig(0, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
                    elif(self.SearchBar.get() == ""):
                        self.ModList.insert(0, mod)
                        self.ModList.itemconfig(0, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
    

    def grid(self,row,column,sticky):
        self.masterBox.grid(row=row, column=column,sticky=sticky)
