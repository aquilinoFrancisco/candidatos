# -*- coding:utf8 -*-

'''
Programa que obtiene el corpus del contexto politico por medio de expresiones regulares
'''
# http://www.elfinanciero.com.mx/elecciones-2018/estos-son-los-hashtags-mas-usados-para-hablar-de-los-candidatos-esta-semana

from pymongo import MongoClient
import re
from time import clock

def tweetText(tweet):
    return tweet['text'] if not tweet['truncated'] else tweet['extended_tweet']['full_text']

toc = clock()

HOST = "mongodb://localhost/repo"
client = MongoClient(HOST)
db = client.repo


# Acapulco
regex_name_amlo = re.compile(r'(andr[eé][sz][\s]{1,2}manuel)|(l[oó]pe[sz][\s]{1,2}obrador)',re.I)
#regex_name_amlo = re.compile(r'(?:|\W)(L(o|ó)pe(z|s) ?Obrador)|(A(n|m)dr(e|é)(s|z) ?Manuel)|(((A(n|m)dr(e|é)(s|z))|(Manuel)) ?Obrador)(?:$|\W)', re.IGNORECASE)
regex_hashtags_amlo = re.compile(r'(\w*amlo\w*)|(andresmanuelovich|yasabesquien|as[ií]noandres|peje|juntosharemoshistoria)',re.I)
#regex_hashtags_amlo = re.compile(r'(?:|\W)(AMLO*(|v|dipino|2017|2018|EsUnPeligroParaMexico|ver?)|Manuelovsky|MiVotoParaAMLO|Andresmanuelovich|YaSabesQuien|LopezObrador|elpeje|JuntosHaremosHistoria)(?:$|\W)',re.IGNORECASE)
regex_mention_amlo = re.compile(r'(lopezobrador_)',re.I)

# Ciudad Juarez
#regex_name_anaya = re.compile(r'(?:|\W)Ricardo ?Anaya(?:$|\W)',re.IGNORECASE)
regex_name_anaya = re.compile(r'(ricardo\s{1,2}c?anaya\s{1,2}cort[eé]s)',re.I)
#regex_hashtags_anaya = re.compile(r'(?:|\W)(YoConAnaya|AnayaPresidente|RicardoAnaya|PorMéxicoAlFrente|CalvoAnaya)(?:$|\W)',re.I)
regex_hashtags_anaya = re.compile(r'(yoconanaya|anayapresidente|ricardoanaya|porm[eé]xicoalfrente|canaya|calvoanaya)',re.I)
regex_mention_anaya = re.compile(r'(RicardoAnayaC)',re.IGNORECASE)

# Tijuana
#regex_name_meade = re.compile(r'(?:|\W)(((meade)|(jos(e|é))|(antonio))? ?(k|c)uribre(n|ñ)a)|(((antonio)|(jos(e|é))|(Jos(e|é)) ?(Antonio))? ?Meade| (pepe(| )Meade))(?:$|\W)', re.IGNORECASE)
regex_name_meade = re.compile(r'(((jos[ée]|pepe|pepito)\s{1,2}(antonio\s{1,2})*)*meade\s{1,2}(kuribreña)*)',re.I)
#regex_hashtags_meade = re.compile(r'(?:|\W)(J(o|ó)venes(por|con)Meade|Meade|YoMero|YoConMeade|VotoMEADE|MovimientoMEADE|Avanzar ?Contigo)(?:$|\W)',re.IGNORECASE)
regex_hashtags_meade = re.compile(r'(\w*meade\w*)|(yomero|avanzarcontigo)',re.I)
regex_mention_meade = re.compile(r'(JoseAMeadeK)',re.I)


#regex_name_bronco = re.compile(r'(?:|\W)(Jaime ?Rodr(i|í)gue(z|s) ?Calder(o|ó)n)(?:$|\W)',re.IGNORECASE)
regex_name_bronco = re.compile(r'(jaime\s{1,2}rodr[ií]gue[sz](\s{1,2}calder[oó]n)*)',re.I)
#regex_hashtags_bronco = re.compile(r'(?:|\W)((al|el) ?bronco|BroncoConFE|NlEsBronco|bronconocumple|noquemuybronco|yosoybronco|preguntalealbronco)(?:$|\W)',re.IGNORECASE)
regex_hashtags_bronco = re.compile(r'(\w*bronco\w*)',re.I)
regex_mention_bronco = re.compile(r'(JaimeRdzNL)',re.I)

regex_political = re.compile(r'\b(PAN|PRD|PRI|MORENA|Partido\sVerde|Movimiento\snaranja|Movimiento\sciudadano|PRIAN|PRIMOR|EPN|PT|PANAL|Nueva\sAlianza|Partido\sEncuentro\sSocial|PES|elecciones2018|debateine|inem[eé]xico)\b',re.I)

regex_exception = re.compile(r'')

regex_list = [regex_name_amlo,regex_hashtags_amlo,regex_mention_amlo,regex_name_anaya,regex_hashtags_anaya,regex_mention_anaya,
                regex_name_meade,regex_hashtags_meade,regex_mention_meade,regex_name_bronco,regex_hashtags_bronco,regex_mention_bronco,regex_political]

i = 0
total = db.ciudades.count()
for tweet in db.ciudades.find({},no_cursor_timeout=True).batch_size(5):
    text = tweetText(tweet)
    i += 1
    for regex in regex_list:
        if regex.search(text):
            db.contextociudadesnuevo.insert(tweet)
            break
    print '%d tweets procesados de %d' % (i,total)

toc = clock()
#print('Timing: ' + str(toc-tic))
