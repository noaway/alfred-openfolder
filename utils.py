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
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            "create table if not exists dirs (root text not null, dir text not null, priority integer not null, unique(root, dir))")
        self.conn.commit()

        return self.conn, self.cursor

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()
