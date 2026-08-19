import customtkinter as ctk
import tkinter as tk

from database import Database
from newmemo import NewMemo

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.menu_bar()
        self.title("Note Bloc")
        self.geometry("800x700")

        # Initialize the database
        self.db = Database()
        self.db.connect()
        select_query = "SELECT id, content FROM memos ORDER BY id DESC"
        results = self.db.execute_query(select_query)

        if results:
            for memo_id, memo_content in results:
                memo_label = ctk.CTkLabel(self, text=f"Memo {memo_id}: {memo_content}")
                memo_label.pack(pady=5)


    def menu_bar(self):
        # Create a menubar
        self.menu_bar = tk.Menu(self)
        self.configure(menu=self.menu_bar)
        
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=False)
        file_menu.add_command(label="Nouveau", command=self.new_memo)
        file_menu.add_command(label="Quitter", command=self.window_close)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def new_memo(self):
            self.withdraw()  # Hide the main window
            self.new_memo_window = NewMemo(self)
            self.new_memo_window.protocol("WM_DELETE_WINDOW", self.on_new_memo_close)

    def on_new_memo_close(self):
         self.new_memo_window.destroy()
         self.deiconify()  # Show the main window again
    
    def window_close(self):
        self.db.disconnect()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.window_close)
    app.mainloop()