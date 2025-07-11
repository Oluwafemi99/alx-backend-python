import sqlite3


class ExecuteQuery:
    def __init__(self, query, params=()):
        self.query = query
        self.params = params
        self.conn = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect('user_db')
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        for row in self.result:
            return row

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            print('closing database')
            self.conn.close()
        if exc_val:
            return False


with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25)) as result:
    print(f'results:{result}')
