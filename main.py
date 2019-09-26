#!/usr/bin/python
# encoding: utf-8

import sys
import os
import re

from workflow import Workflow3
from os.path import expanduser

# 返回 workspace 目录
def dir(workspace):
    for files in os.listdir(workspace):
        path = workspace+files
        if os.path.isdir(path):
            yield files

def main(wf):
    args = wf.args
    workspace,query = "",""
    if len(args)!=2:
        return
    for i in range(len(args)):
        if i == 0:
            # 将 ～ 转行 Home 目录
            workspace = expanduser(args[i])
        elif i == 1:
            query = str(args[i])
    
    if workspace and workspace[-1] != '/':
        workspace+='/'

    for d in dir(workspace):
        # 判断 query 是否是目录名前缀
        # 如果 query 是 / 返回全部目录
        if d.startswith(query.strip('/')) or query == "/":
            wf.add_item(title=d,arg=workspace+d,valid=True)
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))