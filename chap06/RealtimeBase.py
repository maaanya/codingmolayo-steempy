from contextlib import suppress
from steem.blockchain import Blockchain
from steem.post import Post
from steembase.exceptions import PostDoesNotExist
from steembase.exceptions import RPCError
from datetime import timedelta

def gen(stream):
    while True:
        try:
            for post in stream:
                yield post
        except PostDoesNotExist as e:
            print('')
            print(e)
            print('')
            pass
        except RPCError as e:
            print('')
            print(e)
            print('')
            pass
        except StopIteration:
            raise
        except Exception as e:
            print('')
            print('그 외 오류 전부')
            print('')
            pass

b = Blockchain()
stream = map(Post, b.stream(filter_by=['comment']))

for post in gen(stream):
    post_tags = post.json_metadata.get('tags', [])
    if 'kr' in post_tags:
        print(post.get("last_update", "1970-01-01T00:00:00") + timedelta(hours=9))
        print(post["author"], ' : ', post["body"])