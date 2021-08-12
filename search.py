#!/usr/bin/python
# encoding: utf-8

import os
import re
import sys
import argparse

from workflow import Workflow3
from os.path import expanduser

# 返回 workspace 目录
def dirs(workspace, type):
    for files in os.listdir(workspace):
        path = workspace+files
        if type == "d" and os.path.isdir(path):
            yield files
        elif type == "f" and os.path.isfile(path):
            yield files
        elif not type or type == "":
            yield files

def main(wf):
    parser = argparse.ArgumentParser(description="搜索文件或目录。")
    parser.add_argument("query", metavar="query", type=str, help="查找的文件名。")
    parser.add_argument("-app", metavar="app", type=str, help="用于打开文件的 app 名字。")
    parser.add_argument("-workspace", dest="workspace", required=True, help="在指定的目录下搜索。")
    parser.add_argument("-type",dest="type", help="搜索类型，如果是文件参数为f 如果搜索目录参数是 d。")
    args = parser.parse_args()
    args.workspace = expanduser(args.workspace)

    if args.workspace and args.workspace[-1] != '/':
        args.workspace+='/'

    wf.setvar(name="app_name", value=args.app)
    for dir in dirs(args.workspace,args.type):
        # 判断 query 是否是目录名前缀
        # 如果 query 是 / 返回全部目录
        if re.search(args.query.strip('/'), dir) is not None:
            wf.add_item(title=dir, arg=args.workspace + dir, valid=True)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))