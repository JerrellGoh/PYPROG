import Adafruit_DHT
from time import sleep

sensor = Adafruit_DHT.AM2302
pin = 4 #GPIO 4 or pin 7

while(True):
    # This read_retry method tries up to 15 times to get a sensor reading,
    # 2-second wait between retries.
    ____________________________________________________________ #read humidity & temperature

    # Sometimes, you won't get a reading and results will be null.
    # Linux can't guarantee the timing of calls to read the sensor.
    if humidity is not None and temperature is not None:
        __________________________________________________________________________ # print results on screen
        # Refer to https://docs.python.org/3/library/string.html#string-formatting
        # (esp.ly "6.1.3.2 Format examples") for more info
    else:
        print('Failed to get reading. Try again!')
    sleep(2)



    
