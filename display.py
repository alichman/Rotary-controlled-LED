from machine import Pin, I2C
import framebuf
import Menu
from ssd1306 import SSD1306_I2C

# Init display object
# using default address 0x3C
class display:
    text_buffer = 4    
    left_buffer = 5
    bar_height = 15
    num_items_per_page = 3
    
    def __init__(self, Sda:int, Scl:int, i2cType: int):
        i2c = I2C(0, sda=Pin(Sda), scl=Pin(Scl))
        self.screen = SSD1306_I2C(128, 64, i2c)
        self.cMenu = None
        self.cMenuStrings = []
        self.pos = 0
        self.offset = 0
    
    def setMenu(self, newMenu:menu):
        self.cMenu = newMenu
        self.cMenuStrings = self.cMenu.getStrings()
        self.update()
        
    def update(self):
        # Clear and print title
        self.screen.fill(0)
        self.screen.fill_rect(0, 0, 128, self.bar_height, 1)
        self.screen.text(self.cMenu.getName(), self.left_buffer, self.text_buffer, 0)
        # Loop through items until screen limit or end of items
        i=0
        while i<self.num_items_per_page and i<len(self.cMenuStrings) - self.offset:
            y = (i+1)*self.bar_height
            
            # If at selected item, highlight and write inverted.
            if i == self.pos:
                self.screen.fill_rect(0, y, 128, self.bar_height, 1)
                self.screen.text(self.cMenuStrings[i+self.offset], self.left_buffer, y+self.text_buffer, 0)
            # Else, write normally.
            else: self.screen.text(self.cMenuStrings[i+self.offset], self.left_buffer, y+self.text_buffer, 1)
            # Iterate
            i += 1
        
        self.screen.show()
        
    def scroll(self, dir:int):
        # dir 1: down, -1 up
        
        if dir == 1 and self.pos == 2:
            if not self.pos + self.offset + 1 == len(self.cMenuStrings):
                self.offset += 1
        # If pushing top
        elif dir == -1 and self.pos == 0:
            if not self.pos + self.offset == 0:
                self.offset -= 1
        else:
            self.pos += dir
        self.update()
        
    def click(self):
        # If back button is pressed
        if self.offset + self.pos + 1 == len(self.cMenuStrings):
            if self.cMenu.origin == -1:
                # If in main menu
                self.cMenu = None
                return True
            else:
                self.cMenu = self.cMenu.origin
                self.update()
            
        else:
            self.cMenu.clickItem(self.offset + self.pos)
        
        return False
    
    def back(self):
        if self.cMenu.origin == -1:
            # If in main menu
            self.cMenu = None
            return True
        # Else, go to previous menu
        self.cMenu = self.cMenu.origin
        self.update()
        return False
            
    def update_home(self, val:int, hue:int, mode:str):
        #Clear
        self.screen.fill(0)
        # Mode title
        self.screen.fill_rect(0, 0, 128, self.bar_height, 1)
        self.screen.text("Mode: " + mode, self.left_buffer, self.text_buffer, 0)
        # Brightness
        self.screen.text("Brightness: ", self.left_buffer, self.text_buffer + self.bar_height, 1)
        self.screen.text(str(int(val*100)) + "%\t\t" + str(hue), self.left_buffer, self.text_buffer + self.bar_height * 2, 1)
        self.screen.text("\t\tBase Hue: ", self.left_buffer, self.text_buffer + self.bar_height*3, 1)
        
        self.screen.show()



