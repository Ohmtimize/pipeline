import time, os
import paho.mqtt.client as paho
from dotenv import load_dotenv
from src.mysqlDriver import MysqlDB

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
    client.connect(
        os.getenv("MQTT_HOST"), int(os.getenv("PORT"))
    )  # client.connect(broker, port)
    return client


def save_message_in_DB(message):
    """
    Save a message in the database.

    Args:
        message (object): The message object containing the topic, QoS, and payload.

    Returns:
        None

    Raises:
        mysql.connector.Error: If there is an error connecting to or executing the SQL query.

    Description:
        This function connects to a MySQL database using the provided environment variables and saves the message in a table named 'your_table'. The message object should have the following attributes:
        - topic (str): The topic of the message.
        - qos (int): The Quality of Service level of the message.
        - payload (str): The payload of the message.

        The function executes an INSERT statement to insert the topic, QoS, and payload into the 'your_table' table. After the insertion, the changes are committed to the database.

        Note: The function assumes that the MySQL database is already set up with a table named 'your_table' that has the columns 'topic', 'qos', and 'payload'.

    Example:
        message = Message("topic1", 1, "payload1")
        save_message_in_DB(message)
    """
    with MysqlDB() as db:
        sql = "INSERT INTO messages (topic, qos, payload) VALUES (%s, %s, %s)"
        val = (message.topic, message.qos, message.payload)
        db.runSQL(sql, val)


def save_message_in_file(message):
    if not os.path.exists("data/"):
        os.makedirs("data/")
    with open("data/msg.txt", "a+") as file:
        file.write(
            message.topic + " " + str(message.qos) + " " + str(message.payload) + "\n"
        )


# Print message - callback for when a publish message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    save_message_in_file(msg)
    save_message_in_DB(msg)


# Subscribe function
def subscribe(client, topic):
    client.subscribe(topic, qos=1)  # subscribe to all topics
    client.on_message = on_message


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
