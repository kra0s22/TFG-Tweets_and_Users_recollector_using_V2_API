#Versión para tweepy V2

#agregar que tipo de tweet es y a quien responden si es necesario
import datetime
from datetime import date
import tweepy
import csv
import pandas as pd
import json
from subprocess import check_output
import time
import math

# CONSTANTES
PETITIONS_PER_TIME_LAPSE = 300
TIME_LAPSE = 15*60
TIMER = TIME_LAPSE/PETITIONS_PER_TIME_LAPSE
TIMER_LOG = 20*60
listaResultados = []
TIEMPO = TIMER_LOG

#variables
entrada = ""
next_token = None
entradaizq = '' 
entradader = ''
hashtags = ''
total = 0
startDate = ''
endDate = ''
inicio = 0
fin = 0
resultado = ''
url = 'curl "https://api.twitter.com/2/tweets/search/all?'
iniTimerLog = 0
finTimerLog = 0

today = datetime.date.today()
# dd/mm/YY
d1 = today.strftime("%d-%m-%Y")
#Crear ficheros de log
log = open("./log" + d1 + ".txt", "a")
log.write("Primer log\n")
#Crear ficheros de log
errorlog = open("./errorlog" + d1 + ".txt", "a")



#####Uso de Hashtag
f =  open("./hashtags.txt", "r")
hashtagsList = []
hashtag = None
while True:
    # read line
    try:
        hashtag = f.readline()
        if (hashtag == "") :
            break
    except:
        # datetime object containing current date and time
        now = datetime.datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        errorlog.write("Fallo al leer el fichero hashtags.txt " + dt_string + "\n")

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


def DayMonthYearToPetition(date):
    splited = ''
    if ('/' in date):
        splited = date.split('/')
    elif ('-' in date):
        splited = date.split('-')

    return (splited[2] + '-' + splited[1] + '-' + splited[0])

def PetitionToDayMonthYear(petition):
    splited = ''
    time = ''
    splited = petition.split('T')
    time = splited[1]
    splited = splited[0].split('-')
    return (splited[2] + '-' + splited[1] + '-' + splited[0] + 'T' + time)


# Problemas a resolver: 
# - Hay que resolver el problema de la situaci'on geogr'afica y el uso de entities 
# - Hacer el Log y ejecutar durante horas para que muestre dicho Log

# Hashtag: nombre del hashtag que se va a buscar
# start: fecha de inicio
# end: fecha de respuesta
# number: n'umero de tweets que queremos obtener
# bearer: bearer id
# next_token: token de la page (inicialmente string vac'ia) que quieres buscar
# return tupla de n'umero de respuestas y next_token
def PetitionsLessEqual100(hashtag, start, end, number, bearer, next_token):

    startDate = DayMonthYearToPetition(start)
    endDate = DayMonthYearToPetition(end)
    total = (0, '')
    entradaizq = url + "query=%23" + hashtag + "&start_time=" +  startDate + "T00%3A00%3A00Z" + "&end_time=" + endDate + 'T11%3A59%3A59Z&max_results=' + str(number) + '&tweet.fields=author_id,referenced_tweets,created_at,context_annotations,lang,entities&expansions=geo.place_id&place.fields=country'
    entradader = '"' + ' -H "Authorization: Bearer '+ bearer + '"'

    if (next_token != ''):
        entrada = entradaizq + '&next_token=' + next_token + entradader
    else:
        entrada = entradaizq + entradader

    #primera petici'on del hashtag
    json_obj = json.loads(check_output(entrada, shell=True).decode())

    #inicio de timer
    #timerasofa
    # Comprobar que hay respuestas para dicho hashtag
    if ('meta' in json_obj) and (int(json_obj['meta']['result_count']) > 0):

        for tweet in json_obj['data']: 
            #imprimir id de usuario
            print("     author_id: " + tweet['author_id'])
            #imprimir id de tweet
            print("     id: " + tweet['id'])
            #imprimir fecha de creción
            print("       created_at: " + PetitionToDayMonthYear(tweet['created_at']))
            
            if ('referenced_tweets' in tweet):
                #imprimir tweets referidos
                print("       referenced_tweets: " + str(tweet['referenced_tweets']))
            if ('context_annotation' in tweet):
                #imprimir context_annotation
                print("       context_annotation: " + str(tweet['context_annotations']))
            if ('geo' in tweet) and (('includes' in json_obj) and ('places' in json_obj['includes'])):
                place_id = tweet['geo']['place_id']
                for place in json_obj['includes']['places']:
                    if (place_id == place['id']):
                        #imprimir context_annotation
                        print("       Country: " + str(place['country']))
            print("       lang: " + str(tweet['lang']) + '\n')
            print("       entities: " + str(tweet['entities']) + '\n')




        if ('next_token' in json_obj['meta']):
            total = (int(json_obj['meta']['result_count']), json_obj['meta']['next_token'])
        else:
            total = (int(json_obj['meta']['result_count']), '')
        print("N'umero de peticiones enviadas: " + str(number))
        print("N'umero de peticiones recibidas: " + str(json_obj['meta']['result_count']))
        #df = pd.DataFrame(msgs)
        return total

    #si no tiene meta entonces es un error y hay que manejarlo
    elif ('meta' in  json_obj) and (int(json_obj['meta']['result_count']) == 0):
        # datetime object containing current date and time
        now = datetime.datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        errorlog.write("Error, no hay tweets para el Hashtag: " + str(hashtag) + " " + dt_string + '\n')
        print("No hay tweets para el Hashtag: " + str(hashtag))
    else:
        strerror = ''
        print("Error en la petición: ")
        strerror = strerror + "Error en la petición: "
        # si el error es por cuestión de peticiones esperar para hacer la siguiente peticion
        if ('title' in json_obj):
            print("  Título del error: " + json_obj['title'])
            strerror = strerror + "  Título del error: " + str(json_obj['title'])
            if ('status' in json_obj):
                strerror = strerror + " Código de error: " + str(json_obj['status'])
                print("  Código de error: " + json_obj['status'])
            if ('detail' in json_obj):
                strerror = strerror + "  Descripción del error: " + str(json_obj['detail'])
                print("  Descripción del error: " + json_obj['detail'])

            if ('Invalid Request' == json_obj['title']):
                strerror = strerror + " Error: " + str(entrada.split(' -H')[0])
                print(entrada.split(' -H')[0])
        errorlog.write(strerror + " " + dt_string + '\n')
    return total


