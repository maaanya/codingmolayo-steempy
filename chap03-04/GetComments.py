from steem.account import Account
from datetime import datetime

a = Account('whoami') # 계정명 입력
comment_histories = list(a.get_account_history(index = -1, limit = 20, filter_by=['comment'], raw_output=True))
comment_histories = [ comment for comment in comment_histories if comment[1]['op'][1]['title'] == '' ]
comment_histories = [ comment for comment in comment_histories if comment[1]['op'][1]['author'] != 'maanya' ]

unique_permlink = []
happy_comments = []
for comment in comment_histories:
    if comment[1]['op'][1]['permlink'] not in unique_permlink:
        unique_permlink.append(comment[1]['op'][1]['permlink'])
        happy_comments.append(comment)

print('와! %d개의 고마운 댓글이 있어요.\n' % len(happy_comments))
for comment in happy_comments:
    print('작성자:', comment[1]['op'][1]['author'])
    print('작성시간:', datetime.strptime(comment[1]['timestamp'], '%Y-%m-%dT%H:%M:%S'))
    print('내용: ', comment[1]['op'][1]['body'])
    print('')




