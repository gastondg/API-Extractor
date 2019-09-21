from twitterscraper import query_tweets
import datetime as dt
from pprint import pprint
import subprocess

def scrap_tweets(event, context):
    list_of_tweets = query_tweets("@gdigiu", begindate=dt.date(2019, 3, 8), enddate=dt.date(2019, 3, 11), lang='es')
    tweets = []
    id_busqueda = 1 # en realidad tendria que sacarla de event o context
    
    #if list_of_tweets not None and list_of_tweets distinta de vacio 
    # armo el json de cada tweet
    for tweet in list_of_tweets:
        # parseo cada tweet object a un json
        tweet_json = {
            "id_busqueda" : id_busqueda,
            "texto" : tweet.text,
            "user" : tweet.username,
            "fecha":  tweet.timestamp,
            "fecha2": tweet.timestamp_epochs,
            "replies": tweet.replies,
            "rts ": tweet.retweets,
            "likes ": tweet.likes,
            "url": "https://twitter.com"+tweet.tweet_url,
        }
        tweets.append(tweet_json)
    
    return tweets



if __name__ == '__main__':
    list_of_tweets = query_tweets("@gdigiu", begindate=dt.date(2019, 3, 8), enddate=dt.date(2019, 3, 11), lang='es')
    tweets = []
    if list_of_tweets == []:
        # no hay tweets
        pass
        # return list_of_tweets
    else:
        #print the retrieved tweets to the screen:
        for tweet in list_of_tweets:
            # parseo cada tweet object a un json
            tweet_json = {
                "texto" : tweet.text,
                "user" : tweet.username,
                "fecha":  tweet.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "replies": tweet.replies,
                "rts ": tweet.retweets,
                "likes ": tweet.likes,
                "url": "https://twitter.com"+tweet.tweet_url,
            }
            tweets.append(tweet_json)

    pprint(tweets)
    print(len(tweets))