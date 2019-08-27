from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from datetime import datetime, timedelta
from django.test import tag

from extractor_scripts.twitter_extractor import Scrapper

@tag("busq")
class BusquedaTest(APITestCase):

    def setUp(self):
        
        self.url = reverse('busqueda:create')
        
        self.fecha = datetime.utcnow() - timedelta(days=365)

        self.fecha2 = datetime.utcnow() - timedelta(days=300)

        self.data = {
          'id_busqueda' : 1,
          'user_id' : 1,                
          'ands' : "charfield testing",
          'phrase' : "charfield testing",
          'ors' : "charfield testing",
          'nots' : "charfield testing",
          'tags' : "charfield testing",
          'respondiendo' : "charfield testing",
          'mencionando' : "charfield testing",
          'From' : "charfield testing",
          'fecha_hasta' : "2019-03-25",
          'fecha_desde' : "2019-03-25",
          'fecha_peticion' : "2019-03-25",
          'fecha_finalizacion' : "2019-03-25",
          'finalizado' : False
           }

    
    def test_create(self):

        response = self.client.post(self.url, self.data, format('json'))
        # response ok?
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        #validar objeto
        self.assertEquals(response.json()['id_busqueda'], self.data['id_busqueda'])
        self.assertEquals(response.json()['user_id'], self.data['user_id'])
        self.assertEquals(response.json()['ands'], self.data['ands'])
        self.assertEquals(response.json()['phrase'], self.data['phrase'])
        self.assertEquals(response.json()['ors'], self.data['ors'])
        self.assertEquals(response.json()['nots'], self.data['nots'])
        self.assertEquals(response.json()['tags'], self.data['tags'])
        self.assertEquals(response.json()['respondiendo'], self.data['respondiendo'])
        self.assertEquals(response.json()['mencionando'], self.data['mencionando'])
        self.assertEquals(response.json()['From'], self.data['From'])
        self.assertEquals(response.json()['fecha_hasta'], self.data['fecha_hasta'])
        self.assertEquals(response.json()['fecha_desde'], self.data['fecha_desde'])
        self.assertEquals(response.json()['fecha_peticion'], self.data['fecha_peticion'])
        self.assertEquals(response.json()['fecha_finalizacion'], self.data['fecha_finalizacion'])
        self.assertEquals(response.json()['finalizado'], self.data['finalizado'])
        
        

    
    """ def test_get_avgprice(self):

        self.client.post(self.url, self.data, format('json'))
        response = self.client.get(self.url)
    
        # response ok?
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), len(self.data))

        fecha = str(datetime.utcnow().date())
        #validar primer objeto
        avg_price_json = response.json()[0]
        avg_price_data = self.data[0]
        self.assertEqual(avg_price_json['symbol'], avg_price_data['symbol'])
        self.assertEqual(avg_price_json['mins'], avg_price_data['mins'])
        self.assertEqual(avg_price_json['price'], avg_price_data['price'])
        fecha_0 = avg_price_json['timestamp'][:10] #datos obtenidos del get
        self.assertEquals(fecha_0, fecha)
        
        #validar segundo objeto
        avg_price_json = response.json()[1]
        avg_price_data = self.data[1]
        self.assertEqual(avg_price_json['symbol'], avg_price_data['symbol'])
        self.assertEqual(avg_price_json['mins'], avg_price_data['mins'])
        self.assertEqual(avg_price_json['price'], avg_price_data['price']) # datos obtenidos del get
        fecha_1 = avg_price_json['timestamp'][:10]
        self.assertEquals(fecha_1, fecha)

    
    def test_get_avgprice_by_symbol(self):

        r = self.client.post(self.url, self.data, format('json')) #deberia estar listo y sin errores
        fecha_de_creacion = r.json()[2]['timestamp'] 
        url = self.url + '?symbol=BTCUSDT'
        response = self.client.get(url)
        # response ok?
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 1)
        # validar el objeto obtenido
        self.assertEquals(response.json()[0]['symbol'], self.data[2]['symbol'])
        self.assertEquals(response.json()[0]['mins'], self.data[2]['mins'])
        self.assertEquals(response.json()[0]['price'], self.data[2]['price'])
        self.assertEquals(response.json()[0]['timestamp'][:10], fecha_de_creacion[:10]) """
    
    @tag("selenium")
    def test_open_selenium(self):
        print("intentando abrir selenium")
        scraper = Scrapper()
        scraper.test()
        self.assertEquals(200, status.HTTP_200_OK)