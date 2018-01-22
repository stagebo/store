#!/usr/bin/env python
from __future__ import print_function

from tornado import ioloop, gen
from tornado_mysql import pools


pools.DEBUG = True


POOL = pools.Pool(
    dict(host='127.0.0.1', port=3306, user='root', passwd='root', db='pyweb'),
    max_idle_connections=1,
    max_recycle_sec=3)


@gen.coroutine
def worker(n):
    for i in range(10):
        t = 1
        print(n, "sleeping", t, "seconds")
        cur = yield POOL.execute("SELECT * from t_jieba")
        print(n, cur.fetchall())


@gen.coroutine
def main():
    workers = [worker(i) for i in range(10)]
    print(workers)
    yield workers


ioloop.IOLoop.current().run_sync(main)
print("numbers:",POOL._opened_conns)