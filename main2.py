import ctk
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
    notes_list.delete(0, ctk.END)
    for note in notes:
        notes_list.insert(ctk.END, note[1])

def edit_note():
    selected_note = notes_list.curselection()
    if selected_note:
        note_content = notes_list.get(selected_note)
        note_entry.delete(0, ctk.END)
        note_entry.insert(0, note_content)

app = ctk.CTk()
app.title("Notes")

note_entry = ctk.CTkEntry(app)
note_entry.pack()

create_button = ctk.CTkButton(app, text="Create note", command=create_note)
create_button.pack()

edit_button = ctk.CTkButton(app, text="Edit note", command=edit_note)
edit_button.pack()

notes_list = ctk.CTkListbox(app)
notes_list.pack()

load_notes()

app.mainloop()

conn.close()
