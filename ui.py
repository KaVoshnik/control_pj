import customtkinter as ctk
import tkinter as tk
from notes_manager import NotesManager
from settings import open_settings

def create_ui(app):
    menu_frame = ctk.CTkFrame(app)
    menu_frame.pack(side=ctk.LEFT, fill=ctk.Y)

    notes_manager = NotesManager()

    sort_menu = ctk.CTkOptionMenu(menu_frame, 
                                    values=["Sort by ID (Ascending)", "Sort by ID (Descending)"],
                                    command=lambda value: notes_manager.change_sort_order(value.split()[2].lower() + ("_asc" if "Ascending" in value else "_desc")))
    sort_menu.pack(padx=10, pady=10)

    notes_list = tk.Listbox(menu_frame, height=20, font=("JetBrains Mono", 12))
    notes_list.pack(padx=10, pady=10)

    create_button = ctk.CTkButton(menu_frame, text="Create note", command=notes_manager.create_note)
    create_button.pack(pady=5)

    save_button = ctk.CTkButton(menu_frame, text="Save note", command=notes_manager.save_note)
    save_button.pack(pady=5)

    delete_button = ctk.CTkButton(menu_frame, text="Delete note", command=notes_manager.delete_note)
    delete_button.pack(pady=5)

    settings_button = ctk.CTkButton(menu_frame, text="Settings", command=open_settings)
    settings_button.pack(pady=5)

    note_entry = ctk.CTkTextbox(app, width=400, height=300, font=("JetBrains Mono", 12))
    note_entry.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=20, pady=20)

    notes_list.bind('<<ListboxSelect>>', lambda event: notes_manager.open_note(event, notes_list, note_entry))

    notes_manager.load_notes(notes_list)
