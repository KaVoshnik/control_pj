import psycopg2
from datetime import datetime
import customtkinter as ctk

DB_HOST = "localhost"
DB_NAME = "task_manager"
DB_USER = "postgres"
DB_PASS = "496284"

def connect_db():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

def add_task(title, description, deadline, priority):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, deadline, priority) VALUES (%s, %s, %s, %s)",
                   (title, description, deadline, priority))
    conn.commit()
    cursor.close()
    conn.close()

def get_tasks():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

def update_task(task_id, title, description, deadline, priority, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title=%s, description=%s, deadline=%s, priority=%s, status=%s WHERE id=%s",
                   (title, description, deadline, priority, status, task_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()

# Графический интерфейс
class TaskManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager")
        self.geometry("600x400")
        
        # Установка темной темы
        ctk.set_appearance_mode("dark")  # Устанавливаем темный режим
        ctk.set_default_color_theme("dark-blue")  # Устанавливаем цветовую тему

        # Установка шрифта JetBrains Mono
        ctk.CTkFont(family="JetBrains Mono", size=12)

        self.task_textbox = ctk.CTkTextbox(self, fg_color="#2E2E2E", text_color="white", font=("JetBrains Mono", 12))
        self.task_textbox.pack(fill="both", expand=True)

        self.load_tasks()

        self.title_entry = ctk.CTkEntry(self, placeholder_text="Title", fg_color="#3E3E3E", text_color="white", font=("JetBrains Mono", 12))
        self.title_entry.pack(pady=5)

        self.description_entry = ctk.CTkEntry(self, placeholder_text="Description", fg_color="#3E3E3E", text_color="white", font=("JetBrains Mono", 12))
        self.description_entry.pack(pady=5)

        self.deadline_entry = ctk.CTkEntry(self, placeholder_text="Deadline (YYYY-MM-DD HH:MM:SS)", fg_color="#3E3E3E", text_color="white", font=("JetBrains Mono", 12))
        self.deadline_entry.pack(pady=5)

        self.priority_entry = ctk.CTkEntry(self, placeholder_text="Priority", fg_color="#3E3E3E", text_color="white", font=("JetBrains Mono", 12))
        self.priority_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(self, text="Add Task", command=self.add_task, font=("JetBrains Mono", 12))
        self.add_button.pack(pady=5)

        self.update_button = ctk.CTkButton(self, text="Update Task", command=self.update_task, font=("JetBrains Mono", 12))
        self.update_button.pack(pady=5)

        self.delete_button = ctk.CTkButton(self, text="Delete Task", command=self.delete_task, font=("JetBrains Mono", 12))
        self.delete_button.pack(pady=5)

    def load_tasks(self):
        self.task_textbox.delete("1.0", ctk.END)
        tasks = get_tasks()
        for task in tasks:
            self.task_textbox.insert(ctk.END, f"{task[0]}: {task[1]} - {task[4]}\n")

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        deadline = self.deadline_entry.get()
        priority = self.priority_entry.get()
        add_task(title, description, deadline, priority)
        self.load_tasks()

    def update_task(self):
        selected_task = self.task_textbox.get("1.0", ctk.END).strip().split("\n")
        if selected_task:
            task_id = int(selected_task[0].split(":")[0])
            title = self.title_entry.get()
            description = self.description_entry.get()
            deadline = self.deadline_entry.get()
            priority = self.priority_entry.get()
            update_task(task_id, title, description, deadline, priority, "в процессе")
            self.load_tasks()

    def delete_task(self):
        selected_task = self.task_textbox.get("1.0", ctk.END).strip().split("\n")
        if selected_task:
            task_id = int(selected_task[0].split(":")[0])
            delete_task(task_id)
            self.load_tasks()

if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()
