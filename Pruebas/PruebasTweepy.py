#.\TFGBots\Scripts\Activate.ps1
import tweepy
import csv
import pandas as pd

f = open("./TFG-Bots-OSN/account.txt", "r")

access_token = f.readline().rstrip('\n')
access_token_secret = f.readline().rstrip('\n')

consumer_key = f.readline().rstrip('\n')
consumer_secret = f.readline().rstrip('\n')
f.close()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# imrpimir timeline
def my_timeline():
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)

# Get followers and friendship
def user_followers(name):
    for f in api.friends(name):
        if api.lookup_friendships(name, f.screen_name):
            print(name + " and " + f.screen_name + " follows each other")
        else:
            print(name + " and " + f.screen_name + " doesn't follows each other")

def hashtags_tweets(hashtag):
    trends = api.trends_place(1)
    tweets_list = []
    search_hashtag = tweepy.Cursor(api.search, q = hashtag, tweet_mode = "extended").items(5000)

    for tweet in search_hashtag:
            if 'retweeted_status' in tweet._json: 
                full_text = tweet._json['retweeted_status']['full_text']
            else:
                full_text = tweet.full_text
                        
            tweets_list.append([tweet.user.screen_name,
                                tweet.id,
                                tweet.retweet_count, # What you are interested of
                                tweet.favorite_count, # Maybe it is helpfull too
                                full_text,
                                tweet.created_at,
                                tweet.entities
                               ])
    tweets_df = pd.DataFrame(tweets_list, columns = ["screen_name", "tweet_id",
                                                      "n rt", 
                                                      "n replies",
                                                      "text",
                                                      "created_at", 
                                                      "entities"])
    # In a data frame format you can sort the tweets by the n of rt and get the top one
    print(tweets_list)
    tweets_df.to_json()

user_followers("kra0s22")
#hashtags_tweets("Arrimadas")