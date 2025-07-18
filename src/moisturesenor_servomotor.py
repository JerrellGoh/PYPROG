from sample_code import moisturesensor as ms, servomotor as servo
from time import sleep
import RPi.GPIO as GPIO

def moisture_sensor():
    while True:
        moisture_level = moisture_sensor.read_moisture()
        if moisture_level:
            print('Moisture detected')
        else:
            print('No moisture detected')
        sleep(0.5)  # Adjust the frequency of moisture checks as needed

def servo_control_On():# Move servo to 0 degrees, then to 90 degrees
    servo.move_to_position(0)
    sleep(1)
    servo.move_to_position(90)
    sleep(1)

def servo_control_Off():# Move servo to 90 degrees, then to 0 degrees
    servo.move_to_position(90)
    sleep(1)
    servo.move_to_position(0)
    sleep(1)

def main():
    servo.init()  # Initialize the servo
    ms.init()   # Initialize the moisture sensor 
    while True:
        moisture_level = ms.read_sensor()
        if moisture_level:
            print('Moisture detected')
            servo_control_On()
            sleep(5)
            servo_control_Off()
        else:
            print('No moisture detected')
        sleep(0.5)  # Adjust the frequency of moisture checks as needed

if __name__ == "__main__":
    main()

