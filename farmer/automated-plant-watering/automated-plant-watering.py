import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
import paho.mqtt.client as mqtt

# Khởi tạo kết nối với CounterFit trên địa chỉ và cổng đúng
CounterFitConnection.init('127.0.0.1', 5000)


adc = ADC()
relay = GroveRelay(5)

id = '<ID>'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'moisture_sensor_server'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()
print("MQTT connected!")

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    soil_moisture = adc.read(0)
    
    print("Soil moisture: ", soil_moisture)
    if soil_moisture > 450:
        print("Soil moisture is too low, turning relay on.")
        relay.on()
    else:
        print("Soil moisture is ok, turning relay off.")
        relay.off()

    time.sleep(1)