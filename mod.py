class Mod(object):
    def __init__(self,name, packageId, id):
        self.name = name
        self.id = id
        self.packageId = packageId
        self.loaded = False
        self.compatibility = 0

    def __str__(self):
        return str(self.compatibility) + " | " + self.name
    
    def __rtr__(self):
        return self.compatibility + " | " + self.name + "|" + self.packageId + "|" + self.id 