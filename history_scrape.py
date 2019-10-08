import numpy as np
import json
import tweepy
import pandas as pd
from tweepy import OAuthHandler
from pprint import pprint

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status


if __name__ == '__main__':
    with open('./tweet_data.json','r') as f:
        loaded_json = json.load(f)

    access_token = "227333278-qRu2VFBTKktO1orp7kotaaSx1brdAhqAhWyx5e3j"
    access_token_secret = "KToUaDqXNCCndtE14okptPeqdtlmIwzahjgrOHgJ2vm9t"
    consumer_key = "UVMu9FNSWco0Uerxw7AP4fs77"
    consumer_secret = "cPtrBRPFCIPLKryjzFWXjBZRqpFyWGcKZrygBykDBn7UH5B1k5"

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, parser=tweepy.parsers.JSONParser())


    all_users = []
    user_ids = []
    for tweet in loaded_json.values():
        all_users.append(tweet['user']['screen_name'])
        user_ids.append(tweet['user']['id'])
    # all_users = set(all_users)
    print(len(all_users))



    tweepy.models.Status.first_parse = tweepy.models.Status.parse
    tweepy.models.Status.parse = parse


    tweepy.models.User.first_parse = tweepy.models.User.parse
    tweepy.models.User.parse = parse


    history = {}
    ctr = 0
    for user, id in zip(all_users, user_ids):
        ctr += 1
        print(ctr)
        try:
            tweets = api.user_timeline(screen_name=user,
                                        page=1,
                                        count=20,
                                        tweet_mode='extended',
                                        full_text=True)
        except:
            pass
        page=2

        while (True):
            try:
                more_tweets = api.user_timeline(screen_name=user,
                                            page=page,
                                            count=20,
                                            tweet_mode='extended',
                                            full_text=True)
                # There are no more tweets
                if (len(more_tweets) == 0):
                    break
                else:
                    page = page + 1
                    tweets = tweets + more_tweets
            except:
                pass

        history[id] = tweets

    with open('history.json', 'w') as outfile:
        json.dump(history, outfile, indent=4)
