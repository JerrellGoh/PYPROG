from IoTe import I2C_LCD_driver as lcd 
from time import sleep 
import RPi.GPIO as GPIO
from hal import hal_keypad as keypad
import queue
from threading import Thread

shared_keypad_queue = queue.Queue()

# Keypad callback function (missing in original)
def key_pressed(key):
    shared_keypad_queue.put(key)

def main():
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Initialize LCD
    LCD = lcd.lcd()
    sleep(0.5)
    LCD.backlight(0) # turn backlight off
    sleep(0.5)
    LCD.backlight(1) # turn backlight on
    
    # Initialize keypad with callback
    keypad.init(key_pressed)
    
    # Start keypad thread (missing in original)
    Thread(target=keypad.get_key, daemon=True).start()

    try:
        while True:
            if not shared_keypad_queue.empty():
                key = shared_keypad_queue.get()
                
                LCD.lcd_clear()
                LCD.lcd_display_string("Pressed:", 1)
                LCD.lcd_display_string(str(key), 2)  # Convert key to string
                
                # Don't return here unless you want to exit
                # return key  # This would exit the function immediately
                
            sleep(0.1)
            
    except KeyboardInterrupt:
        LCD.lcd_clear()
        LCD.backlight(0)
        GPIO.cleanup()

if __name__ == "__main__":
    main()