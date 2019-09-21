from twitterscraper import query_tweets
import datetime as dt
import sys
import requests
import re


def get_busqueda(id_busqueda):
    # get a la base de datos
    response = requests.get("http://127.0.0.1:8000/id_busqueda/" + str(id_busqueda))
    return response

def ands_ors(query, x, separador):
    """ para obtener ands y ors """

    # x = busqueda[clave]
    if len(x.split()) > 1:
        x = x.split()
        separator = separador
        x = separator.join(x)
    if x != "" :
        query = query + " " + x
    
    return query

def resto(query, x, separador, separador2):
    """
    Para obtener nots, tags, etc
    """
    if len(x.split()) > 0:
        x = [separador + word if word[0] != separador else word for word in x.split()]
        separator = separador2
        x = separator.join(x)
    if x != "":
        query = query + " " + x
    return query


def armar_query(busqueda):
    # arma la query de acuerdo con los campos que llegan de la busqueda

    if busqueda['es_cuenta']:
        # hay que buscar la cuenta
        if "@" == busqueda['ands'][0]:
            query = busqueda['ands']
        else:
            query = "@" + busqueda['ands']
        # cronear busqueda de followers

    else:
        # parseamos todos los campos
        query = ""
        # todas estas palabras
        ands = busqueda['ands']
        query = ands_ors(query, ands, " AND ")
        
        # algunas de estas palabras
        ors = busqueda['ors']
        separador = " OR "
        if query != "":
            query = query + separador
        query = ands_ors(query, ors, separador)

        # MENCIONANDO a
        mencionando = busqueda['mencionando']
        if mencionando != "":
            query = query + " OR" 
        query = resto(query, mencionando, "@", " OR ")
        
        # ninguna de estas palabras
        nots = busqueda['nots']
        query = resto(query, nots, "-", " ")
    
        # hashtags
        tags = busqueda['tags']
        query = resto(query, tags, "#", " OR ")
        
        # desde estas cuentas
        From = busqueda['From']
        if len(From.split()) > 0:
            froms = ["from:@" + word if word[0] != "@" else "from:" + word for word in From.split()]
            separator = " OR "
            From = separator.join(froms)
        if From != "":
            query = query + " " + From

        # respondiendo a
        respondiendo = busqueda['respondiendo']
        if len(respondiendo.split()) > 0:
            respond = ["to:@" + word if word[0] != "@" else "to:" + word for word in respondiendo.split()]
            separator = " OR "
            respondiendo = separator.join(respond)
        if respondiendo != "":
            query = query + " " + respondiendo 

        query = re.sub(' +', ' ', query).lstrip()
    
        fecha_desde = busqueda['fecha_desde']
        fecha_hasta = busqueda['fecha_hasta']

    return query, fecha_desde, fecha_hasta


def scrap_tweets(id_busqueda):
    # get todos los tweets con la busqueda

    # busqueda = get_busqueda()

    #query = armar_query(busqueda)
    query = "-chistosa -mental from:gdigiu"

    list_of_tweets = query_tweets(query, begindate=dt.date(2019, 9, 19), enddate=dt.date(2019, 9, 22), lang='es')
    #list_of_tweets = query_tweets(query, begindate=dt.date(2019, 9, 20), lang='es')

    tweets = []
    
    try:

        # armo el json de cada tweet
        for tweet in list_of_tweets:
            # parseo cada tweet object a un json
            tweet_json = {
                "id_busqueda" : id_busqueda,
                "texto" : tweet.text,
                "user" : tweet.username,
                "fecha":  tweet.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "replies": tweet.replies,
                "rts ": tweet.retweets,
                "likes ": tweet.likes,
                "url": "https://twitter.com"+tweet.tweet_url,
            }
            tweets.append(tweet_json)
        
        return {
            "statusCode": 200,
            "body": tweets
        }
    except Error as e:
        return e

if __name__ == "__main__":
    """ if len(sys.argv) == 1:
        query = sys.argv
        print("longitud 1")
        print(query)
    else:
        print("longitud 2 o mas")
        print(sys.argv) """

    busqueda = {
          'id_busqueda' : 1,
          'user_id' : 1,                
          'ands' : "charfield testing",
          'phrase' : "charfield testing",
          'ors' : "esto aquello",
          'nots' : "sol playa",
          'tags' : "delpo",
          'respondiendo' : "gdigiu",
          'mencionando' : "mercadolibre mercadopago",
          'From' : "rogerfederer",
          'fecha_hasta' : "2019-03-25",
          'fecha_desde' : "2019-03-25",
          'fecha_peticion' : "2019-03-25",
          'fecha_finalizacion' : "2019-03-25",
          'finalizado' : False,
          'tiene_tweets' : False,
          'es_cuenta' : False
           }

    query, fecha_desde, fecha_hasta = armar_query(busqueda)
    print(query)

   # print(scrap_tweets(12))
    
