from tkinter import *
from tkinter import messagebox
import sqlite3


def add_task():
    """Adds a new task to the list and database."""
    task = task_entry.get().strip()
    if not task:
        messagebox.showwarning("Error", "Task field is empty.")
        return

    tasks.append(task)
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (task,))
    update_task_list()
    task_entry.delete(0, END)


def update_task_list():
    """Refreshes the task list in the Listbox."""
    task_listbox.delete(0, END)
    for task in tasks:
        task_listbox.insert(END, task)


def delete_task():
    """Deletes the selected task from the list and database."""
    try:
        selected_task = task_listbox.get(task_listbox.curselection())
        tasks.remove(selected_task)
        cursor.execute("DELETE FROM tasks WHERE title = ?", (selected_task,))
        update_task_list()
    except TclError:
        messagebox.showwarning("Error", "No task selected for deletion.")


def delete_all_tasks():
    """Deletes all tasks after confirmation."""
    if messagebox.askyesno("Delete All", "Are you sure you want to delete all tasks?"):
        tasks.clear()
        cursor.execute("DELETE FROM tasks")
        update_task_list()


def close_app():
    """Closes the app and saves the database."""
    connection.commit()
    cursor.close()
    root.destroy()


def load_tasks_from_db():
    """Loads tasks from the database into the list."""
    cursor.execute("SELECT title FROM tasks")
    tasks.extend([row[0] for row in cursor.fetchall()])
    update_task_list()


if __name__ == "__main__":
    # Initialize the application window
    root = Tk()
    root.title("To-Do List")
    root.geometry("700x450+500+200")
    root.configure(bg="#F0F8FF")
    root.resizable(0, 0)

    # Database connection setup
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (title TEXT)")
    tasks = []

    # Task input and buttons
    Label(
        root,
        text="📝 TO-DO LIST",
        font=("Arial", 18, "bold"),
        bg="#4682B4",
        fg="white",
        padx=10,
        pady=10
    ).pack(fill=X)

    input_frame = Frame(root, bg="#F0F8FF", pady=10)
    input_frame.pack()

    Label(
        input_frame,
        text="Enter Task:",
        font=("Arial", 14),
        bg="#F0F8FF",
        fg="#333"
    ).grid(row=0, column=0, padx=10, pady=5)

    task_entry = Entry(input_frame, font=("Arial", 14), width=35, bg="#FFFFFF", fg="#333")
    task_entry.grid(row=0, column=1, padx=10, pady=5)

    Button(input_frame, text="Add Task", width=12, bg="#32CD32", fg="white", font=("Arial", 12, "bold"),
           command=add_task).grid(row=0, column=2, padx=10, pady=5)

    # Task list display
    task_frame = Frame(root, bg="#F0F8FF")
    task_frame.pack(pady=10)

    task_listbox = Listbox(
        task_frame,
        width=60,
        height=12,
        font=("Arial", 12),
        bg="#FFFFFF",
        fg="#333",
        selectbackground="#FFD700",
        selectforeground="black",
        highlightbackground="#4682B4",
        highlightthickness=1
    )
    task_listbox.pack(side=LEFT, padx=10)

    scrollbar = Scrollbar(task_frame, orient=VERTICAL, command=task_listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    task_listbox.config(yscrollcommand=scrollbar.set)

    # Action buttons
    button_frame = Frame(root, bg="#F0F8FF", pady=10)
    button_frame.pack()

    Button(button_frame, text="Remove Task", width=15, bg="#FF4500", fg="white", font=("Arial", 12, "bold"),
           command=delete_task).grid(row=0, column=0, padx=10, pady=5)
    Button(button_frame, text="Delete All", width=15, bg="#FF6347", fg="white", font=("Arial", 12, "bold"),
           command=delete_all_tasks).grid(row=0, column=1, padx=10, pady=5)
    Button(button_frame, text="Close App", width=15, bg="#4682B4", fg="white", font=("Arial", 12, "bold"),
           command=close_app).grid(row=0, column=2, padx=10, pady=5)

    # Load tasks from database and update the list
    load_tasks_from_db()

    # Start the main application loop
    root.mainloop()
