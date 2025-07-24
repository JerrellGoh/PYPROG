import Adafruit_DHT
import time
import csv

sensor = Adafruit_DHT.AM2302
pin = 4 #GPIO 4 or pin 7
n = 0

while(True):
    # This read_retry method tries up to 15 times to get a sensor reading,
    # 2-second wait between retries.
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Sometimes, you won't get a reading and results will be null.
    # Linux can't guarantee the timing of calls to read the sensor.
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        # Refer to https://docs.python.org/3/library/string.html#string-formatting
        # (esp.ly "6.1.3.2 Format examples") for more info

        # Compute n (row number), sample time & date, and compose a row of data
        n = n + 1
        Ntime = time.strftime("%H")+':'+time.strftime("%M")+':'+time.strftime("%S")
        Ndate = time.strftime("%d")+'-'+time.strftime("%m")+'-'+time.strftime("%Y")
        ____________________________________________________________ #prepare a row of data

        # Open csv file and append the row of data
        with open('sensordata.txt','a') as csvfile:
            datafile = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            __________________________ #write data to file

    else:
        print('Failed to get reading. Try again!')
    time.sleep(2)



    
