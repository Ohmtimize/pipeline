from model import Message
from mysqlDriver import MysqlDB


def test_save_message_in_DB():
    table = "messages"
    message = Message("test_topic", 1, "test_payload")

    with MysqlDB() as db:
        db.cursor.execute(
            "DELETE FROM " + table + " WHERE topic = %s AND qos = %s AND payload = %s",
            (message.topic, message.qos, message.payload),
        )
        db.connexion.commit()

        # Run the test
        message.save()

        # Assertions
        assert_DB_has(
            table, topic=message.topic, qos=message.qos, payload=message.payload
        )

        # Clean DB
        db.cursor.execute(
            "DELETE FROM " + table + " WHERE topic = %s AND qos = %s AND payload = %s",
            (message.topic, message.qos, message.payload),
        )
        db.connexion.commit()


def assert_DB_has(table, **values):
    with MysqlDB() as db:
        db.cursor.execute(
            "SELECT * FROM "
            + table
            + " WHERE "
            + " AND ".join(f"{key} = '{value}'" for key, value in values.items())
        )
        assert db.cursor.fetchone() != None
