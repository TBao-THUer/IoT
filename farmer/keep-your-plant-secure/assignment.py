from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
import time
import json

# Connect to CounterFit
CounterFitConnection.init('127.0.0.1', 5000)

# Initialize sensor and actuator
adc = ADC()
relay = GroveRelay(5)

# IoT Hub device connection string
connection_string = "<YOUR_DEVICE_CONNECTION_STRING>"
device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

# Connect the device client
print("Connecting to IoT Hub...")
device_client.connect()
print("Connected.")

# Method handler for cloud-to-device messages
def handle_method_request(request):
    print("Received method:", request.name)
    if request.name == "relay_on":
        relay.on()
    elif request.name == "relay_off":
        relay.off()
    device_client.send_method_response(MethodResponse.create_from_method_request(request, 200))

device_client.on_method_request_received = handle_method_request

# Telemetry loop
while True:
    soil_moisture = adc.read(0)
    print(f"Soil Moisture: {soil_moisture}")
    msg = Message(json.dumps({"soil_moisture": soil_moisture}))
    device_client.send_message(msg)
    time.sleep(10)
