from database import Database

class NotesManager:
    def __init__(self):
        self.db = Database(dbname="notes_db", user="postgres", password="496284", host="localhost")
        self.current_note_id = None
        self.sort_order = "id_asc"

    def create_note(self):
        self.save_current_note()
        self.current_note_id = None

    def save_current_note(self, note_content):
        if note_content:
            if self.current_note_id is None:
                self.db.execute("INSERT INTO notes (content) VALUES (%s)", (note_content,))
            else:
                self.db.execute("UPDATE notes SET content = %s WHERE id = %s", (note_content, self.current_note_id))

    def save_note(self, note_content):
        self.save_current_note(note_content)
        self.load_notes()

    def load_notes(self, notes_list):
        query = "SELECT * FROM notes ORDER BY id ASC" if self.sort_order == "id_asc" else "SELECT * FROM notes ORDER BY id DESC"
        notes = self.db.fetchall(query)
        notes_list.delete(0, tk.END)
        for note in notes:
            notes_list.insert(tk.END, (note[0], note[1]))

    def open_note(self, event, notes_list, note_entry):
        self.save_current_note(note_entry.get("1.0", tk.END).strip())
        selected_index = notes_list.curselection()
        if selected_index:
            note_id, note_content = notes_list.get(selected_index)
            note_entry.delete("1.0", tk.END)
            note_entry.insert("1.0", note_content)
            self.current_note_id = note_id

    def delete_note(self, note_id):
        if note_id:
            self.db.execute("DELETE FROM notes WHERE id = %s", (note_id,))
            self.load_notes()

    def change_sort_order(self, new_order):
        self.sort_order = new_order
        self.load_notes()
