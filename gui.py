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

        #LIST FRAME THE LIST OF MODS AND BUTTONS ABOVE THEM
        self.listFrame = tk.Frame(self.root)
        self.listFrame.rowconfigure(0, weight=0)
        self.listFrame.rowconfigure(1, weight=1)
        self.listFrame.columnconfigure(0, weight=1)
        self.listFrame.columnconfigure(1, weight=1)
        self.listFrame.grid(row=1, column=0,sticky="nsew")

        #sort button to sort the list either my compatibility or aplpabaticly 
        self.SortButton = tk.Button(self.listFrame, text="Sort Numericaly", height=1,command=self.sortlists)
        self.SortButton.grid(row=0, column=0,sticky="nw")
        self.alphabeticSort = True

        #search nar to search for mods
        self.SearchBar = tk.Entry(self.listFrame, relief="sunken",)
        self.SearchBar.grid(row=0, column=1,sticky="nsew")
        self.SearchBar.bind("<KeyRelease>", self.filter)

        #unloaded mod list
        self.Modlist = tk.Listbox(self.listFrame)
        self.mods = indexSteamMods(getPaths()[0])
        self.mods = updateLoadedMods(self.mods)
        self.updateAllModList()
        self.Modlist.grid(row=1, column=0,sticky="nsew")

        #loaded mod list
        self.ActiveModlist = tk.Listbox(self.listFrame)
        self.mods = indexSteamMods(getPaths()[0])
        self.mods = updateLoadedMods(self.mods)
        self.updateActiveModList()
        self.ActiveModlist.grid(row=1, column=1,sticky="nsew")

        self.root.mainloop()   



    def sortlists(self):
        self.alphabeticSort = not self.alphabeticSort
        if(self.alphabeticSort):
            self.SortButton.config(text="Sort Numericaly")
        else:
            self.SortButton.config(text="Sort Alphabeticaly")
        self.updateAllModList()
        self.updateActiveModList()

    def updateAllModList(self):
        self.Modlist.delete(0, tk.END)
        if(self.alphabeticSort):
            self.mods.sort(key=lambda x: x.name)
            for mod in self.mods:
                if(not mod.loaded):
                    if(not self.SearchBar.get() == "" and self.SearchBar.get().lower() in mod.name.lower()):
                        self.Modlist.insert(tk.END, mod)
                        self.Modlist.itemconfig(tk.END, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
                    elif(self.SearchBar.get() == ""):
                        self.Modlist.insert(tk.END, mod)
                        self.Modlist.itemconfig(tk.END, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
        else:
            self.mods.sort(key=lambda x: x.compatibility)
            for mod in self.mods:
                if(not mod.loaded):
                    if(not self.SearchBar.get() == "" and self.SearchBar.get().lower() in mod.name.lower()):
                        self.Modlist.insert(0, mod)
                        self.Modlist.itemconfig(0, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
                    elif(self.SearchBar.get() == ""):
                        self.Modlist.insert(0, mod)
                        self.Modlist.itemconfig(0, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
    
    def updateActiveModList(self):
        self.ActiveModlist.delete(0, tk.END)
        if(self.alphabeticSort):
            self.mods.sort(key=lambda x: x.name)
            for mod in self.mods:
                if(mod.loaded):
                    if(not self.SearchBar.get() == "" and self.SearchBar.get().lower() in mod.name.lower()):
                        self.ActiveModlist.insert(tk.END, mod)
                        self.ActiveModlist.itemconfig(tk.END, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
                    elif(self.SearchBar.get() == ""):
                        self.ActiveModlist.insert(tk.END, mod)
                        self.ActiveModlist.itemconfig(tk.END, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
        else:
            self.mods.sort(key=lambda x: x.compatibility)
            for mod in self.mods:
                if(mod.loaded):
                    if(not self.SearchBar.get() == "" and self.SearchBar.get().lower() in mod.name.lower()):
                        self.ActiveModlist.insert(0, mod)
                        self.ActiveModlist.itemconfig(0, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
                    elif(self.SearchBar.get() == ""):
                        self.ActiveModlist.insert(0, mod)
                        self.ActiveModlist.itemconfig(0, bg="red" if mod.compatibility == 1 else "orange" if mod.compatibility == 2 else "yellow" if mod.compatibility == 3 else "green" if mod.compatibility == 4 else "gray")
    
    def filter(self,e):
        self.updateAllModList()
        self.updateActiveModList()
        
        
        



__imit__ = modGUI()
