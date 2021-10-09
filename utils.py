import os
import sqlite3

from os.path import expanduser


class Db:
    def __init__(self):
        self.openfolder = expanduser(os.getenv("openfolder", "."))
        if not os.path.exists(self.openfolder):
            os.makedirs(self.openfolder)

    def __enter__(self):
        self.conn = sqlite3.connect(self.openfolder + "/index.db")
        self.conn.text_factory = str
        return self.conn, self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()
