#!/usr/bin/python
# encoding: utf-8

import os
import sys
import sqlite3
import argparse

from utils import Db
from workflow import Workflow3
from workflow.background import run_in_background


def search(wf, query):
    with Db() as (_, cursor):
        try:
            cursor.execute(
                "select * from dirs where dir like ? order by priority desc, length(root) limit 30", ("%{}%".format(query),))
        except sqlite3.OperationalError as e:
            print(e)

        for root, dir, _ in cursor.fetchall():
            if not os.path.exists("{}/{}".format(root, dir)):
                cursor.execute(
                    "delete from dirs where root = ? and dir = ?", (root, dir,))
                continue
            ap = "{}/{}".format(root, dir)
            wf.add_item(title=dir, arg=ap, subtitle=ap, valid=True)
        wf.send_feedback()


def main(wf):
    parser = argparse.ArgumentParser(description="搜索文件或目录。")
    parser.add_argument("query", metavar="query", type=str, help="查找的文件名。")
    parser.add_argument("-app", metavar="app", type=str,
                        help="用于打开文件的 app 名字。")
    args = parser.parse_args()

    run_in_background(
        "update_index", ["/usr/bin/python", wf.workflowfile("index.py"), "create_index"])
    wf.setvar(name="app_name", value=args.app)
    search(wf, args.query.strip('/'))


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
