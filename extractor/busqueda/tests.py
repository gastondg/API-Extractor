from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from datetime import datetime, timedelta
from django.test import tag
from pprint import pprint

""" 
ARREGLAR FECHA DE PETICION!!!
Hay que eliminar el assert equals
Tambien puede estar fallando el get por ID porque ya no devuelve una lista, devuelve un solo elemento
"""


@tag("busq")
class BusquedaTest(APITestCase):

    def setUp(self):
        
        self.url = reverse('busqueda:create')
        
        self.fecha = datetime.utcnow() - timedelta(days=365)

        self.fecha2 = datetime.utcnow() - timedelta(days=300)

        self.data = {
          'id_busqueda' : 1,
          'user' : 1,                
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
          #'fecha_peticion' : None,
          #'fecha_finalizacion' : None,
          'finalizado' : False,
          'tiene_tweets' : False,
          'es_cuenta' : False,
          'nombre' : "nombre1",
           }
        
        self.data2 = {
          'id_busqueda' : 2,
          'user' : 1,                
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
          #'fecha_peticion' : "2019-03-25",
          #'fecha_finalizacion' : "2019-03-25",
          'finalizado' : True,
          'tiene_tweets' : True,
          'nombre' : "nombre2",
          'es_cuenta' : False,
           }

    @tag("prueba_create")
    def test_create(self):

        response = self.client.post(self.url, self.data, format('json'))
        # response ok?
        pprint(response)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        #validar objeto
        self.assertEquals(response.json()['id_busqueda'], self.data['id_busqueda'])
        self.assertEquals(response.json()['user'], self.data['user'])
        self.assertEquals(response.json()['nombre'], self.data['nombre'])
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
        #self.assertEquals(response.json()['fecha_peticion'], self.data['fecha_peticion'])
        #self.assertEquals(response.json()['fecha_finalizacion'], self.data['fecha_finalizacion'])
        self.assertEquals(response.json()['finalizado'], self.data['finalizado'])
        self.assertEquals(response.json()['tiene_tweets'], self.data['tiene_tweets'])

    
    @tag("busqueda_fin")
    def test_busqueda_finalizada(self):
        
        response = self.client.post(self.url, self.data, format('json'))
        # response ok?
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        url = reverse('busqueda:busqueda_finalizada',args=str(self.data['id_busqueda']))
        response = self.client.put(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # definimos url para el get 
        id_busqueda = self.data['id_busqueda']
        url = reverse('busqueda:busquedaById', args=[id_busqueda])
        
        # hacemos el get
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        #validar objeto
        self.assertEquals(response.json()['id_busqueda'], self.data['id_busqueda'])
        self.assertEquals(response.json()['user'], self.data['user'])
        self.assertEquals(response.json()['nombre'], self.data['nombre'])
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
        print("Fecha peticion")
        print(response.json()['fecha_peticion'])
        print("Fecha finalizacion")
        print(response.json()['fecha_finalizacion'])
        self.assertEquals(response.json()['finalizado'], True)
        self.assertEquals(response.json()['tiene_tweets'], True)
        
    
    def test_get(self):

        response = self.client.post(self.url, self.data, format('json'))
        # response ok?
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # hacemos el get
        response_get = self.client.get(self.url)
        self.assertEquals(response_get.status_code, status.HTTP_200_OK)
        #validar objeto
        self.assertEquals(response_get.json()[0]['id_busqueda'], self.data['id_busqueda'])
        self.assertEquals(response_get.json()[0]['user'], self.data['user'])
        self.assertEquals(response_get.json()[0]['ands'], self.data['ands'])
        self.assertEquals(response_get.json()[0]['phrase'], self.data['phrase'])
        self.assertEquals(response_get.json()[0]['ors'], self.data['ors'])
        self.assertEquals(response_get.json()[0]['nots'], self.data['nots'])
        self.assertEquals(response_get.json()[0]['tags'], self.data['tags'])
        self.assertEquals(response_get.json()[0]['respondiendo'], self.data['respondiendo'])
        self.assertEquals(response_get.json()[0]['mencionando'], self.data['mencionando'])
        self.assertEquals(response_get.json()[0]['From'], self.data['From'])
        self.assertEquals(response_get.json()[0]['fecha_hasta'], self.data['fecha_hasta'])
        self.assertEquals(response_get.json()[0]['fecha_desde'], self.data['fecha_desde'])
        #self.assertEquals(response_get.json()[0]['fecha_peticion'], self.data['fecha_peticion'])
        #self.assertEquals(response_get.json()[0]['fecha_finalizacion'], self.data['fecha_finalizacion'])
        self.assertEquals(response_get.json()[0]['finalizado'], self.data['finalizado'])
        self.assertEquals(response_get.json()[0]['tiene_tweets'], self.data['tiene_tweets'])
        

    
    def test_get_byBusquedaId(self):
        # primero el post para guardar los datos
        response = self.client.post(self.url, self.data2, format('json'))
        # response ok?
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # definimos url para el get 
        id_busqueda = self.data2['id_busqueda']
        url = reverse('busqueda:busquedaById', args=[id_busqueda])
        
        # hacemos el get
        response_get = self.client.get(url)
        self.assertEquals(response_get.status_code, status.HTTP_200_OK)

        #validar objeto
        self.assertEquals(response_get.json()[0]['id_busqueda'], self.data2['id_busqueda'])
        self.assertEquals(response_get.json()[0]['user'], self.data2['user'])
        self.assertEquals(response_get.json()[0]['ands'], self.data2['ands'])
        self.assertEquals(response_get.json()[0]['phrase'], self.data2['phrase'])
        self.assertEquals(response_get.json()[0]['ors'], self.data2['ors'])
        self.assertEquals(response_get.json()[0]['nots'], self.data2['nots'])
        self.assertEquals(response_get.json()[0]['tags'], self.data2['tags'])
        self.assertEquals(response_get.json()[0]['respondiendo'], self.data2['respondiendo'])
        self.assertEquals(response_get.json()[0]['mencionando'], self.data2['mencionando'])
        self.assertEquals(response_get.json()[0]['From'], self.data2['From'])
        self.assertEquals(response_get.json()[0]['fecha_hasta'], self.data2['fecha_hasta'])
        self.assertEquals(response_get.json()[0]['fecha_desde'], self.data2['fecha_desde'])
        #self.assertEquals(response_get.json()[0]['fecha_peticion'], self.data2['fecha_peticion'])
        #self.assertEquals(response_get.json()[0]['fecha_finalizacion'], self.data2['fecha_finalizacion'])
        self.assertEquals(response_get.json()[0]['finalizado'], self.data2['finalizado'])
        self.assertEquals(response_get.json()[0]['tiene_tweets'], self.data2['tiene_tweets'])  
        

    def test_get_finalizadas(self):
        # primero el post para guardar los datos
        response = self.client.post(self.url, self.data2, format('json'))
        # response ok?
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # definimos url para el get 
        url = reverse('busqueda:finalizadas')
        
        # hacemos el get
        response_get = self.client.get(url)
        self.assertEquals(response_get.status_code, status.HTTP_200_OK)

        #validar objeto
        self.assertEquals(response_get.json()['id_busqueda'], self.data2['id_busqueda'])
        self.assertEquals(response_get.json()['user'], self.data2['user'])
        self.assertEquals(response_get.json()['ands'], self.data2['ands'])
        self.assertEquals(response_get.json()['phrase'], self.data2['phrase'])
        self.assertEquals(response_get.json()['ors'], self.data2['ors'])
        self.assertEquals(response_get.json()['nots'], self.data2['nots'])
        self.assertEquals(response_get.json()['tags'], self.data2['tags'])
        self.assertEquals(response_get.json()['respondiendo'], self.data2['respondiendo'])
        self.assertEquals(response_get.json()['mencionando'], self.data2['mencionando'])
        self.assertEquals(response_get.json()['From'], self.data2['From'])
        self.assertEquals(response_get.json()['fecha_hasta'], self.data2['fecha_hasta'])
        self.assertEquals(response_get.json()['fecha_desde'], self.data2['fecha_desde'])
        #self.assertEquals(response_get.json()['fecha_peticion'], self.data2['fecha_peticion'])
        #self.assertEquals(response_get.json()['fecha_finalizacion'], self.data2['fecha_finalizacion'])
        self.assertEquals(response_get.json()['finalizado'], self.data2['finalizado'])
        self.assertEquals(response_get.json()['tiene_tweets'], self.data2['tiene_tweets'])  
    
        
    
