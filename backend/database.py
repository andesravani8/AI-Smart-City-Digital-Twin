import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Database:

    def __init__(self):

        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "3306"))
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv(
            "DB_NAME",
            "smart"
        )

    def get_connection(self):

        try:

            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if connection.is_connected():
                return connection

        except Error as e:

            print("Database connection error:", e)

        return None


database = Database()