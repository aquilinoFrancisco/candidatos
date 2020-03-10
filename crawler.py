# coding: utf-8

'''
Crawler de tweets que obtiene solo los realizados en Mexico
'''

#from dotenv import load_dotenv, find_dotenv
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient

import os
import tweepy

'''load_dotenv(find_dotenv())

MEXICO_CONSUMER_KEY =  os.getenv('MEXICO_CONSUMER_KEY')
MEXICO_CONSUMER_SECRET = os.getenv('MEXICO_CONSUMER_SECRET')
MEXICO_ACCESS_TOKEN = os.getenv('MEXICO_ACCESS_TOKEN')
MEXICO_ACCESS_TOKEN_SECRET = os.getenv('MEXICO_ACCESS_TOKEN_SECRET')
'''

MEXICO_CONSUMER_KEY = 'jg'
MEXICO_CONSUMER_SECRET = 
MEXICO_ACCESS_TOKEN = 'jj-g'
MEXICO_ACCESS_TOKEN_SECRET = 'algo'


N = 100

MONGO_HOST= 'mongodb://localhost/twitterdb'
client = MongoClient(MONGO_HOST)
db = client.twitterdb


auth = OAuthHandler(MEXICO_CONSUMER_KEY,MEXICO_CONSUMER_SECRET)
auth.set_access_token(MEXICO_ACCESS_TOKEN, MEXICO_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

class TwitterListener(StreamListener):

	# Funcion que procesa data y verifica si el tweet es de Mexico
	def on_status(self, data):
		tweet = self.process_tweet(data)
		if tweet['tweet']:
			if tweet['lugar'] == 'MX':
				db.tweets_All_Mexico.insert(tweet['tweet']._json)
				print(tweet['tweet']._json)
		return True

	# Funcion que maneja los codigos de error
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
		return False # kill the stream

	# Funcion que procesa data para verificar de que pais es
	def process_tweet(self, tweet):
		if tweet.id:
			identificador = tweet.id
			print identificador
		else:
			identificador = ""
		if tweet.place.country_code:
			lugar = tweet.place.country_code
		else:
			lugar = ""
		return {'tweet': tweet, 'identificador': identificador, 'lugar': lugar}


listener = TwitterListener()
stream = Stream(auth, listener)

# Mexico: -117.61,14.34,-86.38,32.67

for i in range(N):
    try:
		stream.filter(locations=[-117.61,14.34,-86.38,32.67])
    except:
        continue
