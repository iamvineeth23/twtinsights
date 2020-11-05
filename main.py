#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 18:25:21 2020

@author: vinnie
"""

import tweepy
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pickle

from keys import (
    api_key,
    api_secret_key,
    access_token,
    access_token_secret
)



def check_if_retweet(obj):
    
    if hasattr(obj, 'retweeted_status'):
        return True
    
    return False

%matplotlib qt
def plot_stats(tweets_dict):
    
    fig, ax = plt.subplots(1)
    fig.autofmt_xdate()
    
    plt.plot(tweets_dict['created_at'], tweets_dict['favourite_count'], 'ko', tweets_dict['created_at'], tweets_dict['favourite_count'])
    y_mean = [np.mean(tweets_dict['favourite_count'])]*len(tweets_dict['created_at'])
    plt.plot(tweets_dict['created_at'], y_mean, 'b--')
    xfmt = mdates.DateFormatter('%d-%m-%y')
    
    ax.xaxis.set_major_formatter(xfmt)

    plt.show()


def save_obj(obj, name ):
    with open('data/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
        
        
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print (tweet.text)
    
    
tweets = api.user_timeline(screen_name = USERID, count = 200, include_rts = False, tweet_mode = 'extended')

tweets_dict = defaultdict(list)

for status in tweets:

    tweets_dict['id'].append(status.id_str)
    tweets_dict['favourite_count'].append(status.favorite_count)
    tweets_dict['created_at'].append(status.created_at)
    tweets_dict['retweeted'].append(status.retweeted)
    tweets_dict['retweet_count'].append(status.retweet_count)
    tweets_dict['is_retweet'].append(check_if_retweet(status))
    tweets_dict['text'].append(status.full_text)
    
    tweet_url = 'https://twitter.com/twitter/status/' + status.id_str
    tweets_dict['tweet_url'].append(tweet_url)
    

save_obj(tweets_dict, 'donald_20201103' )

for pages in tweepy.Cursor(api.user_timeline, id='id', count=200).pages():        
   print(pages)

plot_stats(tweets_dict)



class GetTweets:
    
    def __init__(self, api, userid):
        self.userid = userid
        self.tweets = api.user_timeline(screen_name = self.userid, count = 200, include_rts = False, tweet_mode = 'extended')
        self.tweets_dict = defaultdict(list)

            
            
    def check_if_retweet(self, obj):
    
        if hasattr(obj, 'retweeted_status'):
            return True
        
        return False


    def build_dictionary(self):
        
        for status in self.tweets:

            self.tweets_dict['id'].append(status.id_str)
            self.tweets_dict['favourite_count'].append(status.favorite_count)
            self.tweets_dict['created_at'].append(status.created_at)
            self.tweets_dict['retweeted'].append(status.retweeted)
            self.tweets_dict['retweet_count'].append(status.retweet_count)
            #self.tweets_dict['is_retweet'].append(self.check_if_retweet(status))
            self.tweets_dict['text'].append(status.full_text)
            
            tweet_url = 'https://twitter.com/twitter/status/' + status.id_str
            self.tweets_dict['tweet_url'].append(tweet_url)


    def fetch_tweets(self):

        oldest_id = self.tweets[-1].id

        self.build_dictionary()
        print('Fetching tweets of: ', self.userid)
        while True:
            print('Tweets fetched till now {}'.format(len(self.tweets)))
            
            self.tweets = api.user_timeline(screen_name = self.userid,
                                            count = 200, include_rts = False,
                                            max_id = oldest_id - 1,
                                            tweet_mode = 'extended')
            
            if len(self.tweets)  == 0:
                break
            
            oldest_id = self.tweets[-1].id
            self.build_dictionary()
        
        return self.tweets_dict


    def save_obj(self, obj, name ):
        
    with open('data/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
        
        

USERID = 'realDonaldTrump'

t1 = GetTweets(api, USERID)
tweets_dict = t1.fetch_tweets()

test_id = 'JoeBiden'

t1 = GetTweets(api, test_id)
test_tweets_dict = t1.fetch_tweets()


save_obj(test_tweets_dict, 'biden_20201105' )

test_id = '@3XS0'
tweets = api.user_timeline(screen_name = test_id, count = 20, include_rts = False, tweet_mode = 'extended')

for status in tweets:
    
    print(status.entities['hashtags'][0]['text'])