# Hashtag: nombre del hashtag que se va a buscar
# start: fecha de inicio
# end: fecha de respuesta
# number: n'umero de tweets que queremos obtener
# bearer: bearer id
# return devuelve el totl de tweets que se han obtenido
def TweetList(hashtag, start, end, number, bearer):
    global TIEMPO
    global listaResultados
    total = 0
    aux = 0
    resultado = (0, '')
    startTime = 0
    endTime = 0

    print("Inicio Hashtag: " + hashtag + "\\\\\\\\\\\\ \n")
    if (number < 100):
        startTime = time.time()
        total =  PetitionsLessEqual100(hashtag, start, end, number, bearer, None)[0]
        listaResultados.append((hashtag, total))
        endTime = time.time()

        aux = endTime - starTime
        

        if (aux < TIMER):
            time.sleep(math.ceil(TIMER - aux))
            TIEMPO -= (TIMER - aux)

        if (TIEMPO <= 0):
            #aqui se imprime en el log los hashtags que se han escrito y c'uantos valores se han obtenido de estos
            TIEMPO = TIMER_LOG
            # datetime object containing current date and time
            now = datetime.datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            log.write(str(listaResultados) + dt_string + '\n')
            listaResultados = []
    else:
        startTime = 0
        endTime = 0
        while ((number - total) > 0):
            #Caso base
            if ((number - total) >= 100):
                startTime = time.time()
                resultado = PetitionsLessEqual100(hashtag, start, end, 100, bearer, resultado[1])
                endTime = time.time()
            #Fin de caso
            elif ((number - total) > 0) and ((number - total) < 100):
                startTime = time.time()
                resultado = PetitionsLessEqual100(hashtag, start, end, (number - total), bearer, resultado[1])
                endTime = time.time()

            aux = endTime - startTime
            if (aux < TIMER):
                TIEMPO -= (TIMER - aux)
                time.sleep(math.ceil(TIMER - aux))
                time.sleep(TIMER)

            total += resultado[0]
            listaResultados.append((hashtag, total))
            if (TIEMPO <= 0):
                #aqui se imprime en el log los hashtags que se han escrito y c'uantos valores se han obtenido de estos
                TIEMPO = TIMER_LOG
                # datetime object containing current date and time
                now = datetime.now()
                # dd/mm/YY H:M:S
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                log.write(str(listaResultados) + dt_string + '\n')
                listaResultados = []
            
            # caso en el que la respuesta no encuentra tweets o no hay mas tweets
            if (resultado[0] == 0) or ((resultado[0] > 0) and resultado[1] == ''):
                break
    
    print ("Tweets totales: " + str(total))
    print("Fin Hashtag: " + str(hashtag) + "\\\\\\\\\\\\ \n\n")

    return (total, hashtag)




f = open("./accountV2.txt", "r")
Bearer = f.readline().rstrip('\n')
f.close()


for l in hashtagsList:
    resultado = TweetList(l[0], l[1], l[2], 121, Bearer)

log.close()
errorlog.close()

    
 

