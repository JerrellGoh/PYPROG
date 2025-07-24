import RPi.GPIO as GPIO
import dht11
import time
import csv
import datetime
import requests

# GPIO setup
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# Sensor configuration
instance = dht11.DHT11(pin=21)  # Read data using pin 21

# ThingSpeak API configuration
THINGSPEAK_API_KEY = "SFUJ600ET56E08EE"

# Function to send data to ThingSpeak
def send_to_thingspeak(temperature, humidity):
    try:
        response = requests.get(
            "https://api.thingspeak.com/update",
            params={
                "api_key": THINGSPEAK_API_KEY,
                "field2": temperature,
                "field3": humidity
            }
        )
        if response.status_code == 200:
            print("Data uploaded successfully: Temp={}C, Humidity={}%".format(temperature, humidity))
        else:
            print("Failed to upload data. Status code: {}.".format(response.status_code))
    except requests.RequestException as e:
        print("Error occurred while uploading data: {}.".format(e))

# Function to collect temperature and humidity data
def collect_and_send_data():
    try:
        while True:
            result = instance.read()
            if result.is_valid():
                temperature = result.temperature
                humidity = result.humidity

                # Print sensor data
                print("Last valid input: {}".format(datetime.datetime.now()))
                print("Temperature: {:.1f} C".format(temperature))
                print("Humidity: {:.1f} %".format(humidity))

                # Write to CSV
                n_time = time.strftime("%H:%M:%S")
                n_date = time.strftime("%d/%m/%Y")
                data_row = ["{:.1f}".format(temperature), "{:.1f}".format(humidity), n_time, n_date]
                with open('sensordata.csv', 'a', newline='') as file_handle:
                    data_file = csv.writer(file_handle, delimiter=',', lineterminator='\n')
                    data_file.writerow(data_row)

                # Send to ThingSpeak
                send_to_thingspeak("{:.1f}".format(temperature), "{:.1f}".format(humidity))
            else:
                print("Failed to get reading. Trying again!")
            time.sleep(0.5)  # Short delay between reads
    except KeyboardInterrupt:
        print("Cleanup")
        GPIO.cleanup()

if __name__ == "__main__":
    collect_and_send_data()

        


