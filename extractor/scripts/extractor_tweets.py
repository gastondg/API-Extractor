from twitterscraper import query_tweets
import datetime as dt
import sys
import requests
import re
import pandas as pd
from pprint import pprint

def get_busqueda(id_busqueda):
    # get a la base de datos
    response = requests.get("http://127.0.0.1:8000/v1/api/busqueda/id_busqueda/" + str(id_busqueda))
    print("\nEsta es la respuesta del server de busqueda: ")
    pprint(response.json())
    return response.json()

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
        if ors != "":
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


#def scrap_tweets(id_busqueda):
def scrap_tweets(id_busqueda):
    """ 
    Obtiene la busqueda con el id_busqueda y la realiza
    """
    # get busqueda
    busqueda = get_busqueda(id_busqueda)
    
    # comprobar que la busqueda no sea vacia
    if not busqueda:
        # es decir, si busqueda es vacia
        print("Busqueda vacia")
    else:
        # generar query
        query, fecha_desde, fecha_hasta = armar_query(busqueda)
        print("\nQuery armada: ")
        pprint(query)
        
        # list_of_tweets = query_tweets(query, begindate=dt.date(2019, 9, 19), enddate=dt.date(2019, 9, 22), lang='es')
        aaaa, mm, dd = int(fecha_desde[:4]), int(fecha_desde[5:7]), int(fecha_desde[8:])
        AAAA, MM, DD = int(fecha_hasta[:4]), int(fecha_hasta[5:7]), int(fecha_hasta[8:])
        list_of_tweets = query_tweets(query, begindate=dt.date(aaaa, mm, dd), enddate=dt.date(AAAA, MM, DD), lang='es')
        
        tweets = []
        id_busqueda = 1
        try:

            # armo el json de cada tweet
            for tweet in list_of_tweets:
                # parseo cada tweet object a un json
                tweet_json = {
                    "id_busqueda" : id_busqueda,
                    "text" : tweet.text,
                    "username" : tweet.username,
                    "fecha":  tweet.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "replies": tweet.replies,
                    "rts ": tweet.retweets,
                    "likes ": tweet.likes,
                    "url": "https://twitter.com"+tweet.tweet_url,
                }
                tweets.append(tweet_json)

            # eliminar repetidos
            # convertir a dataframe
            df = pd.DataFrame(tweets)
            df = df.drop_duplicates(subset='url')
            tweets = df.to_dict(orient="records")

            print("\nSe encontraron estos tweets:")
            pprint(tweets)
            return tweets
            
        except Exception as e:
            return e

print("Nombre de main")
print(__name__)

if __name__ == "__main__":
    
    id_busqueda = str(sys.argv[1])
    print("Vamos a buscar la busqueda con id: " + str(id_busqueda))

    # tweets = scrap_tweets(id_busqueda)["body"] 
    tweets = scrap_tweets(id_busqueda)
    
    if tweets == []:
    
        url_busqueda_sin_tweets = "http://127.0.0.1:8000/v1/api/busqueda/id_busqueda/busqueda_vacia/" + str(id_busqueda)
        requests.post(url_busqueda_sin_tweets)
    
    else: # si trajo tweets

        # clasificar tweets
        # armar nube de palabras

        # POST a la BD 
        # Tweets obtenidos
        print("\nGuardando tweets obtenidos al http://127.0.0.1:8000/v1/api/tweets/")
        url_tweets = "http://127.0.0.1:8000/v1/api/tweets/"
        response1 = requests.post(url_tweets, data=tweets)
        print("\nRespuesta del POST a guardar tweets")
        pprint(response1.json())

        # Busqueda finalizada
        url_busqueda_finalizada = "http://127.0.0.1:8000/v1/api/busqueda/id_busqueda/busqueda_finalizada/" + str(id_busqueda)
        response2 = requests.post(url_busqueda_finalizada)
        print("\nRespuesta al POST a busqueda finalizada")
        pprint(response2.json())
        print("\nFin!")