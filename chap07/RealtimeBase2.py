from multiprocessing import Process
from contextlib import suppress
import json
import gevent.monkey
from steem.steemd import Steemd
import requests
import time

def read_block(start_block_num, last_block_num):
    # 블록 가져오는 부분
    blocks = []
    threads = []
    print(start_block_num, last_block_num)
    gevent.monkey.patch_all()
    for block in range(start_block_num, last_block_num):
        threads.append(
            gevent.spawn(blocks.append(get_block(block))))
    gevent.joinall(threads)

    # 코멘트 읽는 부분
    procs = []
    for block in blocks:
        proc = Process(target=read_post, args=(block,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

def read_post(block):
    comments = [comment for comment in block if comment['op'][0] == 'comment'
                and comment['op'][1]['parent_author'] != '']

    for comment in comments:
        print(comment)

def get_block(block_num):
    req = json.dumps(
        {"jsonrpc": "2.0", "id": 0, "method": "call",
         "params": [0, "get_ops_in_block", [block_num, False]]})
    res = requests.post('https://api.steemit.com', data=req).json()['result']
    return res

if __name__ == '__main__':
    s = Steemd(nodes=["https://api.steemit.com"])
    start_block_num = s.head_block_number
    time.sleep(7)
    last_block_num = s.head_block_number

    with suppress(KeyboardInterrupt):
        while True:
            read_block(start_block_num, last_block_num)
            start_block_num = last_block_num
            last_block_num = s.head_block_number