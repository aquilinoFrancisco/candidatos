# coding: utf-8

'''
Crawler de tweets de los usuarios que se deseen obtener
'''

from tweepy.streaming import StreamListener
#from dotenv import load_dotenv, find_dotenv
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import sys
import os
import unicodedata

#load_dotenv(find_dotenv())

'''CANDIDATE_CONSUMER_KEY =  os.getenv('CANDIDATE_CONSUMER_KEY')
CANDIDATE_CONSUMER_SECRET = os.getenv('CANDIDATE_CONSUMER_SECRET')
CANDIDATE_ACCESS_TOKEN = os.getenv('CANDIDATE_ACCESS_TOKEN')
CANDIDATE_ACCESS_TOKEN_SECRET = os.getenv('CANDIDATE_ACCESS_TOKEN_SECRET')'''


CANDIDATE_CONSUMER_KEY = ''
CANDIDATE_CONSUMER_SECRET = ''
CANDIDATE_ACCESS_TOKEN = '-'
CANDIDATE_ACCESS_TOKEN_SECRET = ''


auth = tweepy.OAuthHandler(CANDIDATE_CONSUMER_KEY, CANDIDATE_CONSUMER_SECRET)
auth.set_access_token(CANDIDATE_ACCESS_TOKEN, CANDIDATE_ACCESS_TOKEN_SECRET )

#Obtenemos lo necesario de mongodb
from pymongo import MongoClient

MONGO_HOST= 'mongodb://localhost/elections'
client = MongoClient(MONGO_HOST)
db = client.elections

TOTAL_ERRORS = 100


class CustomStreamListener(StreamListener):

    def on_status(self, status):
        try:

            if (status.author.screen_name).encode('utf8') == 'RichardBotBot':
                ##db.canMeade.insert(status._json)
                print "%s\t%s\t%s\t%s" % (status.text,status.author.screen_name,status.created_at,status.source)



        except Exception, e:
            print >> sys.stderr, 'Exception: ', e
            pass


    #primero revisamos si hay error. Si lo hay, no se ejecuta on_data
    def on_error(self, status):
        if status == 400:
            print ('Error 400: Peticion invalida')
        if status == 401:
            print ('Error 401: Error en la autenticacion')
        if status == 404:
            print ('Error 404: Revisar a donde se hace la peticion')
        if status == 406:
            print ('Error 406: Error en el formato de las peticiones')
        if status == 420:
            print ('Error 420: Demasiadas peticiones!')
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream


streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener())

# Status of users
# AMLO, ANAYA, MEADE, BRONCO
# Tatiana, jorge, aurelio, BRONCO NO TIENE

# Todos por mexico
# PRI
# PV
# NA
# Por mexico al frente
# MC
# PAN
# PRD
# Juntos haremos historia
# PES
# MORENA
# PT


for i in range(TOTAL_ERRORS):
    try:
        streaming_api.filter(follow=['777518176489775106','82119937','777518176489775106','237372254','1342520820',
        '33937794','92399925','32226455',
        '292116167','109045622','109711056',
        '141260426','16808700','119545041',
        '2329473343','889466488117235712','806348526137393152'])
    except:
        print ('Error %d' % i)
        continue
