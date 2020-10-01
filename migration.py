#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import os
import sys

if __name__ == '__main__':
    if (int(sys.version_info[0]) * 10 + int(sys.version_info[1])) >= 38:
        python = sys.executable
        os.system(f'{python} {os.path.join(os.path.dirname(__file__), "manage.py")} makemigrations user')
        os.system(f'{python} {os.path.join(os.path.dirname(__file__), "manage.py")} migrate user')
        os.system(f'{python} {os.path.join(os.path.dirname(__file__), "manage.py")} makemigrations')
        os.system(f'{python} {os.path.join(os.path.dirname(__file__), "manage.py")} migrate')
        exit()
    print('当前使用的 Python 版本小于 3.8')
