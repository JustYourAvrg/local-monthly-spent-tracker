import sqlite3


class dataManagement:
    def __init__(self):
        self.db = sqlite3.connect('data/database.db')
        self.cur = self.db.cursor()
    

    def setup(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS total_spent (
                id INTEGER PRIMARY KEY,
                spent FLOAT DEFAULT 0,
                month TEXT
        )""")
    

    def execute_query(self, query: str, params: tuple):
        self.cur.execute(query, params)
        self.db.commit()

        return self.cur.fetchall()
