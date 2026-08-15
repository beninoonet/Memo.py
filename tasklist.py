from tkinter import *

import os
# import psycopg2 - PostgreSQL database adapter for Python
import psycopg2
# dotenv - loads environment variables from a .env file into the environment
from dotenv import load_dotenv
load_dotenv()

import datetime

# Load DB credentials from environment variables
host = os.getenv("DB_HOST")
monica_database = os.getenv("DB_DATABASE_MONICA")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

class App:
        def connect_db(self):
            try:
                self.conn = psycopg2.connect(
                    host=host,
                    database=monica_database,
                    user=user,
                    password=password
                )
                self.cursor = self.conn.cursor()
                print("Connected to the database")
            except Exception as e:
                print(f"Error connecting to the database: {e}")

        def get_tasks(self):
            try:
                self.cursor.execute("SELECT * FROM monica_tasks")
                tasks = self.cursor.fetchall()
                return tasks
            except Exception as e:
                print(f"Error fetching tasks: {e}")
                return []

        def check_db_changes(self):
             # check if the database has changed and update the task list accordingly
            current_tasks = self.get_tasks()
            if current_tasks != self.previous_tasks:
                self.previous_tasks = current_tasks
                self.see_tasks()
            if self.root.winfo_exists():  # Check if the window still exists
                self.root.after(5000, self.check_db_changes)  # Check again after 5 seconds

        def see_tasks(self):
            tasks = self.get_tasks()
            for task in tasks:
                print(f"Task ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Due Date: {task[3]}, Status: {task[4]}")
                statusFrames = LabelFrame(self.root, text=f"Status: {task[4]}", font=("Helvetica", 12, "bold"), bg="#f0f0f0", padx=10, pady=5) 
                statusFrames.pack(pady=5, fill="x", expand=True)

                user_label = Label(statusFrames, text=f"Utilisateur: {task[1]}")
                user_label.pack(pady=5, anchor="w")

                task_label = Label(statusFrames, text=f"Tâche: {task[2]}")
                task_label.pack(pady=5, anchor="w")

                        # Formatage de la date/heure
                raw_date = task[3]
                if isinstance(raw_date, (datetime.date, datetime.datetime)):
                    formatted_date = raw_date.strftime("%d/%m/%Y à %H:%M")
                else:
                    formatted_date = str(raw_date)  # au cas où ce serait déjà une chaîne
                
                created_label = Label(statusFrames, text=f"Crée le: {formatted_date}")
                created_label.pack(pady=5, anchor="w")

                id_label = Label(statusFrames, text=f"ID: {task[0]}")
                id_label.pack(pady=5, anchor="w")
            self.previous_tasks = tasks


        def __init__(self, root):
            self.root = root
            self.root.title("Secret Silent Box - Tasklist")
            self.connect_db()
            self.menu()
            self.windows()
            print("Task initialized")


        def windows(self):
            self.root.geometry("800x500")
            self.root.configure(bg="#f0f0f0")

            self.label = Label(self.root, text="Secret Silent Box - Tasklist", font=("Helvetica", 16), bg="#f0f0f0")
            self.label.pack(pady=10)

            self.previous_tasks = []
            self.see_tasks()
            self.root.after(5000, self.check_db_changes)  # Check for changes every 5 seconds
            




        # Menu to navigate
        def menu(self):
            self.menu_bar = Menu(self.root)
            self.root.config(menu=self.menu_bar)
        
            self.file_menu = Menu(self.menu_bar, tearoff=0)
            self.file_menu.add_command(label="Quitter", command=self.on_closing)
            self.menu_bar.add_cascade(label="Fichier", menu=self.file_menu)
            # add a change page menu to the menu bar
            self.page_menu = Menu(self.menu_bar, tearoff=0)
            # add a tasklist page to the menu bar to change a app to tasklist.py
            self.page_menu.add_command(label="App", command=self.open_app)
            self.menu_bar.add_cascade(label="Pages", menu=self.page_menu)

        def open_app(self):
            self.root.destroy()
            import memo
            memo = memo.App(Tk())


        def on_closing(self):
                    self.root.destroy()

# add a main function to run the application
if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

# export the App class for use in other modules
tasklist = App