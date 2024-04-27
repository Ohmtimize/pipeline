import mysql.connector as mysql
import src.config as config


# Database class
class MysqlDB:
    def __enter__(self):
        self.connector = mysql
        self.db = self.connector.connect(**config.db)
        self.cursor = self.db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.db.close()

    def runSQL(self, sql, val):
        self.cursor.execute(sql, val)
        self.db.commit()
