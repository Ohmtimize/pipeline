from mysqlDriver import MysqlDB


class Message:
    def __init__(self, topic, qos, payload):
        self.table = "messages"
        self.topic = topic
        self.qos = qos
        self.payload = payload

    def save(self):
        with MysqlDB() as db:
            sql = (
                "INSERT INTO "
                + self.table
                + " (topic, qos, payload) VALUES (%s, %s, %s)"
            )
            val = (self.topic, self.qos, self.payload)
            db.runSQL(sql, val)
