#!/usr/bin/python
# encoding: utf-8

import os
import re
import sys
import argparse

from workflow import Workflow3
from os.path import expanduser


def dirs(workspace, type):
    # 返回 workspace 目录
    for files in os.listdir(workspace):
        path = workspace + files
        if type == "d" and os.path.isdir(path):
            yield files
        elif type == "f" and os.path.isfile(path):
            yield files
        elif not type or type == "":
            yield files


def add_error_item(wf, title):
    wf.add_item(title=title, valid=True)
    wf.send_feedback()


def main(wf):
    parser = argparse.ArgumentParser(description="搜索文件或目录。")
    parser.add_argument("query", metavar="query", type=str, help="查找的文件名。")
    parser.add_argument("-app", metavar="app", type=str,
                        help="用于打开文件的 app 名字。")
    parser.add_argument("-type", dest="type",
                        help="搜索类型，如果是文件参数为f 如果搜索目录参数是 d。")
    args = parser.parse_args()

    wf.setvar(name="app_name", value=args.app)

    wp_path = os.getenv("workspaces")
    if not wp_path:
        add_error_item(wf, "缺少 workspaces 环境变量。")
        return

    workspaces = [p if p[-1] == "/" else p + "/" for p in (expanduser(p)
                  for p in wp_path.split(":")) if os.path.exists(p)]

    if len(workspaces) == 0:
        add_error_item(wf, "workspaces 路径不合法。")
        return

    has_item = False
    query = args.query.strip('/')

    for workspace in workspaces:
        for dir in dirs(workspace, args.type):
            # 如果 query 是 / 返回全部目录
            if re.search(query, dir) is not None:
                if not has_item:
                    has_item = True
                ap = workspace + dir
                wf.add_item(title=dir, arg=ap, subtitle=ap, valid=True)

    if not has_item:
        wf.add_item(title="未找到目录" + query, valid=True)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
