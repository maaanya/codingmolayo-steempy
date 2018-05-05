from steem.account import Account
from steem.post import Post
from steem import Steem
import time

acc_name = 'maanyabot'
pkey = 'postkey'
steem = Steem(keys=pkey, nodes=['https://api.steemit.com'])
acc = Account(acc_name)

voted_permlink = []

# 봇 실행 당시 가장 최근의 기록 번호를 seq_num에 저장
past_seq_num = list(acc.get_account_history(index=-1, limit=2, raw_output=True))[0][0]

while True:
    # 최근 댓글 확인
    recent_seq_num = list(acc.get_account_history(index=-1, limit=2, raw_output=True))[0][0]

    # 봇이 확인한 이후에 최근 댓글이 있으면 동작
    if recent_seq_num > past_seq_num:
        comment_histories = list(
            acc.get_account_history(index=-1, limit=recent_seq_num - past_seq_num, raw_output=True))
        replies = [comment for comment in comment_histories if comment[1]['op'][0] == 'comment' and
                   comment[1]['op'][1]['title'] == '' and comment[1]['op'][1]['author'] != 'maanyabot']

        for reply in replies:
            if reply[1]['op'][1]['permlink'] in voted_permlink:
                pass

            reply_post = None

            # 대댓글 달기
            try:
                reply_post = Post('@' + reply[1]['op'][1]['author'] + '/' + reply[1]['op'][1]['permlink'])
            except Exception as e:
                pass

            while (True):
                try:
                    reply_post.reply(body="금손봇", author=acc_name)
                    break
                except Exception as e:
                    print(e)
                    time.sleep(17)

            # 보팅하기
            reply_post.upvote(10, acc_name)

            # 대댓글과 보팅한 댓글을 저장
            voted_permlink.insert(0, reply[1]['op'][1]['permlink'])

        # 확인 기록(past_seq_num) 갱신
        past_seq_num = recent_seq_num
        print(voted_permlink)

    # 적절한 휴식
    print(recent_seq_num, past_seq_num)
    time.sleep(3)