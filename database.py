import os
import psycopg2

from dotenv import load_dotenv
load_dotenv()

# Connect to the PostgreSQL database
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

# Database connection
class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor()
            self.create_table()  # Create the table if it doesn't exist
            print("Database connection successful")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database connection closed")

    def execute_query(self, query, params=None):
        if self.connection is None or self.cursor is None:
            print("Database connection is not established")
            return None
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            if self.cursor.description is not None:
                return self.cursor.fetchall()
            return None
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
        
    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS memos (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.execute_query(create_table_query)
        print("Table 'texts' created or already exists")
