# coding: utf-8

'''
 Programa que obtiene el timeline de un usuario de Twitter
 Se debe proporcionar el numero de dias hacia atras
'''

#from dotenv import , find_dotenv
from pymongo import MongoClient
from datetime import datetime
from time import mktime,strftime,strptime
import tweepy
import os

#load_dotenv(find_dotenv())

'''CANDIDATE_CONSUMER_KEY = os.getenv('CANDIDATE_CONSUMER_KEY')
CANDIDATE_CONSUMER_SECRET = os.getenv('CANDIDATE_CONSUMER_SECRET')
CANDIDATE_ACCESS_TOKEN = os.getenv('CANDIDATE_ACCESS_TOKEN')
CANDIDATE_ACCESS_TOKEN_SECRET = os.getenv('CANDIDATE_ACCESS_TOKEN_SECRET')
'''

CANDIDATE_CONSUMER_KEY = ''
CANDIDATE_CONSUMER_SECRET = ''
CANDIDATE_ACCESS_TOKEN = '-'
CANDIDATE_ACCESS_TOKEN_SECRET = ''



MONGO_HOST = 'mongodb://localhost/elections'

client = MongoClient(MONGO_HOST)
db = client.elections

auth = tweepy.OAuthHandler(CANDIDATE_CONSUMER_KEY, CANDIDATE_CONSUMER_SECRET)
auth.set_access_token(CANDIDATE_ACCESS_TOKEN, CANDIDATE_ACCESS_TOKEN_SECRET )

api = tweepy.API(auth)
total = 0
DIAS = 170

for status in tweepy.Cursor(api.user_timeline, screen_name='@JoseAMeadeK',tweet_mode='extended').items():
    #print type(strftime('%Y-%m-%d %H:%M:%S', strptime(status._json['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))#
    total = total + 1

    d = datetime.fromtimestamp(mktime(strptime(status._json['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))

    if (datetime.now() - d).days < DIAS:
        print 'Fecha: %s Diferencia de días: %d' % (status.created_at,(datetime.now() - d).days)
        #print status.full_text
        db.canMeade.insert(status._json)
        print(status._json)
    else:
        print 'Ya pasaron %d dias' % DIAS
        break

print 'Total de Tweets: %d' % total
