# database.py
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Создает таблицу с 6 колонками"""
        with self.conn:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,        -- [0]
                username TEXT,                      -- [1]
                total_points REAL DEFAULT 0,        -- [2]
                daily_msg_points INTEGER DEFAULT 0, -- [3]
                daily_rxn_points REAL DEFAULT 0,    -- [4]
                last_update DATE                    -- [5]
            )''')

    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()

    def register_user(self, user_id, username):
        if not self.get_user(user_id):
            with self.conn:
                self.cursor.execute(
                    "INSERT INTO users (user_id, username, last_update) VALUES (?, ?, ?)",
                    (user_id, username, datetime.now().date())
                )
            return True
        return False

    def reset_daily_limits(self, user_id, today):
        with self.conn:
            self.cursor.execute(
                "UPDATE users SET daily_msg_points = 0, daily_rxn_points = 0, last_update = ? WHERE user_id = ?",
                (today, user_id)
            )

    def add_msg_point(self, user_id, new_total, new_daily_msg):
        with self.conn:
            self.cursor.execute(
                "UPDATE users SET total_points = ?, daily_msg_points = ? WHERE user_id = ?",
                (new_total, new_daily_msg, user_id)
            )

    def add_rxn_point(self, user_id, new_total, new_daily_rxn):
        with self.conn:
            self.cursor.execute(
                "UPDATE users SET total_points = ?, daily_rxn_points = ? WHERE user_id = ?",
                (new_total, new_daily_rxn, user_id)
            )

db = Database("moji_app.db")