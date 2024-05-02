import os
import paho.mqtt.client as paho
from dotenv import load_dotenv
from model import Message

# load environment variables
load_dotenv()

# Define topic
topic = "#"


# Connect functions
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("CONNACK received with result code %s." % rc)
    else:
        print("Failed to connect, return code %s\n" % rc)


def connect_mqtt():
    # Create client instance
    client = paho.Client(
        callback_api_version=paho.CallbackAPIVersion.VERSION2,
        client_id="1",
        userdata=None,
        protocol=paho.MQTTv5,
    )
    client.on_connect = on_connect

    # enable TLS for secure connection
    # client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.tls_set(ca_certs="./isrgrootx1.pem")
    # set username and password
    client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASSWORD"))
    # connect to MQTT broker
    client.connect(host=os.getenv("MQTT_HOST"), port=int(os.getenv("MQTT_PORT")))
    return client


# Print message - callback for when a publish message is received from the server.
def on_message(client, userdata, msg):
    # Map to Message object from our model
    message = Message(msg.topic, msg.qos, msg.payload)
    # Do things with the message
    print(message.topic + " " + str(message.qos) + " " + str(message.payload))

    message.save()


# Subscribe function
def subscribe(client, topic):
    client.on_message = on_message
    client.subscribe(topic, qos=1)  # subscribe to all topics


# Main function
def main():
    # Program starts
    print("Connecting to client...")

    # Connect and subscribe
    client = connect_mqtt()
    subscribe(client, topic)
    try:
        while True:
            client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
        print("Disconnecting from client...")


if __name__ == "__main__":
    main()
