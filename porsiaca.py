#####Uso de Hashtag
f =  open("./hashtags.txt", "r")
hashtagsList = []
hashtag = None
while True:
    # read line
    hashtag = f.readline()
    if (hashtag == "") :
        break
    hashtag = hashtag.rstrip('\n')
    hashtag = hashtag.replace('#', '')
    initDate = f.readline().rstrip('\n')
    lastDate = f.readline().rstrip('\n')
    hashtag = (hashtag, initDate, lastDate)
    hashtagsList.append(hashtag)
    # check if line is not empty
    
f.close()
for h in hashtagsList:
    print(h)

#Versión para tweepy V2

#agregar que tipo de tweet es y a quien responden si es necesario
import tweepy
import csv
import pandas as pd
import json
from subprocess import check_output

entrada = ""
next_token = None
entradaizq = '' 
entradader = ''
hashtags = ''
total = 0
url = 'curl "https://api.twitter.com/2/tweets/search/all?'

f = open("./accountV2.txt", "r")
Bearer = f.readline().rstrip('\n')
f.close()




for l in hashtagsList:
    total = 0
    entradaizq = url + "query=%23" + str(l[0]) + "&start_time=" +  str(l[1]) + "T00%3A00%3A00Z" + "&end_time=" + str(l[2]) + 'T11%3A59%3A59Z&max_results=100&expansions=author_id&tweet.fields=created_at,lang,conversation_id&user.fields=created_at,entities'
    entradader = '"' + ' -H "Authorization: Bearer '+ str(Bearer) + '"'

    print("Inicio Hashtag: " + str(l[0]) + "\\\\\\\\\\\\ \n") 
    entrada = entradaizq + entradader

    json_obj = json.loads(check_output(entrada, shell=True).decode())
    # Caso en el que hay que esperar para volver a hacer petición
    while ('data' not in json_obj):
        json_obj = json.loads(check_output(entrada, shell=True).decode())

    if ('next_token' in json_obj['meta']):
        next_token = json_obj['meta']['next_token']
    else:
        next_token = None

    #Manejamos la primera respuesta con el next_t
    while next_token is not None:
        total += int(json_obj['meta']['result_count'])
        for tweet in json_obj['includes']['users']:
            if ('entities' in tweet) and ('description' in tweet['entities']) and ('hashtags' in tweet['entities']['description']):
                for h in tweet['entities']['description']['hashtags']:
                    if hashtags == '':
                        hashtags = h['tag']
                    else:
                        hashtags = hashtags + ', ' + h['tag']  

            #imprimir id de usuario
            print("     id: " + tweet['id'])
            #imprimir hashtags
            print("     hashtags: " + hashtags)
            #imprimir fecha de creción
            print("         created_at: " + tweet['created_at'] + "\n")

        entrada = entradaizq + '&next_token=' + next_token + entradader
        json_obj = json.loads(check_output(entrada, shell=True).decode())

        # Caso en el que hay que esperar para volver a hacer petición
        while ('data' not in json_obj):
            json_obj = json.loads(check_output(entrada, shell=True).decode())

        if ('meta' in json_obj) and ('next_token' in json_obj['meta']):
            next_token = json_obj['meta']['next_token']
        else:
            next_token = None
        #reiniciar variables de bucle
        hashtags = ''

    # Manejo de ultima respuesta
    if (next_token is None) and ('meta' in json_obj) and (int(json_obj['meta']['result_count']) > 0):
        for tweet in json_obj['includes']['users']:
            if ('entities' in tweet) and ('description' in tweet['entities']) and ('hashtags' in tweet['entities']['description']):
                for h in tweet['entities']['description']['hashtags']:
                    if hashtags == '':
                        hashtags = h['tag']
                    else:
                        hashtags = hashtags + ', ' + h['tag'] 

            #imprimir id de usuario
            print("     User id: " + tweet['id'])
            #imprimir fecha de creción
            print("         created_at: " + tweet['created_at'] + "\n")

        total += int(json_obj['meta']['result_count'])
    print("Fin Hashtag: " + str(l[0]) + "\\\\\\\\\\\\ \n\n") 
    print ("total final " + str(total))
#df = pd.DataFrame(msgs)