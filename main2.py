import customtkinter as ctk
import psycopg2

conn = psycopg2.connect(
    dbname="notes_db",
    user="postgres",
    password="496284",
    host="localhost"
)
cursor = conn.cursor()

def create_note():
    note_content = note_entry.get()
    if note_content:
        cursor.execute("INSERT INTO notes (content) VALUES (%s)", (note_content,))
        conn.commit()
        note_entry.delete(0, ctk.END)
        load_notes()

def load_notes():
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    notes_display.delete(1.0, ctk.END)
    for note in notes:
        notes_display.insert(ctk.END, note[1] + "\n")
def edit_note():
    selected_note = notes_display.get("1.0", ctk.END).strip().split("\n")
    if selected_note:
        note_content = selected_note[-1]
        note_entry.delete(0, ctk.END)
        note_entry.insert(0, note_content)

app = ctk.CTk()
app.title("Notes App")

note_entry = ctk.CTkEntry(app)
note_entry.pack()

create_button = ctk.CTkButton(app, text="Create note", command=create_note)
create_button.pack()

edit_button = ctk.CTkButton(app, text="Edit note", command=edit_note)
edit_button.pack()

notes_display = ctk.CTkTextbox(app, height=10)
notes_display.pack()

load_notes()

app.mainloop()

conn.close()
