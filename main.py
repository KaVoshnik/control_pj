import customtkinter as ctk
import tkinter as tk
import psycopg2
import json
import os

# Database connection
conn = psycopg2.connect(
    dbname="notes_db",
    user="postgres",
    password="496284",
    host="localhost"
)
cursor = conn.cursor()

def create_notes_table():
    """Create the notes table if it doesn't exist."""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id SERIAL PRIMARY KEY,
        content TEXT NOT NULL
    )
    """)
    conn.commit()

create_notes_table()

# Global Vars
font_size = 12  # Font size
current_note_id = None  # Note Id for use in code
theme = "dark"  # Default theme
config_path = 'config/cfg.json'  # Config folder path
sort_order = "id_asc"  # Id sort

def load_settings():
    """Load user settings from a configuration file."""
    global font_size, theme
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            font_size = config.get('font_size', 12)
            theme = config.get('theme', 'dark')

def save_settings():
    """Save user settings to a configuration file."""
    config = {'font_size': font_size, 'theme': theme}
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file)

def apply_theme():
    """Apply the selected theme."""
    ctk.set_appearance_mode(theme)

def create_note():
    """Prepare to create a new note."""
    save_current_note()
    note_entry.delete("1.0", ctk.END)
    global current_note_id
    current_note_id = None

def save_current_note():
    """Save the current note to the database."""
    global current_note_id
    note_content = note_entry.get("1.0", ctk.END).strip()
    if note_content:
        try:
            if current_note_id is None:
                cursor.execute("INSERT INTO notes (content) VALUES (%s)", (note_content,))
            else:
                cursor.execute("UPDATE notes SET content = %s WHERE id = %s", (note_content, current_note_id))
            conn.commit()
        except Exception as e:
            print(f"Error saving note: {e}")

def save_note():
    """Save the current note and reload the notes list."""
    save_current_note()
    load_notes()
    note_entry.delete("1.0", ctk.END)

def load_notes():
    """Load notes from the database and display them in the listbox."""
    global sort_order
    if sort_order == "id_asc":
        cursor.execute("SELECT * FROM notes ORDER BY id ASC")
    elif sort_order == "id_desc":
        cursor.execute("SELECT * FROM notes ORDER BY id DESC")

    notes = cursor.fetchall()
    notes_list.delete(0, tk.END)
    for note in notes:
        notes_list.insert(tk.END, (note[0], note[1]))

def open_note(event):
    """Open the selected note for editing."""
    save_current_note()
    global current_note_id
    selected_index = notes_list.curselection()
    if selected_index:
        note_id, note_content = notes_list.get(selected_index)
        note_entry.delete("1.0", ctk.END)
        note_entry.insert("1.0", note_content)
        current_note_id = note_id

def delete_note():
    """Delete the selected note from the database."""
    selected_index = notes_list.curselection()
    if selected_index:
        note_id, note_content = notes_list.get(selected_index)
        cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
        conn.commit()
        load_notes()
        note_entry.delete("1.0", ctk.END)

def open_settings():
    """Open the settings window for user preferences."""
    settings_window = ctk.CTkToplevel(app)
    settings_window.title("Settings")
    
    font_size_label = ctk.CTkLabel(settings_window, text="Font size:")
    font_size_label.pack(padx=10, pady=10)

    font_size_entry = ctk.CTkEntry(settings_window)
    font_size_entry.insert(0, str(font_size))
    font_size_entry.pack(padx=10, pady=10)

    theme_label = ctk.CTkLabel(settings_window, text="Themes:")
    theme_label.pack(padx=10, pady=10)

    theme_var = tk.StringVar(value=theme)
    dark_theme_radio = ctk.CTkRadioButton(settings_window, text="Dark", variable=theme_var, value="dark", command=lambda: set_theme(theme_var.get()))
    dark_theme_radio.pack(padx=10, pady=5)

    light_theme_radio = ctk.CTkRadioButton(settings_window, text="Light", variable=theme_var, value="light", command=lambda: set_theme(theme_var.get()))
    light_theme_radio.pack(padx=10, pady=5)

    apply_button = ctk.CTkButton(settings_window, text="Apply", command=lambda: apply_settings(font_size_entry.get()))
    apply_button.pack(pady=10)

def set_theme(selected_theme):
    """Set the application theme."""
    global theme
    theme = selected_theme
    apply_theme()
    save_settings()

def apply_settings(new_size):
    """Apply the new font size."""
    global font_size
    try:
        font_size = int(new_size)
        note_entry.configure(font=("JetBrains Mono", font_size))
        notes_list.configure(font=("JetBrains Mono", font_size))
        save_settings()
    except ValueError:
        pass

def change_sort_order(new_order):
    """Change the sort order of the notes."""
    global sort_order
    sort_order = new_order
    load_notes()

app = ctk.CTk()
app.title("Notes App")
load_settings()
apply_theme()

menu_frame = ctk.CTkFrame(app)
menu_frame.pack(side=ctk.LEFT, fill=ctk.Y)

sort_menu = ctk.CTkOptionMenu(menu_frame, 
                                values=["Sort by ID (Ascending)", "Sort by ID (Descending)"],
                                command=lambda value: change_sort_order(value.split()[2].lower() + ("_asc" if "Ascending" in value else "_desc")))
sort_menu.pack(padx=10, pady=10)

notes_list = tk.Listbox(menu_frame, height=20, font=("JetBrains Mono", font_size))
notes_list.pack(padx=10, pady=10)

create_button = ctk.CTkButton(menu_frame, text="Create note", command=create_note)
create_button.pack(pady=5)

save_button = ctk.CTkButton(menu_frame, text="Save note", command=save_note)
save_button.pack(pady=5)

delete_button = ctk.CTkButton(menu_frame, text="Delete note", command=delete_note)
delete_button.pack(pady=5)

settings_button = ctk.CTkButton(menu_frame, text="Settings", command=open_settings)
settings_button.pack(pady=5)

note_entry = ctk.CTkTextbox(app, width=400, height=300, font=("JetBrains Mono", font_size))
note_entry.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=20, pady=20)

notes_list.bind('<<ListboxSelect>>', open_note)

load_notes()

app.mainloop()

conn.close()
