"""Module that will run migration scripts."""

import mysql.connector.errorcode as errorcode
import sys

# Add the parent directory to the path
# This allows migrations to be run from any directory
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append("src")

from mysqlDriver import MysqlDB

# Create migration table if does not yet exist
QUERIES = {}

STATEMENT = "Create table"

QUERIES["migrations"] = {
    STATEMENT: "CREATE TABLE migrations ("
    "id int(1) NOT NULL AUTO_INCREMENT,"
    "name varchar(255) NOT NULL,"
    "inserted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    "last_updated timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "PRIMARY KEY (id)"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
}

QUERIES["messages"] = {
    STATEMENT: "CREATE TABLE messages ("
    "id int(11) NOT NULL AUTO_INCREMENT,"
    "topic varchar(255) NOT NULL,"
    "qos int(11) NOT NULL,"
    "payload TEXT NOT NULL,"
    "inserted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    "last_updated timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "PRIMARY KEY (id)"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
}

QUERIES["base_topics"] = {
    STATEMENT: "CREATE TABLE base_topics ("
    "id int(11) NOT NULL AUTO_INCREMENT,"
    "label varchar(255) NOT NULL,"
    "inserted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    "last_updated timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "PRIMARY KEY (id),"
    "UNIQUE KEY (label)"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
}

QUERIES["entities"] = {
    STATEMENT: "CREATE TABLE entities ("
    "id int(11) NOT NULL AUTO_INCREMENT,"
    "label varchar(255) NOT NULL,"
    "base_topic_id int(11) NOT NULL,"
    "inserted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    "last_updated timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "PRIMARY KEY (id),"
    "UNIQUE KEY (base_topic_id, label),"
    "FOREIGN KEY (base_topic_id) REFERENCES base_topics(id)"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
}

QUERIES["states"] = {
    STATEMENT: "CREATE TABLE states ("
    "id int(11) NOT NULL AUTO_INCREMENT,"
    "entity_id int(11) NOT NULL,"
    "label varchar(255) NOT NULL,"
    "inserted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    "last_updated timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "PRIMARY KEY (id),"
    "UNIQUE KEY (entity_id, label),"
    "FOREIGN KEY (entity_id) REFERENCES entities(id)"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
}

QUERIES["domains"] = {
    STATEMENT: "CREATE TABLE domains ("
    "id int(11) NOT NULL AUTO_INCREMENT,"
    "entity_id int(11) NOT NULL,"
    "label varchar(255) NOT NULL,"
    "inserted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    "last_updated timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "PRIMARY KEY (id),"
    "UNIQUE KEY (entity_id, label),"
    "FOREIGN KEY (entity_id) REFERENCES entities(id)"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
}

QUERIES["facts"] = {
    STATEMENT: "CREATE TABLE facts ("
    "id int(11) NOT NULL AUTO_INCREMENT,"
    "state_id int(11) NOT NULL,"
    "fact TEXT NOT NULL,"
    "inserted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    "last_updated timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "PRIMARY KEY (id),"
    "FOREIGN KEY (state_id) REFERENCES states(id)"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
}

QUERIES["trigger"] = {
    STATEMENT: "CREATE TRIGGER formating "
    "AFTER INSERT "
    "ON messages FOR EACH ROW "
    "BEGIN "
    "INSERT INTO base_topics (label) "
    "SELECT substring_index(substring_index(NEW.topic, '/', 1), '/', -1) as label "
    "ON DUPLICATE KEY UPDATE last_updated=NOW();"
    "INSERT INTO entities (label, base_topic_id) "
    "SELECT substring_index(substring_index(NEW.topic, '/', 3), '/', -1) AS label, base_topics.id AS base_topic_id FROM base_topics "
    "WHERE base_topics.label=substring_index(substring_index(NEW.topic, '/', 1), '/', -1) "
    "ON DUPLICATE KEY UPDATE last_updated=NOW();"
    "INSERT INTO states (label, entity_id) "
    "SELECT substring_index(substring_index(NEW.topic, '/', 4), '/', -1) AS label, entities.id AS entity_id FROM entities "
    "WHERE entities.label=substring_index(substring_index(NEW.topic, '/', 3), '/', -1)"
    "AND entities.base_topic_id=("
    "SELECT base_topics.id "
    "FROM base_topics "
    "WHERE base_topics.label=substring_index(substring_index(NEW.topic, '/', 1), '/', -1) "
    ") "
    "ON DUPLICATE KEY UPDATE last_updated=NOW(); "
    "INSERT INTO facts (fact, state_id) "
    "SELECT NEW.payload AS fact, states.id AS state_id FROM states "
    "WHERE states.label=substring_index(substring_index(NEW.topic, '/', 4), '/', -1) "
    "AND states.entity_id=( "
    "SELECT entities.id "
    "FROM entities "
    "WHERE entities.label=substring_index(substring_index(NEW.topic, '/', 3), '/', -1) "
    "AND entities.base_topic_id=( "
    "SELECT base_topics.id "
    "FROM base_topics "
    "WHERE base_topics.label=substring_index(substring_index(NEW.topic, '/', 1), '/', -1) "
    ")"
    ");"
    "END; "
}


def main():
    with MysqlDB() as db:
        for table_name in QUERIES:
            table_description = QUERIES[table_name]
            try:
                print("Running Queries {}: ".format(table_name), end="")
                db.runSQL(table_description[STATEMENT], None)
                print("OK")
            except db.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("table already exists.")
                else:
                    print(err.msg)


if __name__ == "__main__":
    main()
