from steem import Steem
from steem.account import Account
from steem.converter import Converter
import re

username = 'whoami' # 계정명 입력
s = Steem(nodes=["https://api.steemit.com"])
converter = Converter(steemd_instance=s)

a = Account(username)
histories = list(a.get_account_history(index = -1, limit = 5300, filter_by='claim_reward_balance', raw_output=True))

sum_steem = 0
sum_sbd = 0
sum_sp = 0

for history in histories:
    steem = history[1]['op'][1]['reward_steem']
    steem = float(re.findall("([0-9]+(?:\.[0-9]+)?)(?:\s)", steem)[0])

    sbd = history[1]['op'][1]['reward_sbd']
    sbd = float(re.findall("([0-9]+(?:\.[0-9]+)?)(?:\s)", sbd)[0])

    sp = history[1]['op'][1]['reward_vests']
    sp = float(re.findall("([0-9]+(?:\.[0-9]+)?)(?:\s)", sp)[0])
    sp = converter.vests_to_sp(sp)

    sum_steem += steem
    sum_sbd += sbd
    sum_sp += sp

print('%s가 이웃들에게 받은 과자 값!' % username)
print('스팀: %.3f STEEM / 스달: %.3f SBD / 스파: %.3f SP' %
      (sum_steem, sum_sbd, sum_sp))