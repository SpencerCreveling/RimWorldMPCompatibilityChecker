import tkinter as tk
from library import *
from paths import *

class modGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RimWorld MP compatibility manager")
        self.root.geometry("600x800")
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        #OPTION FRAME TOP ROW
        self.optionframe = tk.Frame(self.root)
        self.optionframe.grid(row=0, column=0,sticky="nsew")
        self.Paths = tk.Button(self.optionframe, text="Paths", height=1,command=lambda: paths(self.root))
        self.Paths.grid(row=0, column=0,sticky="nw")
        
        #LIST FRAME THE LIST OF MODS
        self.listFrame = tk.Frame(self.root)
        self.listFrame.rowconfigure(0, weight=0)
        self.listFrame.rowconfigure(1, weight=1)
        self.listFrame.columnconfigure(0, weight=1)
        self.listFrame.columnconfigure(1, weight=1)
        self.listFrame.grid(row=1, column=0,sticky="nsew")

        #deactive mods option frame
        self.deactiveModOptionFrame = tk.Frame(self.listFrame)
        self.deactiveModOptionFrame.grid(row=0, column=0,sticky="nsew")
        self.deactiveModOptionFrame.rowconfigure(0, weight=1)
        self.deactiveModOptionFrame.columnconfigure(0, weight=0)
        self.deactiveModOptionFrame.columnconfigure(1, weight=1)

        #active mods option frame
        self.activeModOptionFrame = tk.Frame(self.listFrame)
        self.activeModOptionFrame.grid(row=0, column=1,sticky="nsew")
        self.activeModOptionFrame.rowconfigure(0, weight=1)
        self.activeModOptionFrame.columnconfigure(0, weight=0)
        self.activeModOptionFrame.columnconfigure(1, weight=1)

        #sort button to sort the deactive list either by compatibility or aplpabaticly 
        self.deactiveSortButton = tk.Button(self.deactiveModOptionFrame, text="Sort Numericaly", height=1,command=self.deactiveSortlists)
        self.deactiveSortButton.grid(row=0, column=0 ,sticky="nsew")
        self.deactiveAlphabeticSort = True

        #sort button to sort the active list either by compatibility or aplpabaticly
        self.activeSortButton = tk.Button(self.activeModOptionFrame, text="Sort Numericaly", height=1,command=self.activeSortlists)
        self.activeSortButton.grid(row=0, column=0 ,sticky="nsew")
        self.activeAlphabeticSort = True
      
        #search bar to search for deactive mods
        self.deactiveSearchBar = tk.Entry(self.deactiveModOptionFrame, relief="sunken",)
        self.deactiveSearchBar.grid(row=0, column=1,sticky="nsew")
        self.deactiveSearchBar.bind("<KeyRelease>", self.deactiveFilter)

        #search bar to search for active mods
        self.activeSearchBar = tk.Entry(self.activeModOptionFrame, relief="sunken",)
        self.activeSearchBar.grid(row=0, column=1,sticky="nsew")
        self.activeSearchBar.bind("<KeyRelease>", self.activeFilter)
        
        #unloaded mod list
        self.DeActiveModList = tk.Listbox(self.listFrame)
        self.mods = indexSteamMods(getPaths()[0])
        self.mods = updateLoadedMods(self.mods)
        self.updateDeActiveModList()
        self.DeActiveModList.grid(row=1, column=0,sticky="nsew")

        #loaded mod list
        self.ActiveModlist = tk.Listbox(self.listFrame)
        self.mods = indexSteamMods(getPaths()[0])
        self.mods = updateLoadedMods(self.mods)
        self.updateActiveModList()
        self.ActiveModlist.grid(row=1, column=1,sticky="nsew")

        self.root.mainloop()   



    def deactiveSortlists(self):
        self.deactiveAlphabeticSort = not self.deactiveAlphabeticSort
        if(self.deactiveAlphabeticSort):
            self.deactiveSortButton.config(text="Sort Numericaly")
        else:
            self.deactiveSortButton.config(text="Sort Alphabeticaly")
        self.updateDeActiveModList()

    def activeSortlists(self):
        self.activeAlphabeticSort = not self.activeAlphabeticSort
        if(self.activeAlphabeticSort):
            self.activeSortButton.config(text="Sort Numericaly")
        else:
            self.activeSortButton.config(text="Sort Alphabeticaly")
        self.updateActiveModList()

    def updateDeActiveModList(self):
        self.DeActiveModList.delete(0, tk.END)
        if(self.deactiveAlphabeticSort):
            self.mods.sort(key=lambda x: x.name)
            for mod in self.mods:
                if(not mod.loaded):
                    if(not self.deactiveSearchBar.get() == "" and self.deactiveSearchBar.get().lower() in mod.name.lower()):
                        self.DeActiveModList.insert(tk.END, mod)
                        self.DeActiveModList.itemconfig(tk.END, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
                    elif(self.deactiveSearchBar.get() == ""):
                        self.DeActiveModList.insert(tk.END, mod)
                        self.DeActiveModList.itemconfig(tk.END, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
        else:
            self.mods.sort(key=lambda x: x.compatibility)
            for mod in self.mods:
                if(not mod.loaded):
                    if(not self.deactiveSearchBar.get() == "" and self.deactiveSearchBar.get().lower() in mod.name.lower()):
                        self.DeActiveModList.insert(0, mod)
                        self.DeActiveModList.itemconfig(0, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
                    elif(self.deactiveSearchBar.get() == ""):
                        self.DeActiveModList.insert(0, mod)
                        self.DeActiveModList.itemconfig(0, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
    
    def updateActiveModList(self):
        self.ActiveModlist.delete(0, tk.END)
        if(self.activeAlphabeticSort):
            self.mods.sort(key=lambda x: x.name)
            for mod in self.mods:
                if(mod.loaded):
                    if(not self.activeSearchBar.get() == "" and self.activeSearchBar.get().lower() in mod.name.lower()):
                        self.ActiveModlist.insert(tk.END, mod)
                        self.ActiveModlist.itemconfig(tk.END, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
                    elif(self.activeSearchBar.get() == ""):
                        self.ActiveModlist.insert(tk.END, mod)
                        self.ActiveModlist.itemconfig(tk.END, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
        else:
            self.mods.sort(key=lambda x: x.compatibility)
            for mod in self.mods:
                if(mod.loaded):
                    if(not self.activeSearchBar.get() == "" and self.activeSearchBar.get().lower() in mod.name.lower()):
                        self.ActiveModlist.insert(0, mod)
                        self.ActiveModlist.itemconfig(0, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
                    elif(self.activeSearchBar.get() == ""):
                        self.ActiveModlist.insert(0, mod)
                        self.ActiveModlist.itemconfig(0, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
    
    def deactiveFilter(self,e):
        self.updateDeActiveModList()

    def activeFilter(self,e):
        self.updateActiveModList()
        
        
        



__imit__ = modGUI()
