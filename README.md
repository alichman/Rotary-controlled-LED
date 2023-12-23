# Rotary-controlled-LED
A package that uses an i2c display and rotary encoder to control WS2812B LEDs.

This project uses the micropython _thread library to ensure smooth input that is unaffected by the relatively slow proccess of writing LED values. 
Due to the implementation of multithreading on the RP2040 being far from perfect, interrupts don't work consistently enough to be used for input.
The Rotary Encoder is instead handled with a constant loop.

This project was developed using the YD-RP2040 board, and by default uses the built-in LED on pin 23 for its output.
It also uses the user button on pin 24 as an in-program kill switch, as I've run into some issues with _thread, where
the second thread doesn't halt no matter what. If you are not using the YD-RP2040, I recommend replacing the kill switch
with your own button, or removing the section in main labeled " User button used as kill switch..." at the bottom.
