import RPi.GPIO as GPIO
from sample_code import dht11
from sample_code import I2C_LCD_driver
from sample_code import keypad as keypad
from sample_code import servo as servo
from time import sleep
import Adafruit_DHT

sensor = Adafruit_DHT.AM2302  # Sensor type (AM2302/DHT22)
pin = 4                       # GPIO pin where sensor is connected


def Lcd_display_On(temperature, humidity):
    lcd = I2C_LCD_driver.lcd()  # Instantiate an LCD object
    lcd.lcd_clear()              # Clear the display
    lcd.lcd_display_string("Temp: {:.1f}C".format(temperature), 1)  # Display temperature on line 1
    lcd.lcd_display_string("Humidity: {:.1f}%".format(humidity), 2)  # Display humidity on line 2
    sleep(2)                     # Wait for 2 seconds before next update

def Lcd_display_Off():
    lcd = I2C_LCD_driver.lcd()  # Instantiate an LCD object
    lcd.lcd_clear()              # Clear the display
    lcd.backlight(0)             # Turn off the backlight
    sleep(2)                     # Wait for 2 seconds before next update

def read_dht_sensor():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        # read_retry tries 15 times (with 2-sec delays) to get valid data

        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}°C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        
        sleep(2)  # Wait 2 seconds between readings

def keypad_listener():
    def key_press_callback(key):
        print("Key pressed:", key)
        if key == '1':
            Lcd_display_On(humidity, temperature)  # Example action for key '1'
        elif key == '2':
            Lcd_display_Off  # Example action for key '2'
        # Add more actions for other keys as needed

    keypad.init(key_press_callback)  # Initialize keypad with the callback
    while True:
        keypad.get_key()  # Continuously check for key presses

def servo_control():
    servo.init()  # Initialize the servo
    while True:
        # Example: Move servo to 0 degrees, then to 90 degrees
        servo.move_to_position(0)
        sleep(1)
        servo.move_to_position(90)
        sleep(1)