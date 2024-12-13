import customtkinter as ctk
from ui import create_ui
from settings import load_settings, apply_theme

def main():
    load_settings()
    app = ctk.CTk()
    app.title("Notes App")
    apply_theme()
    
    create_ui(app)
    
    app.mainloop()

if __name__ == "__main__":
    main()
