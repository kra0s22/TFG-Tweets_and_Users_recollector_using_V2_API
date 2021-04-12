from twitter_ads.client import Client
from twitter_ads.client import Client
from twitter_ads.campaign import Campaign
from twitter_ads.enum import ENTITY_STATUS

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

f = open("./accountV2.txt", "r")

CONSUMER_KEY = f.readline().rstrip('\n')
CONSUMER_SECRET = f.readline().rstrip('\n')
ACCESS_TOKEN = f.readline().rstrip('\n')
ACCESS_TOKEN_SECRET = f.readline().rstrip('\n')

f.close()

