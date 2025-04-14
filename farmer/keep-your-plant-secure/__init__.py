import logging
import json
from azure.iot.device import IoTHubDeviceClient, MethodRequest

connection_string = "<YOUR_DEVICE_CONNECTION_STRING>"

def main(event: str):
    logging.info("Telemetry received: %s", event)
    data = json.loads(event)
    soil_moisture = data.get("soil_moisture", 0)

    device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
    device_client.connect()

    # Logic to control actuator based on sensor data
    if soil_moisture < 0.5:
        method = MethodRequest.create_from_name("relay_on", "GET")
        logging.info("Soil dry: turning relay ON.")
    else:
        method = MethodRequest.create_from_name("relay_off", "GET")
        logging.info("Soil wet: turning relay OFF.")

    device_client.send_method_request(method)
    device_client.disconnect()
