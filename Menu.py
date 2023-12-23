class menu:
    
    def __init__(self, Name:str, OG = None, Loop:bool = False):
        self.name = Name
        self.origin = OG
        self.items = []
        self.loopScroll = Loop
        
    
    def addItem(self, item:menu_item):
        self.items.append(item)
        
    def clickItem(self, num:int):
        self.items[num].click()
        
    def getName(self):
        return self.name
    
    def getStrings(self):
        return [obj.getStr() for obj in self.items]


class menu_item:
    
    def __init__(self, name:str, func):
        self.text = name
        self.action = func
        
    def getStr(self):
        return self.text
    
    def click(self):
        (self.action)()
    
    
