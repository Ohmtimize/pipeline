import time, os
import paho.mqtt.client as paho

from paho import mqtt
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# Define topic
topic = "#"

# Connect functions
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
         print("CONNACK received with result code %s." % rc)
    else:
        print("Failed to connect, return code %d\n", rc)        


def connect_mqtt():
        # Create client instance
        client = paho.Client(
        callback_api_version=paho.CallbackAPIVersion.VERSION2,
        client_id="2",
        userdata=None,
        protocol=paho.MQTTv5,
        )

        client.on_connect = on_connect
        client.connect(os.getenv("MQTT_HOST"), int(os.getenv("PORT"))) # client.connect(broker, port)
        return client
     

# Print message - callback for when a publish message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if not os.path.exists("data/"):
         os.makedirs("data/")
    with open("data/msg.txt", "a+") as file:
        file.write(msg.topic + " " + str(msg.qos) + " " + str(msg.payload) + "\n")

# Subscribe function
def subscribe(client, topic):
    client.subscribe(topic, qos=1) # subscribe to all topics
    client.on_message = on_message

# Main function
def main():
        # Program starts
        print("Connecting to client...")

        # Connect and subscribe
        client = connect_mqtt()
        subscribe(client, topic)
        
        start_time = time.time()
        duration = 15 # seconds

            
        # Disconnect the client from the broker after X seconds (duration)
        while time.time() - start_time <= duration:
            rc = client.loop(timeout=1.0)
            if rc !=0:
                print("Connection error, please reconnect")
                break

        print("Disconnecting...")
        client.disconnect()

if __name__ == "__main__":
    main()
