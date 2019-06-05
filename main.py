#!/usr/bin/python
# encoding: utf-8

import sys
import os
import re

from workflow import Workflow3

def dir(workspace):
    for files in os.listdir(workspace):
        path = workspace+files
        if os.path.isdir(path):
            yield files

def main(wf):
    args = wf.args
    workspace = ""
    query = ""
    if len(args)!=2:
        return
    for i in range(len(args)):
        if i == 0:
            workspace = str(args[i])
        elif i == 1:
            query = str(args[i])

    if len(args)>0:
        for d in dir(workspace):
            if d.startswith(query):
                wf.add_item(title=d,arg=workspace+d,valid=True)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))

