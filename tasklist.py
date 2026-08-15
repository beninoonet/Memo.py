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

class App:

        def __init__(self, root):
            self.root = root
            self.root.title("Secret Silent Box - Tasklist")
            self.menu()
            self.windows()
            print("Task initialized")


        def windows(self):
            self.root.geometry("800x500")
            self.root.configure(bg="#f0f0f0")

            self.label = Label(self.root, text="Secret Silent Box - Tasklist", font=("Helvetica", 16), bg="#f0f0f0")
            self.label.pack(pady=10)

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