import customtkinter as ctk
import tkinter as tk

from database import Database

class NewMemo(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.window()


    def window(self):
        self.title("Bloc-Note")
        self.geometry("800x700")

        # cursor
        self.main_frame = ctk.CTkScrollableFrame(self, bg_color="#1e1e1e", fg_color="#1e1e1e")
        self.main_frame.pack(fill="both", expand=True)

        # Create a menubar
        self.menu_bar = tk.Menu(self)
        self.configure(menu=self.menu_bar)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=False)
        file_menu.add_command(label="Nouveau", command=self.new_memo)
        file_menu.add_command(label="Sélectionner un mémo.", command=self.input_id)
        file_menu.add_command(label="Quitter", command=self.window_close)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Label Title
        self.title_label = ctk.CTkLabel(self.main_frame, text="Nouveau Mémo", font=("Montserrat", 20, "bold"), text_color="#ffffff")
        self.title_label.pack(pady=10)

        # Memo textbox
        self.memo_textbox = ctk.CTkTextbox(self.main_frame, width=750,  height=500, bg_color="#494949", fg_color="#3f3f3f", text_color="#ffffff", font=("Arial", 16))
        self.memo_textbox.pack()

        # frame for buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, bg_color="#1e1e1e", fg_color="#1e1e1e")
        self.button_frame.pack(pady=10)
        
        # Save button
        self.save_button = ctk.CTkButton(self.button_frame, text="Sauvegarder.", command=self.save_memo)
        self.save_button.pack(side=ctk.LEFT, pady=10, padx=10)
        # Save memo with Ctrl+S
        self.bind("<Control-s>", lambda event: self.save_memo()) 
        # Update button
        self.update_button = ctk.CTkButton(self.button_frame, text="Mettre à jour.", command=self.update_memo)
        self.update_button.pack(side=ctk.LEFT, pady=10, padx=10)

    def window_close(self):
        self.master.deiconify()  # Show the main window again
        self.destroy()  # Close the NewMemo window

    def new_memo(self):
        self.memo_textbox.delete("1.0", "end")


    # List of memos
    def input_id(self):
        db = Database()
        db.connect()
        select_query = "SELECT id, content FROM memos ORDER BY id DESC"
        result = db.execute_query(select_query)
        db.disconnect()

        if result:
            # Create a new window to display the list of memos
            list_window = ctk.CTkToplevel(self)
            list_window.title("Liste des Mémos")
            list_window.geometry("600x400")

            # Create a scrollable frame for the list of memos
            scrollable_frame = ctk.CTkScrollableFrame(list_window, width=580, height=380)
            scrollable_frame.pack(pady=10, padx=10)

            # Display the list of memos with their IDs
            for memo_id, memo_content in result:
                memo_label = ctk.CTkLabel(scrollable_frame, text=f"ID: {memo_id} - {memo_content[:50]}...", font=("Arial", 14), anchor="w")
                memo_label.pack(fill="x", pady=5)

                # Add a button to load the selected memo
                load_button = ctk.CTkButton(scrollable_frame, text="Charger", command=lambda m_id=memo_id: self.load_selected_memo(m_id, list_window))
                load_button.pack(pady=5)
                # add a delete button to delete the selected memo
                delete_button = ctk.CTkButton(scrollable_frame, text="Supprimer", command=lambda m_id=memo_id: self.delete_selected_memo(m_id, list_window))
                delete_button.pack(pady=5)

        else:
            self.bell()  # Alert sound
            if hasattr(self, "success_label") and self.success_label.winfo_exists():
                self.success_label.pack_forget()

            if not hasattr(self, "error_label") or not self.error_label.winfo_exists():
                self.error_label = ctk.CTkLabel(self.main_frame, text="Aucun mémo trouvé.", font=("Arial", 20), text_color="#be2e2e")
                self.error_label.pack(pady=10)
            else:
                self.error_label.configure(text="Aucun mémo trouvé.")
    

    def delete_selected_memo(self, memo_id, list_window):
        db = Database()
        db.connect()
        delete_query = "DELETE FROM memos WHERE id = %s"
        db.execute_query(delete_query, (memo_id,))
        db.disconnect()

        # Refresh the list window after deletion
        list_window.destroy()  # Close the current list window
        self.input_id()  # Reopen the list window to show updated list

        # Check if error_label visible
        if hasattr(self, "error_label") and self.error_label.winfo_exists():
            self.error_label.pack_forget()

        if not hasattr(self, "success_label") or not self.success_label.winfo_exists():
            self.success_label = ctk.CTkLabel(self.main_frame, text=f"Mémo ID {memo_id} supprimé.", font=("Arial", 20))
            self.success_label.pack(pady=10)
        else:
            self.success_label.configure(text=f"Mémo ID {memo_id} supprimé.")

    def load_selected_memo(self, memo_id, list_window):
        db = Database()
        db.connect()
        select_query = "SELECT content FROM memos WHERE id = %s"
        result = db.execute_query(select_query, (memo_id,))
        db.disconnect()

        if result:
            self.memo_textbox.delete("1.0", "end")  # Clear the textbox
            self.memo_textbox.insert("1.0", result[0][0])  # Insert the selected memo
            list_window.destroy()  # Close the list window

            # Check if error_label visible
            if hasattr(self, "error_label") and self.error_label.winfo_exists():
                self.error_label.pack_forget()

            if not hasattr(self, "success_label") or not self.success_label.winfo_exists():
                self.success_label = ctk.CTkLabel(self.main_frame, text=f"Mémo ID {memo_id} chargé.", font=("Arial", 20))
                self.success_label.pack(pady=10)
            else:
                self.success_label.configure(text=f"Mémo ID {memo_id} chargé.")
        else:
            self.bell()  # Alert sound
            if hasattr(self, "success_label") and self.success_label.winfo_exists():
                self.success_label.pack_forget()

            if not hasattr(self, "error_label") or not self.error_label.winfo_exists():
                self.error_label = ctk.CTkLabel(self.main_frame, text=f"Aucun mémo trouvé avec l'ID {memo_id}.", font=("Arial", 20), text_color="#be2e2e")
                self.error_label.pack(pady=10)
            else:
                self.error_label.configure(text=f"Aucun mémo trouvé avec l'ID {memo_id}.")
    
    def update_memo(self):
        memo_text = self.memo_textbox.get("1.0", "end-1c")  # Get the text from the textbox
        if memo_text.strip():  # Check if the text is not empty
            db = Database()
            db.connect()
            update_query = "UPDATE memos SET content = %s, updated_at = CURRENT_TIMESTAMP WHERE id = (SELECT id FROM memos ORDER BY id DESC LIMIT 1)"
            db.execute_query(update_query, (memo_text,))
            db.disconnect()

            # Check if error_label visible
            if hasattr(self, "error_label") and self.error_label.winfo_exists():
                self.error_label.pack_forget()

            if not hasattr(self, "success_label") or not self.success_label.winfo_exists():
                self.success_label = ctk.CTkLabel(self.main_frame, text="Mémo mis à jour.", font=("Arial", 20))
                self.success_label.pack(pady=10)
            else:
                self.success_label.configure(text="Mémo mis à jour.")
        else:
            self.bell() # Alert sound

            if hasattr(self, "success_label") and self.success_label.winfo_exists():
                self.success_label.pack_forget()

            if not hasattr(self, "error_label") or not self.error_label.winfo_exists():
                self.error_label = ctk.CTkLabel(self.main_frame, text="Impossible de mettre à jour un texte vide.", font=("Arial", 20), text_color="#be2e2e")
                self.error_label.pack(pady=10)
            else:
                self.error_label.configure(text="Impossible de mettre à jour un texte vide.")

    def save_memo(self):
        memo_text = self.memo_textbox.get("1.0", "end-1c")  # Get the text from the textbox
        if memo_text.strip():  # Check if the text is not empty
            db = Database()
            db.connect()
            insert_query = "INSERT INTO memos (content) VALUES (%s)"
            db.execute_query(insert_query, (memo_text,))
            db.disconnect()

            # Check if error_label visible
            if hasattr(self, "error_label") and self.error_label.winfo_exists():
                self.error_label.pack_forget()

            if not hasattr(self, "success_label") or not self.success_label.winfo_exists():
                self.success_label = ctk.CTkLabel(self.main_frame, text="Mémo sauvegarder", font=("Arial", 20))
                self.success_label.pack(pady=10)
            else:
                self.success_label.configure(text="Mémo sauvegardé")
        else:
            self.bell() # Alert sound

            if hasattr(self, "success_label") and self.success_label.winfo_exists():
                self.success_label.pack_forget()

            if not hasattr(self, "error_label") or not self.error_label.winfo_exists():
                self.error_label = ctk.CTkLabel(self.main_frame, text="Impossible de sauvegarder un texte vide.", font=("Arial", 20), text_color="#be2e2e")
                self.error_label.pack(pady=10)
            else:
                self.error_label.configure(text="Impossible de sauvegarder un texte vide.")
                
if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()  # Hide the root window
    app = NewMemo(root)
    app.protocol("WM_DELETE_WINDOW", app.window_close)
    app.mainloop()