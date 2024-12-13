import json
import os
import customtkinter as ctk

config_path = 'cfg/cfg.json'

def load_settings():
    global font_size, theme
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            font_size = config.get('font_size', 12)
            theme = config.get('theme', 'dark')

def save_settings(font_size, theme):
    config = {'font_size': font_size, 'theme': theme}
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file)

def apply_theme():
    ctk.set_appearance_mode(theme)

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
    save_settings(font_size, theme)

def apply_settings(new_size):
    global font_size
    try:
        font_size = int(new_size)
        note_entry.configure(font=("JetBrains Mono", font_size))
        notes_list.configure(font=("JetBrains Mono", font_size))
        save_settings(font_size, theme)
    except ValueError:
        pass
