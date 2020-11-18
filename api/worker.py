import os

import redis
from rq import Worker, Queue, Connection

listen = ['default']

redis_url = 'redis://redistogo:fd695f70a5a774bdef9f6fb0a3cae2bb@pike.redistogo.com:11607/'#'redis://localhost:6379'

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()