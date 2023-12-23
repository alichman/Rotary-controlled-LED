from machine import Pin
from neopixel import NeoPixel
import utime, math
import _thread

numLeds = 1
strip = NeoPixel(Pin(23),numLeds)

Current_Mode = None
Brightness = 0.1
Base_Hue = 0
doRun = True


def hsv_to_rgb(h, s, v):
    """
    Convert HSV (Hue, Saturation, Value) to RGB (Red, Green, Blue).

    Parameters:
        h (float): Hue, a value between 0 and 360.
        s (float): Saturation, a value between 0 and 1.
        v (float): Value, a value between 0 and 1.

    Returns:
        tuple: RGB values as integers in the range 0-255.
    """
    h /= 360.0

    i = int(h * 6)
    f = (h * 6) - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    if i % 6 == 0:
        return int(v * 255), int(t * 255), int(p * 255)
    elif i % 6 == 1:
        return int(q * 255), int(v * 255), int(p * 255)
    elif i % 6 == 2:
        return int(p * 255), int(v * 255), int(t * 255)
    elif i % 6 == 3:
        return int(p * 255), int(q * 255), int(v * 255)
    elif i % 6 == 4:
        return int(t * 255), int(p * 255), int(v * 255)
    else:
        return int(v * 255), int(p * 255), int(q * 255)
 

# Independent Hue
def NorthLights(num: int):
    sine_phase = 500
    val = Brightness
    num = num % sine_phase
    
    for i in range(numLeds):
        # Calculate Hue
        hue = (num*1.0/sine_phase *360 + i*5)%360            
        # Calculate Brightness
        bright = val - (math.sin(sine_phase-num - i*4)*3.14159/sine_phase +1)*val/3.0
        # Write
        strip[i] = hsv_to_rgb(hue, 0.7, bright)
    
    return num
        
# Doesn't need iterator
def StableHue(num):
    strip.fill(hsv_to_rgb(Base_Hue, 1, Brightness))
    return 0


Mode_Dict = {NorthLights: "Aurora",
             StableHue: "Stable",
             None: "Off"}



# Setter and Getter methods
def setMode(func):
    global Current_Mode
    Current_Mode = func
    
def setVal(newVal:float):
    global Brightness
    
    if newVal < 0: newVal = 0
    if newVal > 1: newVal = 1
    
    Brightness = newVal

def setHue(newHue:int):
    global Base_Hue
    Base_Hue = (360 + Base_Hue)%360
    Base_Hue = newHue
    
def forceEnd():
    global doRun, strip
    doRun = False
    strip.fill((0,0,0))
    strip.write()
    

def getMode():
    return Mode_Dict[Current_Mode]
    

# Run LED loop on second thread
def Runner():
    x=0
    
    while(doRun):
        
        # While LED mode is set to off, wait.
        while Current_Mode is None:
            strip.fill((0,0,0))
            strip.write()
            utime.sleep_ms(500)
            
            
        # Call current mode and iterate
        x = 1 + Current_Mode(x)
        # Show on Strip
        strip.write()
        utime.sleep_ms(10)
