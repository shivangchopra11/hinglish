import numpy as np
import json
import tweepy
import pandas as pd
from tweepy import OAuthHandler
from pprint import pprint

with open('./tweet_data.json','r') as f:
    loaded_json = json.load(f)

access_token = "227333278-qRu2VFBTKktO1orp7kotaaSx1brdAhqAhWyx5e3j"
access_token_secret = "KToUaDqXNCCndtE14okptPeqdtlmIwzahjgrOHgJ2vm9t"
consumer_key = "UVMu9FNSWco0Uerxw7AP4fs77"
consumer_secret = "cPtrBRPFCIPLKryjzFWXjBZRqpFyWGcKZrygBykDBn7UH5B1k5"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

all_users = []
for tweet in loaded_json.values():
    all_users.append(tweet['user']['id'])
all_users = set(all_users)
print(len(all_users))


user_retweets = {}
for tweet_id in loaded_json:
    try:
        print(tweet_id)
        user_id = loaded_json[tweet_id]['user']['id']
        user_retweets[str(user_id)] = []
        retweet_ids = []
        res = api.retweets(id=tweet_id)
        for rt in res:
            rt = rt._json
            pprint(rt)
            rt_id = rt['user']['id']
            if rt_id in all_users:
                user_retweets[user_id].append(rt_id)
    except tweepy.TweepError:
        user_retweets[str(user_id)] = []
        print('Something went wrong')

with open('rt_data.json', 'w') as fp:
    json.dump(user_retweets, fp, indent=4)
