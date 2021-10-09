#!/usr/bin/python
# encoding: utf-8

import os
import argparse

from utils import Db
from os.path import expanduser


def create_index():
    with Db() as (conn, cursor):
        for workspace in (expanduser(p) for p in os.getenv("workspaces", "~/Desktop").split(":")):
            if not os.path.exists(workspace):
                continue

            for root, dirs, files in os.walk(workspace, topdown=True):
                if not root or not dirs:
                    continue
                for dir in dirs:
                    cursor.execute(
                        "insert or ignore into dirs (root, dir, priority) values (?, ?, 0)", (root, dir,))
                conn.commit()


def update_priority(path):
    root = os.path.dirname(path)
    dir = os.path.basename(path)
    if not root or not dir:
        return

    with Db() as (conn, cursor):
        cursor.execute(
            "select * from dirs where root = ? and dir = ?", (root, dir,))
        ret = cursor.fetchone()
        if not ret:
            return
        _, _, priority = ret
        cursor.execute(
            "update dirs set priority = ? where root = ? and dir = ?", (priority + 1, root, dir,))
        conn.commit()


def main(args):
    if args.type[0] == "create_index":
        create_index()
        return

    if len(args.type) == 2 and args.type[0] == "update_priority":
        update_priority(args.type[1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="修改索引。")
    parser.add_argument("type", nargs="+", help="操作类型。")
    main(parser.parse_args())
