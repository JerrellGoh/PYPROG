import queue
import RPi.GPIO as GPIO 
from time import sleep
from threading import Thread
from IoTe import I2C_LCD_driver as lcd

def keypad_call(key):

    MATRIX=[ [1,2,3],
         [4,5,6],
         [7,8,9],
         ['*',0,'#']] #layout of keys on keypad
    ROW=[6,20,19,13] #row pins
    COL=[12,5,16] #column pins

    #set column pins as outputs, and write default value of 1 to each
    for i in range(3):
        GPIO.setup(COL[i],GPIO.OUT)
        GPIO.output(COL[i],1)

    #set row pins as inputs, with pull up
    for j in range(4):
        GPIO.setup(ROW[j],GPIO.IN,pull_up_down=GPIO.PUD_UP)

    #scan keypad
    while (True):
        for i in range(3): #loop thru’ all columns
            GPIO.output(COL[i],0) #pull one column pin low
            for j in range(4): #check which row pin becomes low
                if GPIO.input(ROW[j])==0: #if a key is pressed
                    print (MATRIX[j][i]) #print the key pressed
                    key = MATRIX[j][i]
                    while GPIO.input(ROW[j])==0: #debounce
                        sleep(0.1)
                        return key 
            GPIO.output(COL[i],1) #write back default value of 1

def main():
    keypad_call()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Initialize LCD
    LCD = lcd.lcd()
    sleep(0.5)
    LCD.backlight(0)  # turn backlight off
    sleep(0.5)
    LCD.backlight(1)  # turn backlight on
    
    while True:
        key = keypad_call()
        if key is not None:
            LCD.lcd_clear()
            LCD.lcd_display_string("Pressed:", 1)
            LCD.lcd_display_string(str(key), 2)
            sleep(0.1)
    