from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.test import tag


from extractor_scripts.twitter_extractor import Scrapper

@tag("tweets")
class TweetsTest(APITestCase):

    def setUp(self):
        
        self.url = reverse('tweets:create')

        self.data = [
                {   
                    'username' : '@gasdigiu',
                    'text' : 'este es un test',
                    'fecha' : '2019-05-05T00:00:00Z',
                    'favs' : 0,
                    'rts' : 7,
                    'link' : 'https:',
                    'label' : '',
                },
                {   
                    'username' : '@lucaocchi',
                    'text' : 'este es un test',
                    'fecha' : '2019-05-12T00:00:00Z',
                    'favs' : 7,
                    'rts' : 8,
                    'link' : 'https:',
                    'label' : '',
                },
                {   
                    'username' : '@gasdigiu',
                    'text' : 'este es un test',
                    'fecha' : '2019-08-05T00:00:00Z',
                    'favs' : 1,
                    'rts' : 7,
                    'link' : 'https:',
                    'label' : 'asdasd',
                },
        ]

    
    def test_create(self):

        response = self.client.post(self.url, self.data, format('json'))
        # response ok?
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        #validar objeto
        self.assertEquals(response.json()[0]['username'], self.data[0]['username'])
        self.assertEquals(response.json()[0]['text'], self.data[0]['text'])
        self.assertEquals(response.json()[0]['fecha'], self.data[0]['fecha'])
        self.assertEquals(response.json()[0]['favs'], self.data[0]['favs'])
        self.assertEquals(response.json()[0]['rts'], self.data[0]['rts'])
        self.assertEquals(response.json()[0]['link'], self.data[0]['link'])
        self.assertEquals(response.json()[0]['label'], self.data[0]['label'])

    
    def test_post_busqueda(self):

        scraper = Scrapper()
        busqueda = {
                    'id_busqueda' : 1,
                    'user_id' : 1,                
                    'ands' : "",
                    'phrase' : "",
                    'ors' : "",
                    'nots' : "",
                    'tags' : "",
                    'respondiendo' : "",
                    'mencionando' : "",
                    'From' : "@gdigiu",
                    'fecha_hasta' : "2019-08-20",
                    'fecha_desde' : "2019-08-07",
                    'fecha_peticion' : "",
                    'fecha_finalizacion' : "",
                    'finalizado' : False
                    }
        
        tweets_json = scraper.selenium_get_tweets(**busqueda)
        
        # post tweets
        response = self.client.post(self.url, tweets_json, format('json'))
        # response ok?
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)