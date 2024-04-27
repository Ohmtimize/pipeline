"""Module that will run migration scripts."""

import mysql.connector.errorcode as errorcode
import os
import sys

# Add the parent directory to the path
# This allows migrations to be run from any directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.mysqlDriver import MysqlDB

# Create migration table if does not yet exist
TABLES = {}

TABLES["migrations"] = {
    "Create table": "CREATE TABLE migrations ("
    "id int(1) NOT NULL AUTO_INCREMENT,"
    "name varchar(255) NOT NULL,"
    "inserted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    "last_updated timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "PRIMARY KEY (id)"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
}

TABLES["messages"] = {
    "Create table": "CREATE TABLE messages ("
    "id int(11) NOT NULL AUTO_INCREMENT,"
    "topic varchar(255) NOT NULL,"
    "qos int(11) NOT NULL,"
    "payload varchar(255) NOT NULL,"
    "inserted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    "last_updated timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "PRIMARY KEY (id)"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
}


def main():
    with MysqlDB() as db:
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end="")
                db.runSQL(table_description["Create table"], None)
                print("OK")
            except db.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)


if __name__ == "__main__":
    main()
