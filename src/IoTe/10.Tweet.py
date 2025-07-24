import RPi.GPIO as GPIO
from time import sleep
import Adafruit_DHT
import requests #see http://docs.python-requests.org/en/master for more details

sensor = Adafruit_DHT.AM2302
pin = 4 #GPIO 4 or pin 7
myUploadAPI = "___________________________" #modify this to yours
baseURL = 'https://api.thingspeak.com/update?api_key=%s' %myUploadAPI

myThingTweetAPI = "___________________________" #modify this to yours

while(True):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        resp = requests.get(baseURL + "&field1=%s&field2=%s" %(humidity,temperature)) #upload to Thingspeak
        if (humidity > 70):
          resp = requests.post('https://api.thingspeak.com/apps/thingtweet/1/statuses/update',
                    json={'api_key':myThingTweetAPI,'status':'Humidity exceeds 70%!'})
    else:
        print('Failed to get reading. Try again!')
    sleep(15) #limit to upload rate, for free channel 



    
