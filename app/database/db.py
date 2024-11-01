class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)

    def close(self):
        self.connection.close()