import customtkinter as ctk
import tkinter as tk
import psycopg2
import json
import os

conn = psycopg2.connect(
    dbname="notes_db",
    user="postgres",
    password="496284",
    host="localhost"
)
cursor = conn.cursor()

# Global Vars
font_size = 12
current_note_id = None
theme = "dark"
config_path = 'cfg/cfg.json'


def load_settings():
    global font_size, theme
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            font_size = config.get('font_size', 12)
            theme = config.get('theme', 'dark')

def save_settings():
    config = {'font_size': font_size, 'theme': theme}
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file)

def apply_theme():
    ctk.set_appearance_mode(theme)

def create_note():
    save_current_note()
    note_entry.delete("1.0", ctk.END)
    global current_note_id
    current_note_id = None

def save_current_note():
    global current_note_id
    note_content = note_entry.get("1.0", ctk.END).strip()
    if note_content:
        if current_note_id is None:
            cursor.execute("INSERT INTO notes (content) VALUES (%s)", (note_content,))
            conn.commit()
        else:
            cursor.execute("UPDATE notes SET content = %s WHERE id = %s", (note_content, current_note_id))
            conn.commit()

def save_note():
    save_current_note()
    load_notes()
    note_entry.delete("1.0", ctk.END)

def load_notes():
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    notes_list.delete(0, tk.END)
    for note in notes:
        notes_list.insert(tk.END, note[1])

def open_note(event):
    save_current_note()
    global current_note_id
    selected_index = notes_list.curselection()
    if selected_index:
        note_content = notes_list.get(selected_index)
        note_entry.delete("1.0", ctk.END)
        note_entry.insert("1.0", note_content)
        current_note_id = selected_index[0] + 1

def delete_note():
    selected_index = notes_list.curselection()
    if selected_index:
        note_content = notes_list.get(selected_index)
        cursor.execute("DELETE FROM notes WHERE content = %s", (note_content,))
        conn.commit()
        load_notes()
        note_entry.delete("1.0", ctk.END)

def open_settings():
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
    global theme
    theme = selected_theme
    apply_theme()
    save_settings()

def apply_settings(new_size):
    global font_size
    try:
        font_size = int(new_size)
        note_entry.configure(font=("JetBrains Mono", font_size))
        notes_list.configure(font=("JetBrains Mono", font_size))
        save_settings()
    except ValueError:
        pass

app = ctk.CTk()
app.title("Notes App")
load_settings()
apply_theme()

menu_frame = ctk.CTkFrame(app)
menu_frame.pack(side=ctk.LEFT, fill=ctk.Y)

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
