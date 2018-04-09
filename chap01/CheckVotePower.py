from steem import Steem
from dateutil.parser import parse
from datetime import datetime


def get_voting_power(account_data):
    last_vote_time = parse(account_data["last_vote_time"])
    diff_in_seconds = (datetime.utcnow() - last_vote_time).seconds
    regenerated_vp = diff_in_seconds * 10000 / 86400 / 5
    total_vp = (account_data["voting_power"] + regenerated_vp) / 100
    if total_vp > 100:
        return 100
    return "%.2f" % total_vp

s = Steem()
account = s.get_account('whoami') # 계정명 입력
print(get_voting_power(account))




