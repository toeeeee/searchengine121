import sqlite3

class SQLite:
    """Reduce boilerplate code for sqlite3"""

    def __init__(self, path: str):
        self.path = path

    def __enter__(self):
        self.connection: sqlite3.Connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        return self # for with ... as object_name

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()