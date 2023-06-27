import tkinter as tk
from library import *
from paths import *
import modList

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
        self.listFrame.rowconfigure(0, weight=1)
        self.listFrame.columnconfigure(0, weight=1)
        self.listFrame.columnconfigure(1, weight=1)
        self.listFrame.grid(row=1, column=0,sticky="nsew")

        unloadedModlist = modList.ModList(False,self.listFrame)
        unloadedModlist.grid(row=0, column=0,sticky="nsew")

        loadedModlist = modList.ModList(True,self.listFrame)
        loadedModlist.grid(row=0, column=1,sticky="nsew")
        

        self.root.mainloop()   

        
__imit__ = modGUI()
