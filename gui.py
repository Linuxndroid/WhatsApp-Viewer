import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from models import Chat, Message  # Imports your existing data models
import main as db_loader  # Imports your existing database logic
import os
import sys  # Needed for the resource_path function

# --- Constants ---
FONT_NAME = "Helvetica"

# --- Theme Palettes ---
LIGHT_MODE = {
    "BG_COLOR": "#ECE5DD",
    "CHAT_LIST_BG": "#FFFFFF",
    "CHAT_LIST_BG_ALT": "#F7F7F7",
    "SENT_BG": "#DCF8C6",
    "RECEIVED_BG": "#FFFFFF",
    "TEXT_COLOR": "#484849",
    "HEADER_BG": "#00A884", # Branded Green
    "HEADER_FG": "#FFFFFF",
    "SELECT_BG": "#EAEAEA",
    "SENDER_FG": "#128C7E",
    "TIME_FG": "#666666"
}

DARK_MODE = {
    "BG_COLOR": "#121212",
    "CHAT_LIST_BG": "#1E1E1E",
    "CHAT_LIST_BG_ALT": "#2A2A2A",
    "SENT_BG": "#056162", # Darker Teal
    "RECEIVED_BG": "#2C2C2C",
    "TEXT_COLOR": "#E0E0E0",
    "HEADER_BG": "#1E1E1E",
    "HEADER_FG": "#00A884", # Branded Green
    "SELECT_BG": "#3A3A3A",
    "SENDER_FG": "#00A884",
    "TIME_FG": "#A0A0A0"
}


