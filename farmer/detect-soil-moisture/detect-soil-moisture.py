import json
import time
from os import path
import csv
from datetime import datetime
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.adc import ADC
import paho.mqtt.client as mqtt

# Khởi tạo kết nối với CounterFit trên địa chỉ và cổng đúng
CounterFitConnection.init('127.0.0.1', 5000)


adc = ADC()

id = '<ID>'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'moisture_sensor_server'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()
print("MQTT connected!")

moisture_file_name = 'moisture.csv'
fieldnames = ['moisture']

if not path.exists(moisture_file_name):
    with open(moisture_file_name, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    with open(moisture_file_name, mode='a') as moisture_file:        
        moisture_writer = csv.DictWriter(moisture_file, fieldnames=fieldnames)
        moisture_writer.writerow({'moisture' : payload['moisture']})

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    soil_moisture = adc.read(0)
    
    telemetry = json.dumps({'moisture' : soil_moisture})
    print("Sending telemetry ", telemetry)

    mqtt_client.publish(client_telemetry_topic, telemetry)
    time.sleep(1)