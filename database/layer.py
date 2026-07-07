import sqlite3
import json

class DB:

    def __init__(self, path="ai_platform.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._init()

    def _init(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            type TEXT,
            data TEXT
        )
        """)
        self.conn.commit()

    def save(self, type_, data):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO logs (type, data) VALUES (?, ?)",
            (type_, json.dumps(data))
        )
        self.conn.commit()
