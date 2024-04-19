import time, os
import paho.mqtt.client as paho

from paho import mqtt
from dotenv import load_dotenv

# load environment variables
load_dotenv()

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with result code %s." % rc)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#", qos=1) # subscribe to all topics

# Print message, callback for when a publish message is received from the server. Useful for checking if it was successful.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if not os.path.exists("data/"):
         os.makedirs("data/")
    with open("data/msg.txt", "a+") as file:
        file.write(msg.topic + " " + str(msg.qos) + " " + str(msg.payload) + "\n")


def main():
        # Program starts
        print("Connecting to client...")
        # Create client instance
        client = paho.Client(
        callback_api_version=paho.CallbackAPIVersion.VERSION2,
        client_id="2",
        userdata=None,
        protocol=paho.MQTTv5,
        )

        client.on_connect = on_connect
        client.on_message = on_message

        # enable TLS for secure connection
        #client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        #client.tls_set(ca_certs="./isrgrootx1.pem")
        # set username and password
        #client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PWD"))
        # connect to broker (HiveMQ Cloud) on port 8883 (default for MQTT)
        #client.connect(os.getenv("MQTT_HOST"), 8883)
        client.connect(os.getenv("MQTT_HOST"), 1883)
        #client.connect("127.0.0.1", 1883)

        start_time = time.time()
        duration = 15 # seconds

        # # Redirect output to a file
        # with open("data/messages.txt", "w") as f:
        #     sys.stdout = f
            
        # disconnect the client from the broker after X seconds (duration)
        while time.time() - start_time <= duration:
            rc = client.loop(timeout=1.0)
            if rc !=0:
                print("Connection error, please reconnect")
                break

        print("Disconnecting...")
        client.disconnect()

if __name__ == "__main__":
    main()
