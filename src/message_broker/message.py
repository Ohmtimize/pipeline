class Message:
    def __init__(self, topic, qos, payload):
        self.table = "raw"
        self.topic = topic
        self.qos = qos
        self.payload = payload
