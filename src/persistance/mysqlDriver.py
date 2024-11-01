import mysql.connector as mysql
import config as config


# Database class
class MysqlDB:
    def __enter__(self):
        self.connector = mysql
        self.connexion = self.connector.connect(**config.db)
        self.cursor = self.connexion.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connexion.close()

    def runSQL(self, sql, val=None):
        self.cursor.execute(sql, val)
        self.connexion.commit()
        return self
    
    def save(self, topic, qos, payload):
        with MysqlDB() as db:
            sql = (
                "INSERT INTO "
                + self.table
                + " (topic, qos, payload) VALUES (%s, %s, %s)"
            )
            val = (topic, qos, payload)
            db.runSQL(sql, val)
