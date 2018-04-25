from multiprocessing import Process
from multiprocessing import Manager
from contextlib import suppress
import json
import gevent.monkey
import requests
import time
from steem.steemd import Steemd

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
    return blocks

def get_replies_from_blocks(blocks):
    # 코멘트 읽는 부분
    procs = []
    replies = Manager().list()
    for block in blocks:
        proc = Process(target=filter_reply, args=(block, replies))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
    print(procs)
    return sum(replies, [])

def filter_reply(block, replies):
    replies.append([comment for comment in block if comment['op'][0] == 'comment'
                and comment['op'][1]['parent_author'] != ''])

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
            # 블록에서 댓글(reply)만 가져오는 처리
            recent_blocks = read_block(start_block_num, last_block_num)
            replies = get_replies_from_blocks(recent_blocks)

            for reply in replies:
                print(reply)

            # 블록 번호 갱신
            start_block_num = last_block_num
            last_block_num = s.head_block_number