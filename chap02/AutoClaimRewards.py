import re
from steem.steem import Steem

acc = 'whoami' # 계정명 입력
pkey = '5xxxxxx' # 포스팅키 입력

def claim_rewards():
    steem = Steem(keys = pkey)
    acc_info = steem.get_account(acc)

    rvb = acc_info['reward_vesting_balance']
    rvs = acc_info['reward_vesting_steem']
    rvd = acc_info['reward_sbd_balance']

    rvb = re.findall("([0-9]+(?:\.[0-9]+)?)(?:\s)", rvb)[0]
    rvs = re.findall("([0-9]+(?:\.[0-9]+)?)(?:\s)", rvs)[0]
    rvd = re.findall("([0-9]+(?:\.[0-9]+)?)(?:\s)", rvd)[0]

    if float(rvb) > 0:
        steem.claim_reward_balance(account = acc)
        print('와! %s의 SP와 %s의 SBD의 과자 값이 들어왔어요.' % (rvs, rvd))

claim_rewards()






