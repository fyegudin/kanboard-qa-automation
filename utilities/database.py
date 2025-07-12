import psycopg2
from config.config import DB_CONFIG


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()

    def execute_query(self, query: str, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor

    def fetch_one(self, query: str, params=None):
        self.execute_query(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query: str, params=None):
        self.execute_query(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()