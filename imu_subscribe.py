import paho.mqtt.client as mqtt
from pylimo import limo
import argparse
import json

limo=limo.LIMO()
limo.EnableCommand()

parser = argparse.ArgumentParser()
parser.add_argument('--ip', type=str, default="192.168.140.91", help="IP address of the MQTT broker.")
parser.add_argument('--port', type=int, default=1883, help="Port number of the MQTT broker.")

args = parser.parse_args()

def on_message(client, userdata, message):
    # MQTT Message
    key = message.payload.decode()
    mqtt_dump = json.loads(key)
    
    ax = mqtt_dump['ax']
    ay = mqtt_dump['ay']
    az = mqtt_dump['az']
    roll = mqtt_dump['roll']
    pitch = mqtt_dump['pitch']
    yaw = mqtt_dump['yaw']
    lin_v = mqtt_dump['linear velocity']
    ang_v = mqtt_dump['angular velocity']

    print(f"x accel: {ax}, y accel: {ay}, z accel: {az}, linear velocity: {lin_v}, angular velocity: {ang_v}")

print("Starting MQTT listener... in IP: ", args.ip, " Port: ", args.port, " Topic: ", "imu data")

# Rest of the MQTT suff
client = mqtt.Client()
client.on_message = on_message
client.connect(args.ip, args.port, keepalive=60)
client.subscribe("imu data")
client.loop_forever()