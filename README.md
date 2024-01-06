# Rotary-controlled-LED
A package that uses an i2c display and rotary encoder to control WS2812B LEDs.

This project uses the micropython _thread library to ensure smooth input that is unaffected by the relatively slow proccess of writing LED values. 
Due to the implementation of multithreading on the RP2040 being far from perfect, interrupts don't work consistently enough to be used for input.
The Rotary Encoder is instead handled with a constant loop.

This project was developed using the YD-RP2040 board, and by default uses the built-in LED on pin 23 for its output.
It also uses the user button on pin 24 as an in-program kill switch, as I've run into some issues with _thread, where
the second thread doesn't halt no matter what. If you are not using the YD-RP2040, I recommend replacing the kill switch
with your own button, or removing the section in main labeled " User button used as kill switch..." at the bottom.

# Planned Rework
* Mode-saver will be implemented in the next update.
* Depending on the saving method, the lighting modes may be reworked into a class-based solution.
* Once the physical device is tested, example videos and STL files may be uploaded.
* A text scroll feature may be implemented, but for now text that is too long will overflow off the side.


# main.py
The main file contains initialization for other files, launches the second thread, and runs the rotary encoder loop.


# display.py
The display file contains the display class.

Constants:
    * text_buffer: The buffer between the text and the top of its bar
    * left_buffer: The buffer between the text and the left side of the screen
    * bar_height: The height of each text bar
    * num_items_per_page: Number of items shown at once in a menu.
        Should typically be around (Screen Height / bar_height) - 1
    
Initialization:
    * Sda: int value of SDA pin
    * Scl: int value of SCL pin
    * i2cType: int value of I2C type. 0 or 1 for the RP2040
    
setMenu:
    Set a menu to display. Automatically updates the display.
    * newMenu: pre-defined menu object
    
update:
    Writes current menu onto the screen, and highlights current selection.
    
scroll:
    Shifts current selection.
    * dir: int value, 1=scroll down, -1=scroll up
    
click:
    Executes lambda method linked to current selection.
    
back:
    Returns either to the menu's origin, or to the home page if in the main menu.
    
update_home:
    Writes home screen to display
    * val: int value for brightness
    * hue: int value for hue
    * mode: str value for current mode name


#Menu.py
The menu file contains the menu and menu_item objects.
    
Menu initialization:
    * Name: str value for menu name
    * OG: Menu of origin, None if main menu.
    * Loop: bool value for whether the selector loops around or sticks to the ends of the menu. Default False.
    
addItem:
    Adds menu_item to menu
    * item: menu_item to add
    
clickItem:
    Wrapper for executing item function
    * num: int index of menu item to execute
    
getName:
    Returns menu name
    
getStrings:
    Returns a list of all item names
    
menu_item initialization:
    * name: string name
    * func: lambda function to execute
    
getStr:
    Returns item name
    
Click:
    executes lambda function


# LED_Modes.py
The LED_Modes file handles the LED writing, and contains the different modes for the LEDs.
The current implementation is not final, and is subject to major changes in the coming updates.
I have chosen against documenting the individual modes. Any function can be used as long as it takes an integer value as input and returns an integer value. Each mode handles its own iteration by reseting and returning the counter as needed.

setMode:
    Sets function to be executed by the runner
    * func: function to execute.
    
setVal:
    Sets max brightness
    * newVal: int value for brightness.
    
setHue:
    Sets base hue
    * newHue: int value for hue.
    
forceEnd:
    breaks out of runner and allows for thread to be termintated in main
    
getMode:
    Returns current mode's name
    
Runner:
    Runs on second thread. While off, the program checks every 500 ms for updates.
    Executes current mode every 10 ms
