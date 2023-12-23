from machine import Pin
import Menu, display, LED_Modes
from neopixel import NeoPixel
import utime
import _thread

# Initialize display
Screen = display.display(16, 17)

# Home constants
baseHue = 0
Value = 0.1
isHome = True
currentMode = "Test"

Screen.update_home(Value, baseHue, currentMode)

# Add a menu
main_menu = Menu.menu("Modes", OG=-1, Loop=True)

# Make menu items
temp = Menu.menu_item("Northern Lights", lambda: setLedMode(LED_Modes.NorthLights))
main_menu.addItem(temp)

temp = Menu.menu_item("Stable Hue", lambda: setLedMode(LED_Modes.StableHue))
main_menu.addItem(temp)

temp = Menu.menu_item("Off", lambda: setLedMode(None))
main_menu.addItem(temp)

# LED setup

LED_Modes.setMode(LED_Modes.NorthLights)
print(LED_Modes.getMode())
uBut = Pin(24, Pin.IN, Pin.PULL_UP)

LED_THREAD = _thread.start_new_thread(LED_Modes.Runner, ())

# Encoder and update defs

def updateValues():
    global Value, baseHue, Screen
    LED_Modes.setVal(Value)
    LED_Modes.setHue(baseHue)
    if isHome: Screen.update_home(Value,baseHue,currentMode)
    else: Screen.update()
    
def setLedMode(func):
    global currentMode
    LED_Modes.setMode(func)
    currentMode = LED_Modes.getMode()
    
# Encoder pins

en_clk = Pin(18, Pin.IN, Pin.PULL_UP)
en_dt = Pin(19, Pin.IN, Pin.PULL_UP)
en_sw = Pin(20, Pin.IN, Pin.PULL_UP)


oldVals = [1, 1]
pressLength = 0
doAct = False
while True:
    # Handle button press
    if not en_sw.value():
        print(pressLength)
        # If press is new
        if not pressLength:
            print("pressed")
            # Enable button action on release,
            # start recording press time.
            doAct = True
            pressLength = utime.ticks_ms()
    else:
        # On release, if action not canceled.
        
        if pressLength != 0 and doAct:
            print("released")
            # Record the press time
            pressLength = utime.ticks_ms()-pressLength
            # If it's a click
            if pressLength < 500:
                # When home, open menu
                if isHome:
                    Screen.setMenu(main_menu)
                    isHome = False
                # If in menu, click.
                else: Screen.click()
            # If its a hold
            else:
                # If home, run save current data as default
                if isHome: pass
                # Else, go back to previous menu or home
                else:
                    isHome = Screen.back()
                    updateValues()
        pressLength = 0
        doAct = False
            
    
    # Handle encoder control
    A_val = en_clk.value()
    B_val = en_dt.value()
    
    # If a change is registered
    newVals = [A_val, B_val]
    if newVals != oldVals:
        # An event has occured
        print(newVals)
        
        # If encoder at stable position
        if newVals == [1,1]:
            # If spun clockwise
            if oldVals == [1,0]:
                # If home, change value and hue
                if isHome:
                    if en_sw.value():
                        Value += 0.05
                        if Value > 1: Value = 1
                    else:
                        baseHue = (baseHue+5)%360
                # If in menu, scroll
                else: Screen.scroll(1)
                    
            # If spun counterclockwise
            elif oldVals == [0,1]:
                # Same layout as clockwise
                if isHome:
                    if en_sw.value():
                        Value -= 0.05
                        if Value < 0: Value = 0
                    else:
                        baseHue = (baseHue+355)%360
                else:
                    Screen.scroll(-1)
            doAct = False
            updateValues()
        oldVals = newVals
        
    # User button used as kill switch for
    # both threads to exit gracefuly.
    if not uBut.value():
        LED_Modes.forceEnd()
        break
    utime.sleep_ms(1)
