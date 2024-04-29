from model import Message
from mysqlDriver import MysqlDB
import pytest


class TestMessage:
    """The TestMessage class is used to test the Message class."""

    @pytest.fixture
    def generate_message(self):
        """
        Fixture that generates a Message object with the topic "test_topic", qos 1, and payload "test_payload".
        This fixture is used to set up the test environment and provides a Message object for testing.
        Returns:
            Message: A Message object with the specified topic, qos, and payload.
        """
        self.message = Message("test_topic", 1, "test_payload")

    @pytest.fixture
    def clean_DB(self, generate_message):
        """
        Fixture that cleans the database before and after running tests.
        Parameters:
            self (TestMessage): The test class instance.
            generate_message (Message): The generated message object.
        Returns:
            Message: The cleaned message object.
        """
        # Setup the DB
        delete_from_DB(
            self.message.table,
            topic=self.message.topic,
            qos=self.message.qos,
            payload=self.message.payload,
        )
        # Where the test will run with the yielded data
        yield self.message
        # Teardown: Clean the DB
        delete_from_DB(
            self.message.table,
            topic=self.message.topic,
            qos=self.message.qos,
            payload=self.message.payload,
        )

    def test_message_table_is_called_messages(self, generate_message):
        assert self.message.table == "messages"

    def test_saves_message_in_DB(self, clean_DB):
        self.message.save()
        assert_DB_has(
            self.message.table,
            topic=self.message.topic,
            qos=self.message.qos,
            payload=self.message.payload,
        )


################################################################
########## Helper functions ####################################
################################################################


def assert_DB_has(table, **values):
    """
    Asserts that a record exists in the specified table of the database that matches the given values.
    Parameters:
        table (str): The name of the table to search in.
        **values: Key-value pairs representing the conditions for the record.
    Returns:
        None
    """
    with MysqlDB() as db:
        db.cursor.execute(
            "SELECT * FROM "
            + table
            + " WHERE "
            + " AND ".join(f"{key} = '{value}'" for key, value in values.items())
        )
        assert db.cursor.fetchone() != None


def delete_from_DB(table, **values):
    """
    Deletes records from the specified table in the database based on the provided values.
    Parameters:
        table (str): The name of the table from which records will be deleted.
        **values: Key-value pairs representing the conditions for deleting records.
    Returns:
        None
    """
    with MysqlDB() as db:
        db.cursor.execute(
            "DELETE FROM "
            + table
            + " WHERE "
            + " AND ".join(f"{key} = '{value}'" for key, value in values.items())
        )
        db.connexion.commit()
