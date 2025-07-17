from sample_code import I2C_LCD_driver as LCD , keypad as keypad
import queue
import RPi.GPIO as GPIO
from time import sleep
from threading import Thread

shared_keypad_queue = queue.Queue()

def key_pressed(key):
    shared_keypad_queue.put(key)


def Lcd_display_On():
    lcd = LCD.lcd()  # Instantiate an LCD object
    lcd.lcd_clear()              # Clear the display
    lcd.lcd_display_string("LCD ON", 1)  # Display message on line 1
    lcd.lcd_display_string("Press any key", 2)  # Display message on line 2
    sleep(2)                     # Wait for 2 seconds before next update

def Lcd_display_Off():
    lcd = LCD.lcd()  # Instantiate an LCD object
    lcd.lcd_clear()              # Clear the display
    lcd.backlight(0)             # Turn off the backlight
    sleep(2)                     # Wait for 2 seconds before next update
    
def main():
    lcd = LCD.lcd()
    lcd.lcd_clear()

    keypad.init(key_pressed)
    Thread(target=keypad.get_key, daemon=True).start()  # Add daemon=True

    while True:
        key = shared_keypad_queue.get()

        if key == '1':
            Lcd_display_On()  # Example action for key '1'
        elif key == '2':
            Lcd_display_Off()



if __name__ == "__main__":
    main()

