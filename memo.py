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

        """ Application """
class App:
        def __init__(self, root):
                        self.root = root
                        self.root.title("Secret Silent Box")
                        self.menu()
                        self.db = Database()
                        self.db.connect()
                        self.windows()

        def windows(self):
            self.root.geometry("800x500")
            self.root.configure(bg="#f0f0f0")
            
            self.canvas = Canvas(self.root, width=800, height=500, bg="#f0f0f0", highlightthickness=0)
            self.scrollbar = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
            self.scrollbar.pack(side="right", fill="y")
            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.canvas.pack(side="left", fill="both", expand=True)
            self.scrollbar.pack(side="right", fill="y")


            self.main_frame = Frame(self.canvas, bg="#f0f0f0")
            self.canvas_window = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

            self.main_frame.bind("<Configure>", self.on_frame_configure)
            self.canvas.bind("<Configure>", self.on_canvas_configure)

            self.main_frame.bind_all("<MouseWheel>", self.on_mousewheel)

            # Label for the text box
            self.label = Label(self.main_frame, text="Memory text", font=("Montserrat", 16), bg="#f0f0f0")
            self.label.pack(pady=20)
            # Text box for user input
            self.textbox = Text(self.main_frame, height=10, width=40, font=("Montserrat", 12), wrap="word", bg="white", relief="solid", borderwidth=1)
            self.textbox.pack(pady=10)
            # Save button to save the text to the database
            self.save_button = Button(
                self.main_frame,
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
                cursor="hand2",
                justify="center"
            )
            self.save_button.pack(pady=15)

            # Remove button to remove the last text saved in the database
            # Entry for the user to enter the ID of the text to remove
            self.remove_entry = Entry(self.main_frame, font=("Montserrat", 12), width=10, justify="center", relief="solid", borderwidth=1)
            self.remove_entry.pack(pady=10)

            self.remove_button = Button(
                self.main_frame,
                text="Supprimer",
                command=self.remove_text,
                font=("Montserrat", 12, "bold"),
                bg="#f44336",
                fg="white",
                activebackground="#e53935",
                activeforeground="white",
                relief="flat",
                borderwidth=0,
                padx=20,
                pady=10,
                cursor="hand2",
                justify="center"
            )
            self.remove_button.pack(pady=15)

            # watch all texts saved in the database
            self.textlabel = Label(self.main_frame, text="Saved texts:", font=("Montserrat", 14), bg="#f0f0f0", justify="center")
            self.textlabel.pack(pady=10)
            self.see_texts()

        def on_frame_configure(self, event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            self.center_frame()

        def on_canvas_configure(self, event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
            self.center_frame()

        def on_mousewheel(self, event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def center_frame(self):
            self.canvas.update_idletasks()
            canvas_height = self.canvas.winfo_height()
            frame_height = self.main_frame.winfo_reqheight()
            if frame_height < canvas_height:
                y_offset = (canvas_height - frame_height) // 2
            else:
                y_offset = 0
            self.canvas.coords(self.canvas_window, 0, y_offset)

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
            self.page_menu.add_command(label="Tasklist", command=self.open_tasklist)
            self.menu_bar.add_cascade(label="Pages", menu=self.page_menu)

        def open_tasklist(self):
            # import tasklist.py change the app to tasklist.py
            self.root.destroy()
            import tasklist
            tasklist_root = Tk()
            tasklist_app = tasklist.App(tasklist_root)
            
            
        def see_texts(self):
            query = "SELECT * FROM texts"
            results = self.db.execute_query(query)
            if results:
                for idx, (text_id, content) in enumerate(results):
                    lframe = LabelFrame(self.main_frame, text=f"ID:{text_id}", font=("Montserrat", 12, "bold"), bg="#f0f0f0", padx=10, pady=5)
                    lframe.pack(pady=5, fill="x", expand=True)
                    text_label = Label(lframe, text=f"{idx + 1}. {content}", font=("Montserrat", 12), bg="#f0f0f0", wraplength=350, justify="center")
                    text_label.pack(pady=5, anchor="w")
            else:
                print("No texts found in the database")

        # Refresh the saved texts display
        def refresh_texts(self):
                    for widget in self.main_frame.winfo_children():
                        if isinstance(widget, LabelFrame):
                            widget.destroy()
                    self.see_texts()

        # remove the last text saved in the database
        def remove_text(self):
            # get the ID from the entry
            text_id = self.remove_entry.get().strip()
            if text_id:
                query = "DELETE FROM texts WHERE id = %s"
                self.db.execute_query(query, (text_id,))
                print(f"Text with ID {text_id} removed from database")
            else:
                query = "DELETE FROM texts WHERE id = (SELECT id FROM texts ORDER BY id DESC LIMIT 1)"
                self.db.execute_query(query)
                print("Last text removed from database")
            # Refresh the saved texts display
            self.refresh_texts()
        
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
                # Refresh the saved texts display
                self.refresh_texts()

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

# add a main function to run the application
if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
