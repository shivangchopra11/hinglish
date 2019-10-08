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

user_followers = {}
for tweet in loaded_json.values():
    try:
        user_id = tweet['user']['id']
        screen_name = tweet['user']['screen_name']
        user_followers[str(user_id)] = []
        print(user_id)
        follower_ids = []
        for page in tweepy.Cursor(api.followers_ids, screen_name=screen_name).pages():
            follower_ids.extend(page)
        print(follower_ids)
        for fol_id in follower_ids:
            if fol_id in all_users:
                user_followers[str(user_id)].append(fol_id)
    except tweepy.TweepError:
        # fill_tweets.append([])
        user_followers[str(user_id)] = []
        print('Something went wrong')

with open('user_data.json', 'w') as fp:
    json.dump(user_followers, fp, indent=4)
