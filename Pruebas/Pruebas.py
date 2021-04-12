#Versión para tweepy V2
import tweepy
import csv
import pandas as pd
consumer_key = ''  # Add your API key here
consumer_secret = ''  # Add your API secret key here
access_token = ''  # Add your access key here
access_token_secret = ''  # Add your access secret key here

####input your credentials here
f = open("./accountV2.txt", "r")

consumer_key = f.readline().rstrip('\n')
consumer_secret = f.readline().rstrip('\n')
access_token = f.readline().rstrip('\n')
access_token_secret = f.readline().rstrip('\n')

f.close()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Espera a que Twitter me deje acceder  
api = tweepy.API(auth, wait_on_rate_limit=True)

#####Uso de Hashtag
f =  open("./hashtags.txt", "r")
hashtagsList = []
while True:
    print("Bucle")
    # read line
    hashtag = f.readline()
    if (hashtag == "") :
        break
    hashtag = hashtag.rstrip('\n')
    initDate = f.readline().rstrip('\n')
    lastDate = f.readline().rstrip('\n')
    hashtag = (hashtag, initDate, lastDate)
    hashtagsList.append(hashtag)
    # check if line is not empty
    
f.close()
for h in hashtagsList:
    print(h)

df = pd.DataFrame(columns=['Hashtag', 'User', 'Relationship', 'Created at (A/'])
msgs = []
msg =[] 
user = []
for l in hashtagsList:
    query = l[0] + " since:" +  l[1] + " until:" +  l[2]
    for tweet in tweepy.Cursor(api.search_full_archive, enviroment_name ='development', query = l[0], fromDate = l[1], toDate = l[2]).items():
        user = [tweet.user.screen_name, tweet.user.id_str]
        reply = None
        # caso en el que haces reply, quote y retweet
        if tweet.in_reply_to_status_id_str != None:
            reply = (tweet.in_reply_to_screen_name, tweet.in_reply_to_status_id_str)
        msg = (l[0], user, reply, str(tweet.created_at))
        print (msg)
        msgs.append(msg)

df = pd.DataFrame(msgs)