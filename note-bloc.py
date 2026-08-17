import customtkinter as ctk
import os
import psycopg2

import tkinter as tk

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
        CREATE TABLE IF NOT EXISTS texts (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL
        );
        """
        self.execute_query(create_table_query)
        print("Table 'texts' created or already exists")



class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.window()


    def window(self):
        self.title("Bloc-Note")
        self.geometry("800x600")

        # Create a menubar
        self.menu_bar = tk.Menu(self)
        self.configure(menu=self.menu_bar)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=False)
        file_menu.add_command(label="Nouveau", command=self.new_memo)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Label Title
        self.title_label = ctk.CTkLabel(self, text="Texte Mémo", font=("Arial", 20))
        self.title_label.pack(pady=10)

        # Memo textbox
        self.memo_textbox = ctk.CTkTextbox(self, width=600, height=500)
        self.memo_textbox.pack(pady=20)

        # Save button
        self.save_button = ctk.CTkButton(self, text="Sauvegarder.", command=self.save_memo)
        self.save_button.pack(pady=10)

        self.bind("<Control-s>", lambda event: self.save_memo())  # Bind Ctrl+S to save_memo*

        # Load button
        self.load_button = ctk.CTkButton(self, text="Charger.", command=self.load_memo)
        self.load_button.pack(pady=10)

    def window_close(self):
        self.destroy()
        print("Window destroyed")

    def new_memo(self):
        self.memo_textbox.delete("1.0", "end")

    def save_memo(self):
        memo_text = self.memo_textbox.get("1.0", "end-1c")  # Get the text from the textbox
        if memo_text.strip():  # Check if the text is not empty
            db = Database()
            db.connect()
            insert_query = "INSERT INTO texts (content) VALUES (%s)"
            db.execute_query(insert_query, (memo_text,))
            db.disconnect()

            # Check if error_label visible
            if hasattr(self, "error_label") and self.error_label.winfo_exists():
                self.error_label.pack_forget()

            if not hasattr(self, "success_label") or not self.success_label.winfo_exists():
                self.success_label = ctk.CTkLabel(self, text="Mémo sauvegarder", font=("Arial", 20))
                self.success_label.pack(pady=10)
            else:
                self.success_label.configure(text="Mémo sauvegardé")

            self.memo_textbox.delete("1.0", "end")
        else:
            self.bell() # Alert sound

            if hasattr(self, "success_label") and self.success_label.winfo_exists():
                self.success_label.pack_forget()

            if not hasattr(self, "error_label") or not self.error_label.winfo_exists():
                self.error_label = ctk.CTkLabel(self, text="Impossible de sauvegarder un texte vide.", font=("Arial", 20), text_color="#be2e2e")
                self.error_label.pack(pady=10)
            else:
                self.error_label.configure(text="Impossible de sauvegarder un texte vide.")

    def load_memo(self):
        db = Database()
        db.connect()
        select_query = "SELECT content FROM texts ORDER BY id DESC LIMIT 1"
        result = db.execute_query(select_query)
        db.disconnect()
        if result:
            self.memo_textbox.delete("1.0", "end")  # Clear the textbox
            self.memo_textbox.insert("1.0", result[0][0])  # Insert the last saved memo

            # Check if error_label visible
            if hasattr(self, "error_label") and self.error_label.winfo_exists():
                self.error_label.pack_forget()
            
            if not hasattr(self, "success_label") or not self.success_label.winfo_exists():
                self.success_label = ctk.CTkLabel(self, text="Dernier texte chargé.", font=("Arial", 20))
                self.success_label.pack(pady=10)
            else:
                self.success_label.configure(text="Dernier texte chargé.")
            
        else:
            self.bell()

            if hasattr(self, "success_label") and self.success_label.winfo_exists():
                self.success_label.pack_forget()
            
            if not hasattr(self, "error_label") or not self.error_label.winfo_exists():
                self.error_label = ctk.CTkLabel(self, text="Base de donnée vide.", font=("Arial", 20), text_color="#be2e2e")
                self.error_label.pack(pady=10)
            else:
                self.error_label.configure(text="Base de donnée vide.")

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.window_close)
    app.mainloop()