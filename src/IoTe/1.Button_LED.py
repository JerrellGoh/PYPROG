import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(27,GPIO.OUT)
_______________________ #make pin 19 an input pin
while(True):
    if GPIO.input(19):
        print("button is pushed")
        GPIO.output(27,1)
    else:
        print("button is released")
        _________________ #turn LED off
    sleep(0.5)
