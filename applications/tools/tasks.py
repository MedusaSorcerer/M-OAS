#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import os
import time

import schedule


def remove_extra_files():
    from .tools import cache, NAME, BASE_DIR, CACHE_TIMEOUT

    tools, delete, pop = cache.get(NAME, {}), [], []
    now = time.time()
    for k, v in tools.items():
        if now - v['timeout'] > CACHE_TIMEOUT:
            delete.append(v['name'])
            pop.append(k)
    for root, dirs, files in os.walk(os.path.join(BASE_DIR, 'applications', 'tools', 'tf')):
        cache_file = [i['name'] for i in tools.values()]
        for i in files:
            if (name := i[1:-3]) not in cache_file:
                delete.append(name)
    for i in delete:
        try:
            os.remove(os.path.join(BASE_DIR, 'applications', 'tools', 'tf', f'M{i}.py'))
        except Exception as e:
            print(i, e)
    for i in pop:
        tools.pop(i, '')
    cache.set(NAME, tools, timeout=CACHE_TIMEOUT)


schedule.every().day.at("05:30").do(remove_extra_files)