# Helper function to find bundled files (like your icon)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class WhatsAppViewerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.current_theme = LIGHT_MODE
        self.is_dark_mode = False

        self.title("Linuxndroid WhatsApp-View")

        # Set the window icon
        try:
            # Assumes your icon is named "icon.ico" and is in the same folder
            icon_path = resource_path("icon.ico") 
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error setting icon: {e}")
            # If it fails, it will just use the default Tkinter icon

        self.geometry("900x700")
        self.configure(bg=self.current_theme["BG_COLOR"])

        self.chats_data: list[Chat] = []
        self.contacts_data = {}

        # --- Header Frame (Branding & Toggle) ---
        self.header_frame = tk.Frame(self, bg=self.current_theme["HEADER_BG"])
        self.header_frame.pack(fill=tk.X)

        self.brand_label = tk.Label(
            self.header_frame,
            text="Linuxndroid WhatsApp-View",
            bg=self.current_theme["HEADER_BG"],
            fg=self.current_theme["HEADER_FG"],
            font=(FONT_NAME, 16, "bold"),
            pady=10
        )
        self.brand_label.pack(side=tk.LEFT, padx=15)

        self.toggle_btn = ttk.Button(
            self.header_frame,
            text="Toggle Dark Mode",
            command=self.toggle_theme
        )
        self.toggle_btn.pack(side=tk.RIGHT, padx=15, pady=10)


        # --- Top Frame for File Selection ---
        self.top_frame = tk.Frame(self, bg=self.current_theme["BG_COLOR"], bd=0)
        self.top_frame.pack(fill=tk.X, padx=10, pady=10)

        # 'msgstore.db' selection
        self.msgstore_label = tk.Label(self.top_frame, text="msgstore.db:", bg=self.current_theme["BG_COLOR"], fg=self.current_theme["TEXT_COLOR"], font=(FONT_NAME, 10))
        self.msgstore_label.pack(side=tk.LEFT, padx=(0, 5))
        self.msgstore_path = tk.Entry(self.top_frame, width=30)
        self.msgstore_path.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.msgstore_btn = ttk.Button(self.top_frame, text="Browse", command=self.load_msgstore)
        self.msgstore_btn.pack(side=tk.LEFT, padx=5)

        # 'wa.db' selection
        self.wa_label = tk.Label(self.top_frame, text="wa.db (Optional):", bg=self.current_theme["BG_COLOR"], fg=self.current_theme["TEXT_COLOR"], font=(FONT_NAME, 10))
        self.wa_label.pack(side=tk.LEFT, padx=(10, 5))
        self.wa_path = tk.Entry(self.top_frame, width=30)
        self.wa_path.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.wa_btn = ttk.Button(self.top_frame, text="Browse", command=self.load_wa)
        self.wa_btn.pack(side=tk.LEFT, padx=5)

        # Load button
        self.load_btn = ttk.Button(self.top_frame, text="Load Chats", command=self.load_chats)
        self.load_btn.pack(side=tk.LEFT, padx=10)

        # --- Main Paned Window (for resizable split) ---
        self.main_pane = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=3, bg=self.current_theme["BG_COLOR"])
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # --- Left Frame (Chat List) ---
        chat_list_frame = tk.Frame(self.main_pane, bg=self.current_theme["CHAT_LIST_BG"])
        chat_list_scroll = tk.Scrollbar(chat_list_frame, orient=tk.VERTICAL)
        self.chat_listbox = tk.Listbox(
            chat_list_frame,
            yscrollcommand=chat_list_scroll.set,
            bg=self.current_theme["CHAT_LIST_BG"],
            fg=self.current_theme["TEXT_COLOR"],
            font=(FONT_NAME, 11),
            bd=1,
            relief=tk.FLAT,
            highlightthickness=0,
            selectbackground=self.current_theme["SELECT_BG"],
            selectforeground=self.current_theme["TEXT_COLOR"],
            activestyle="none"
        )
        chat_list_scroll.config(command=self.chat_listbox.yview)
        
        chat_list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.chat_listbox.bind("<<ListboxSelect>>", self.display_chat)
        
        self.main_pane.add(chat_list_frame, width=250, minsize=150)

        # --- Right Frame (Message Display) ---
        chat_display_frame = tk.Frame(self.main_pane, bg=self.current_theme["BG_COLOR"])
        chat_display_scroll = tk.Scrollbar(chat_display_frame, orient=tk.VERTICAL)
        self.chat_display = tk.Text(
            chat_display_frame,
            yscrollcommand=chat_display_scroll.set,
            bg=self.current_theme["BG_COLOR"],
            font=(FONT_NAME, 10),
            padx=10,
            pady=10,
            bd=1,
            relief=tk.FLAT,
            highlightthickness=0,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        chat_display_scroll.config(command=self.chat_display.yview)

        chat_display_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.main_pane.add(chat_display_frame, minsize=300)

        # --- Configure Text Widget Tags for Styling ---
        self.configure_tags()

    def configure_tags(self):
        theme = self.current_theme
        self.chat_display.tag_configure(
            "sent",
            justify=tk.RIGHT,
            background=theme["SENT_BG"],
            foreground=theme["TEXT_COLOR"],
            font=(FONT_NAME, 11),
            spacing3=8,
            spacing1=2,
            lmargin1=50,
            rmargin=5
        )
        self.chat_display.tag_configure(
            "received",
            justify=tk.LEFT,
            background=theme["RECEIVED_BG"],
            foreground=theme["TEXT_COLOR"],
            font=(FONT_NAME, 11),
            spacing3=8,
            spacing1=2,
            lmargin1=5,
            rmargin=50
        )
        self.chat_display.tag_configure(
            "sender",
            font=(FONT_NAME, 10, "bold"),
            foreground=theme["SENDER_FG"]
        )
        self.chat_display.tag_configure(
            "time",
            font=(FONT_NAME, 8),
            foreground=theme["TIME_FG"],
            spacing1=4
        )
        self.chat_display.tag_configure("spacer", spacing3=5)

    def toggle_theme(self):
        if self.is_dark_mode:
            self.current_theme = LIGHT_MODE
            self.toggle_btn.config(text="Toggle Dark Mode")
            self.is_dark_mode = False
        else:
            self.current_theme = DARK_MODE
            self.toggle_btn.config(text="Toggle Light Mode")
            self.is_dark_mode = True
        
        self.apply_theme()
    
    def apply_theme(self):
        theme = self.current_theme
        
        # 1. Root window
        self.configure(bg=theme["BG_COLOR"])
        
        # 2. Header
        self.header_frame.config(bg=theme["HEADER_BG"])
        self.brand_label.config(bg=theme["HEADER_BG"], fg=theme["HEADER_FG"])
        
        # 3. Top (file selection) frame
        self.top_frame.config(bg=theme["BG_COLOR"])
        self.msgstore_label.config(bg=theme["BG_COLOR"], fg=theme["TEXT_COLOR"])
        self.wa_label.config(bg=theme["BG_COLOR"], fg=theme["TEXT_COLOR"])
        
        # 4. Paned Window
        self.main_pane.config(bg=theme["BG_COLOR"])
        
        # 5. Chat List
        self.chat_listbox.config(
            bg=theme["CHAT_LIST_BG"], 
            fg=theme["TEXT_COLOR"],
            selectbackground=theme["SELECT_BG"],
            selectforeground=theme["TEXT_COLOR"]
        )
        # Re-color existing listbox items
        for i in range(self.chat_listbox.size()):
            bg = theme["CHAT_LIST_BG"] if i % 2 == 0 else theme["CHAT_LIST_BG_ALT"]
            self.chat_listbox.itemconfig(i, {'bg': bg, 'fg': theme["TEXT_COLOR"]})

        # 6. Chat Display
        self.chat_display.config(bg=theme["BG_COLOR"])
        
        # 7. Text Tags
        self.configure_tags()

        # 8. Refresh displayed chat to show new theme
        self.display_chat()


    def load_msgstore(self):
        path = filedialog.askopenfilename(title="Select msgstore.db", filetypes=[("Database files", "*.db")])
        if path:
            self.msgstore_path.delete(0, tk.END)
            self.msgstore_path.insert(0, path)

    def load_wa(self):
        path = filedialog.askopenfilename(title="Select wa.db", filetypes=[("Database files", "*.db")])
        if path:
            self.wa_path.delete(0, tk.END)
            self.wa_path.insert(0, path)

    def load_chats(self):
        msgstore_db_path = self.msgstore_path.get()
        wa_db_path = self.wa_path.get()

        if not msgstore_db_path or not os.path.exists(msgstore_db_path):
            messagebox.showerror("Error", "Please select a valid 'msgstore.db' file.")
            return

        try:
            # 1. Load Contacts (if wa.db is provided)
            if wa_db_path and os.path.exists(wa_db_path):
                print("[+] Loading contacts from wa.db")
                self.contacts_data = db_loader.query_contacts(wa_db_path)
            else:
                print("[-] No wa.db provided, contact names may be missing.")
                self.contacts_data = {}

            # 2. Load all chats and messages
            print("[+] Loading chats from msgstore.db")
            self.chats_data = db_loader.query_all_chats(msgstore_db_path, self.contacts_data)
            
            # 3. Populate the chat listbox
            self.chat_listbox.delete(0, tk.END)
            theme = self.current_theme
            for i, chat in enumerate(self.chats_data):
                if chat.messages: # Only show chats with messages
                    self.chat_listbox.insert(tk.END, f" {chat.title}")
                    # Set item background based on theme and striping
                    bg = theme["CHAT_LIST_BG"] if i % 2 == 0 else theme["CHAT_LIST_BG_ALT"]
                    self.chat_listbox.itemconfig(tk.END, {'bg': bg, 'fg': theme["TEXT_COLOR"]})

            print("[+] Finished loading!")
            if self.chat_listbox.size() > 0:
                self.chat_listbox.select_set(0)
                self.display_chat()  # <--- FIXED (was display__chat)
            else:
                messagebox.showinfo("Info", "No chats found in the database.")

        except Exception as e:
            messagebox.showerror("Loading Error", f"An error occurred while loading the database:\n{e}")
            print(f"[!] Error: {e}")

    def display_chat(self, event=None):
        try:
            selected_indices = self.chat_listbox.curselection()
            if not selected_indices:
                return
            
            selected_index = selected_indices[0]
            
            # Logic to find the correct chat since the listbox is filtered
            visible_chat_index = -1
            actual_chat_index = -1
            for i, chat in enumerate(self.chats_data):
                if chat.messages:
                    visible_chat_index += 1
                if visible_chat_index == selected_index:
                    actual_chat_index = i
                    break
            
            if actual_chat_index == -1:
                print(f"[!] Error: Could not find chat for index {selected_index}")
                return # Should not happen

            chat = self.chats_data[actual_chat_index]

            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)

            for m in chat.messages:
                # Determine message style
                style_tag = "sent" if m.key_from_me else "received"
                
                # Insert sender name (for group messages)
                if not m.key_from_me and m.remote_resource:
                    self.chat_display.insert(tk.END, f"{m.get_sender_name()}\n", ("sender", style_tag))
                
                # Insert message content
                content = m.get_content()
                self.chat_display.insert(tk.END, f"{content}\n", style_tag)
                
                # Insert timestamp
                self.chat_display.insert(tk.END, f"{m.received_timestamp_str}\n\n", ("time", style_tag))

            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.yview_moveto(1.0) # Scroll to bottom

        except Exception as e:
            messagebox.showerror("Display Error", f"An error occurred while displaying the chat:\n{e}")
            print(f"[!] Error displaying chat: {e}")


if __name__ == "__main__":
    app = WhatsAppViewerGUI()
    app.mainloop()