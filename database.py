import sqlite3


class Database:
    def __init__(self, db_name="todo.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL UNIQUE, 
            user_name TEXT NOT NULL, 
            first_name TEXT NOT NULL, 
            language TEXT NOT NULL
        );""")
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_chat_id INTEGER,
            task_name TEXT NOT NULL,
            task_time TEXT NOT NULL,
            FOREIGN KEY(user_chat_id) REFERENCES users(chat_id)
        );""")
        self.conn.commit()

    def create_user(self, first_name, username, lang, chat_id):
        try:
            self.cur.execute("""
                INSERT INTO to_do (first_name, user_name, language, chat_id)
                VALUES (?, ?, ?, ?)""", (first_name, username, lang, chat_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating user: {e}")

    def get_user_by_chat_id(self, chat_id):
        try:
            self.cur.execute("SELECT * FROM to_do WHERE chat_id = ?", (chat_id,))
            user = self.cur.fetchone()
            return user
        except sqlite3.Error as e:
            print(f"Error fetching user: {e}")
            return None

    def update_user_language(self, chat_id, new_language):
        try:
            self.cur.execute("UPDATE to_do SET language = ? WHERE chat_id = ?", (new_language, chat_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating language: {e}")

    def add_task(self, user_chat_id, task_name, task_time):
        try:
            self.cur.execute("""
                INSERT INTO tasks (user_chat_id, task_name, task_time)
                VALUES (?, ?, ?)""", (user_chat_id, task_name, task_time))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding task: {e}")

    def get_tasks_by_chat_id(self, user_chat_id):
        try:
            self.cur.execute("""
                SELECT tasks.id, tasks.task_name, tasks.task_time
                FROM tasks
                JOIN users ON tasks.user_chat_id = users.chat_id
                WHERE users.chat_id = ?
            """, (user_chat_id,))
            tasks = self.cur.fetchall()
            return tasks
        except sqlite3.Error as e:
            print(f"Error fetching tasks: {e}")
            return []

    def remove_task(self, task_id):
        try:
            self.cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error removing task: {e}")

    def close(self):
        self.conn.close()
