import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(27,GPIO.OUT)
___________________ #PWM output at GPIO27, frequency is 50Hz
while(True):
    for x in range (0,101,20):
        ____________
        sleep(1)

