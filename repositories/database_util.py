import psycopg2

globalConnection = None
globalCursor = None
class DBUtil:
    def __init__(self):
        global globalConnection, globalCursor
        self.connection = None
        self.cursor = None
        if globalConnection is not None and globalCursor is not None:
            self.connection = globalConnection
            self.cursor = globalCursor
        else:
            try:
                self.connection = psycopg2.connect(
                    host="localhost",
                    user="jarvis",
                    password="ryuzaki@156969",
                    database="jarvis_db",
                    port="5432"
                )
                self.cursor = self.connection.cursor()
                print("Connected to PostgreSQL")
                globalConnection = self.connection
                globalCursor = self.cursor
            except Exception as error:
                print(f"Error connecting to PostgreSQL: {error}")

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        if self.cursor:
            self.cursor.execute(query, params)
            result = []
            if self.cursor.description:
                result = self.cursor.fetchall()
            self.connection.commit()
            return result
        else:
            print("Connection is not initialized")
            return []