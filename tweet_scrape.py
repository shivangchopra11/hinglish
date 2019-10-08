import numpy as np
import json
import tweepy
import pandas as pd
from tweepy import OAuthHandler
from pprint import pprint

df = pd.read_csv('./id_annotated.tsv', sep='\t', header=None)
tweets = df[0]

tweets = tweets.values

access_token = "227333278-qRu2VFBTKktO1orp7kotaaSx1brdAhqAhWyx5e3j"
access_token_secret = "KToUaDqXNCCndtE14okptPeqdtlmIwzahjgrOHgJ2vm9t"
consumer_key = "UVMu9FNSWco0Uerxw7AP4fs77"
consumer_secret = "cPtrBRPFCIPLKryjzFWXjBZRqpFyWGcKZrygBykDBn7UH5B1k5"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


tweet_list = []
for ix in tweets:
    tweet_list.append(ix)


# full_tweets = []
final_dict = {}
tweet_count = len(tweets)
ctr = 0
try:
    for i in range(len(tweet_list)):
        ix = tweet_list[i]
        print(ctr)
        ctr += 1
        cur = api.statuses_lookup([ix], include_entities=True, tweet_mode='extended')

        if len(cur)>0:
            pprint(cur[0]._json)
            final_dict[str(ix)] = cur[0]._json
        # else:
            # final_dict[str(ix)] = {}
        # full_tweets.append(cur)
except tweepy.TweepError:
    # fill_tweets.append([])
    final_dict[str(ix)] = {}
    print('Something went wrong, quitting...')


# full_tweets = np.array(full_tweets)
# np.save('full_tweets.npy', full_tweets)

with open('tweet_data.json', 'w') as fp:
    json.dump(final_dict, fp, indent=4)
