import paho.mqtt.client as mqtt
import ssl
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()
# Database configuration
mqtt_config = {
    "MQTT_CLIENT_ID": os.getenv("MQTT_CLIENT_ID"),
    "MQTT_USERNAME": os.getenv("MQTT_USERNAME"),
    "MQTT_PASSWORD": os.getenv("MQTT_PASSWORD"),
    "MQTT_BROKER": os.getenv("MQTT_BROKER"),
}


# Define the topic you want to subscribe to
TOPIC = 'home'

# Define the MQTT client callbacks
def on_connect(client: mqtt.Client, userdata: dict, flags: dict, rc: int, properties=None) -> None:
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client: mqtt.Client, userdata: dict, msg: mqtt.MQTTMessage) -> None:
    print(f"Message received: {msg.topic} {msg.payload.decode()}")  # Decode bytes to string

def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Initialize the MQTT client
def start_mqtt() -> None:

    client = mqtt.Client(client_id=mqtt_config['MQTT_CLIENT_ID'], userdata=None, protocol=mqtt.MQTTv5)
    client.on_connect = on_connect

    # enable TLS for secure connection
    client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    # set username and password
    client.username_pw_set(mqtt_config['MQTT_USERNAME'], mqtt_config['MQTT_PASSWORD'])
    # connect to HiveMQ Cloud on port 8883 (default for MQTT)
    client.connect(mqtt_config['MQTT_BROKER'], 8883)

    # setting callbacks, use separate functions like above for better visibility
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_connect = on_connect

    # subscribe to all topics of encyclopedia by using the wildcard "#"
    client.subscribe("home/#", qos=1)
    client.publish("home/temperature", payload="hot", qos=1)

    # a single publish, this can also be done in loops, etc.

    # loop_forever for simplicity, here you need to stop the loop manually
    # you can also use loop_start and loop_stop
    client.loop_forever()
