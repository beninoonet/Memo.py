from tkinter import *

import os
# import psycopg2 - PostgreSQL database adapter for Python
import psycopg2
# dotenv - loads environment variables from a .env file into the environment
from dotenv import load_dotenv
load_dotenv()


# Load DB credentials from environment variables
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.create_table()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor()
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
        CREATE TABLE IF NOT EXISTS texts (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL
        );
        """
        self.execute_query(create_table_query)
        print("Table 'texts' created or already exists")

        """ Application """
class App:
        def windows(self):
            self.root.geometry("400x500")
            self.root.configure(bg="#f0f0f0")

            self.label = Label(self.root, text="Memory text", font=("Montserrat", 16), bg="#f0f0f0")
            self.label.pack(pady=20)

            self.textbox = Text(self.root, height=10, width=40)
            self.textbox.pack(pady=10)

            self.save_button = Button(
                self.root,
                text="Enregistrer",
                command=self.save_text,
                font=("Montserrat", 12, "bold"),
                bg="#813291",
                fg="white",
                activebackground="#8b45a0",
                activeforeground="white",
                relief="flat",
                borderwidth=0,
                padx=20,
                pady=10,
                cursor="hand2"
            )
            self.save_button.pack(pady=15)


        # save the text to the database
        def save_text(self):
            text = self.textbox.get("1.0", END).strip()
            if text:
                query = "INSERT INTO texts (content) VALUES (%s)"
                self.db.execute_query(query, (text,))
                self.textbox.delete("1.0", END)
                self.textbox.configure(bg="white")  # Reset background color to white
                self.save_button.configure(text="Enregistrement...",bg="#4CAF50")  # Reset button color to green
                self.root.after(500, lambda: self.save_button.configure(text="Enregistrer", bg="#813291"))  # Reset button color after 500ms
                print("Text saved to database")
            else:
                print("Textbox is empty")
                self.root.bell()  # Ring the bell to indicate an error
                self.textbox.focus_set()  # Set focus back to the textbox
                self.textbox.configure(bg="#ffcccc")  
                self.root.after(500, lambda: self.textbox.configure(bg="white"))  # Reset background color after 500ms
                self.save_button.configure(text="Aucun texte",bg="#f44336") 
                self.root.after(500, lambda: self.save_button.configure(bg="#4CAF50"))
                # text is empty, show a message box

        def on_closing(self):
            self.db.disconnect()
            self.root.destroy()

        def __init__(self, root):
                self.root = root
                self.root.title("Memory text")
                self.db = Database()
                self.db.connect()
                self.windows()

# add a main function to run the application
if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
