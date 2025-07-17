import RPi.GPIO as GPIO
from sample_code import I2C_LCD_driver as LCD, keypad as keypad, servo as servo, moisturesensor as moisture_sensor
from threading import Thread, Event
from time import sleep, strftime
import Adafruit_DHT
import atexit

class SmartGardenSystem:
    def __init__(self):
        # Hardware configuration
        self.dht_sensor = Adafruit_DHT.DHT11
        self.dht_pin = 4
        self.led_pin = 18
        
        # System state
        self.temperature = None
        self.humidity = None
        self.moisture = None
        self.led_state = False  # REQ_02: Default LED off
        self.lcd = LCD.lcd()
        self.lcd_on = True  # REQ_01: Default LCD on
        
        # Control flags
        self.running = Event()
        self.running.set()
        
        # Initialize hardware
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.LOW)  # Ensure LED starts off
        moisture_sensor.init()
        servo.init()
        
        # Register cleanup
        atexit.register(self.cleanup)

    def start(self):
        """Start all system threads"""
        threads = [
            Thread(target=self.clock_display),  # REQ_01
            Thread(target=self.dht_monitor),
            Thread(target=self.keypad_handler),
            Thread(target=self.moisture_monitor)  # REQ_05
        ]
        
        for t in threads:
            t.daemon = True
            t.start()

    def clock_display(self):
        """REQ_01: Display current time on LCD"""
        while self.running.is_set():
            if self.lcd_on:
                current_time = strftime("%H:%M:%S")
                current_date = strftime("%d/%m/%Y")
                self.lcd.lcd_display_string(f"Time: {current_time}", 1)
                self.lcd.lcd_display_string(f"Date: {current_date}", 2)
            sleep(1)

    def dht_monitor(self):
        """Monitor temperature and humidity"""
        while self.running.is_set():
            humidity, temperature = Adafruit_DHT.read_retry(self.dht_sensor, self.dht_pin)
            if humidity is not None and temperature is not None:
                self.temperature = temperature
                self.humidity = humidity
            sleep(2)

    def keypad_handler(self):
        """Handle keypad input"""
        def callback(key):
            if key == '1':  # REQ_03
                self.display_climate_data()
            elif key == '0':  # REQ_04
                self.toggle_led()
        
        keypad.init(callback)
        while self.running.is_set():
            keypad.get_key()
            sleep(0.1)

    def moisture_monitor(self):
        """REQ_05: Control servo based on moisture"""
        while self.running.is_set():
            self.moisture = moisture_sensor.read_moisture()
            if not self.moisture:  # If no moisture detected
                servo.move_to_position(90)  # Turn 90° clockwise
                sleep(5)  # Hold for 5 seconds
                servo.move_to_position(0)  # Return to original position
            sleep(10)  # Check moisture every 10 seconds

    def display_climate_data(self):
        """REQ_03: Display climate data on LCD"""
        if self.temperature is not None:
            self.lcd.lcd_clear()
            self.lcd.lcd_display_string(f"Temp: {self.temperature:.1f}C", 1)
            self.lcd.lcd_display_string(f"Humidity: {self.humidity:.1f}%", 2)
            sleep(5)  # Display for 5 seconds
            self.lcd.lcd_clear()

    def toggle_led(self):
        """REQ_04: Toggle LED state"""
        self.led_state = not self.led_state
        GPIO.output(self.led_pin, self.led_state)
        print(f"LED turned {'ON' if self.led_state else 'OFF'}")

    def cleanup(self):
        """Clean up resources"""
        self.running.clear()
        self.lcd.lcd_clear()
        self.lcd.backlight(0)
        servo.move_to_position(0)  # Reset servo
        GPIO.output(self.led_pin, GPIO.LOW)
        GPIO.cleanup()
        print("System shutdown complete")

if __name__ == "__main__":
    system = SmartGardenSystem()
    try:
        system.start()
        print("Smart Garden System running. Press CTRL+C to exit.")
        while True:
            sleep(1)
    except KeyboardInterrupt:
        system.cleanup()