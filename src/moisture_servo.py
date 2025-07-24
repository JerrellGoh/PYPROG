import RPi.GPIO as GPIO #import RPi.GPIO module
from time import sleep

GPIO.setmode(GPIO.BCM) #choose BCM mode
GPIO.setwarnings(False)
GPIO.setup(26,GPIO.OUT) #set GPIO 26 as output
GPIO.setup(4,GPIO.IN) #set GPIO 4 as input

PWM=GPIO.PWM(26,50) #set 50Hz PWM output at GPIO26

def servo_control_clockwise():
        PWM.start(3) #3% duty cycle
        print('duty cycle:', 3)
        sleep(4) #allow time for movement
        PWM.start(12) #13% duty cycle
        print('duty cycle:', 9)
        sleep(4) #allow time for movement

def servo_control_anticlockwise():
        PWM.start(12) #13% duty cycle
        print('duty cycle:', 9)
        sleep(4) #allow time for movement
        PWM.start(3) #3% duty cycle
        print('duty cycle:', 3)
        sleep(4) #allow time for movement
        
def main():
    valve = False

    try:
        while (True):
            if GPIO.input(4) and not valve: #if read a high at GPIO 4, moisture present
                print('detected HIGH i.e. moisture')
            elif not GPIO.input(4): #otherwise (i.e. read a low) at GPIO 4, no moisture
                print('detected LOW i.e. no moisture')
                servo_control_clockwise()
                valve = True
            elif GPIO.input(4) and valve:
                print("Moisture detected, closing valve")
                servo_control_anticlockwise()
                valve = False
            sleep(0.5) # to limit print() frequency
    except KeyboardInterrupt:
        print("Exiting...")
        

