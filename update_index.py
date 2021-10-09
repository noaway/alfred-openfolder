import os

from utils import Db
from os.path import expanduser

with Db() as (conn, cursor):
    cursor.execute(
        "create table if not exists dirs (root text not null, dir text not null, unique(root, dir))")
    conn.commit()

    for workspace in (expanduser(p) for p in os.getenv("workspaces").split(":")):
        for root, dirs, files in os.walk(workspace, topdown=True):
            if not root or not dirs:
                continue
            for dir in dirs:
                cursor.execute(
                    "insert or ignore into dirs (root, dir) values (?, ?)", (root, dir,))
            conn.commit()
