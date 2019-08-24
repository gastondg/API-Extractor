from django.test import tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime
from api.helpers import HTrades
from pprint import pprint


class HistoricalTradesTest(APITestCase):

    def setUp(self):

        self.url = reverse('historical_trades:create')

        self.data = [
            {
                "symbol": "ETHBTC",
                "id": 28457,
                "price": '4.00000100',
                "qty": '12.00000000',
                "quoteQty": '0.01',
                "time": 1551723240000,  # 03/04/2019 @ 3:14pm (UTC)
                "isBuyerMaker": False,
                "isBestMatch": True
            },
            {
                "symbol": "ETHBTC",
                "id": 28460,
                "price": '4.00000119',
                "qty": '17.00000000',
                "quoteQty": '0.01',
                "time": 1551796200000,  # 03/05/2019 @ 11:30am (UTC)
                "isBuyerMaker": True,
                "isBestMatch": False
            },
            {
                'symbol': 'EOSETH',
                'id': 13890684,
                'price': '0.02559900',
                'qty': '19.67000000',
                "quoteQty": '0.01',
                'time': 1551710700000,  # 03/04/2019 @ 11:46am (UTC)
                'isBuyerMaker': False,
                'isBestMatch': True
            },
            {
                'symbol': 'EOSETH',
                'id': 13890685,
                'price': '0.02560000',
                'qty': '189.84000000',
                "quoteQty": '0.01',
                'time': 1546269555000,  # 12/31/2018 @ 12:19pm (UTC)
                'isBuyerMaker': False,
                'isBestMatch': True
            },
            {
                'symbol': 'BTCUSDT',
                'id': 104440473,
                'price': '3717.24000000',
                'qty': '0.00278000',
                "quoteQty": '0.01',
                'time': 1540494915000,  # 10/25/2018 @ 4:15pm (UTC)
                'isBuyerMaker': False,
                'isBestMatch': True
            },
            {
                'symbol': 'BTCUSDT',
                'id': 104440474,
                'price': '3716.91000000',
                'qty': '0.07819200',
                "quoteQty": '0.01',
                'time': 1538430300000,  # 10/01/2018 @ 6:45pm (UTC)
                'isBuyerMaker': True,
                'isBestMatch': True
            }

        ]

    
    def test_create(self):
        h_trades = HTrades()
        json = h_trades.transform_htrades(json=self.data)
        response = self.client.post(self.url, json, format('json'))
        #Validar response ok
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #Validar primer objeto
        self.assertEqual(response.json()[0]['symbol'], self.data[0]['symbol'])
        self.assertEqual(response.json()[0]['id_trade'], self.data[0]['id'])
        self.assertEqual(response.json()[0]['price'], float(self.data[0]['price']))
        self.assertEqual(response.json()[0]['quantity'], float(self.data[0]['qty']))
        self.assertEqual(response.json()[0]['quote_quantity'], float(self.data[0]['quoteQty']))
        self.assertEqual(response.json()[0]['timestamp'], self.int_to_date(self.data[0]['time']))
        self.assertEqual(response.json()[0]['is_buyer_maker'], self.data[0]['isBuyerMaker'])
        self.assertEqual(response.json()[0]['is_best_match'], self.data[0]['isBestMatch'])
        
        #Validar segundo objeto
        self.assertEqual(response.json()[1]['symbol'], self.data[1]['symbol'])
        self.assertEqual(response.json()[1]['id_trade'], self.data[1]['id'])
        self.assertEqual(response.json()[1]['price'], float(self.data[1]['price']))
        self.assertEqual(response.json()[1]['quantity'], float(self.data[1]['qty']))
        self.assertEqual(response.json()[1]['quote_quantity'], float(self.data[1]['quoteQty']))
        self.assertEqual(response.json()[1]['timestamp'], self.int_to_date(self.data[1]['time']))
        self.assertEqual(response.json()[1]['is_buyer_maker'], self.data[1]['isBuyerMaker'])
        self.assertEqual(response.json()[1]['is_best_match'], self.data[1]['isBestMatch'])

    
    def int_to_date(self, fecha_int):
        date = datetime.fromtimestamp(fecha_int / 1e3)
        date = date.strftime('%Y-%m-%dT%H:%M:%SZ')
        return date

    
    def test_get_HTList(self):
        #get general
        h_trades = HTrades()
        json = h_trades.transform_htrades(json=self.data)
        response = self.client.post(self.url, json, format('json')) #no deberia tener errores ya esta testeado
        response = self.client.get(self.url)

        # response ok?
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), len(self.data))
        
        #validar primer objeto
        self.assertEqual(response.json()[0]['symbol'], self.data[0]['symbol'])
        self.assertEqual(response.json()[0]['id_trade'], self.data[0]['id'])
        self.assertEqual(response.json()[0]['price'], float(self.data[0]['price']))
        self.assertEqual(response.json()[0]['quantity'], float(self.data[0]['qty']))
        self.assertEqual(response.json()[0]['quote_quantity'], float(self.data[0]['quoteQty']))        
        self.assertEqual(response.json()[0]['timestamp'], self.int_to_date(self.data[0]['time']))
        self.assertEqual(response.json()[0]['is_buyer_maker'], self.data[0]['isBuyerMaker'])
        self.assertEqual(response.json()[0]['is_best_match'], self.data[0]['isBestMatch'])

        #validar segundo objeto
        self.assertEqual(response.json()[1]['symbol'], self.data[1]['symbol'])
        self.assertEqual(response.json()[1]['id_trade'], self.data[1]['id'])
        self.assertEqual(response.json()[1]['price'], float(self.data[1]['price']))
        self.assertEqual(response.json()[1]['quantity'], float(self.data[1]['qty']))
        self.assertEqual(response.json()[1]['quote_quantity'], float(self.data[1]['quoteQty']))
        self.assertEqual(response.json()[1]['timestamp'], self.int_to_date(self.data[1]['time']))
        self.assertEqual(response.json()[1]['is_buyer_maker'], self.data[1]['isBuyerMaker'])
        self.assertEqual(response.json()[1]['is_best_match'], self.data[1]['isBestMatch'])

        #validar sexto objeto
        self.assertEqual(response.json()[5]['symbol'], self.data[5]['symbol'])
        self.assertEqual(response.json()[5]['id_trade'], self.data[5]['id'])
        self.assertEqual(response.json()[5]['price'], float(self.data[5]['price']))
        self.assertEqual(response.json()[5]['quantity'], float(self.data[5]['qty']))
        self.assertEqual(response.json()[5]['quote_quantity'], float(self.data[5]['quoteQty']))
        self.assertEqual(response.json()[5]['timestamp'], self.int_to_date(self.data[5]['time']))
        self.assertEqual(response.json()[5]['is_buyer_maker'], self.data[5]['isBuyerMaker'])
        self.assertEqual(response.json()[5]['is_best_match'], self.data[5]['isBestMatch'])

    
    def test_get_HTList_by_symbol(self):
        #get general
        h_trades = HTrades()
        json = h_trades.transform_htrades(json=self.data)
        response = self.client.post(self.url, json, format('json')) #no deberia tener errores ya esta testeado
        response = self.client.get(self.url + '?symbol=EOSETH')

        # response ok?
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 2)
        
        #validar primer objeto
        self.assertEqual(response.json()[0]['symbol'], self.data[2]['symbol'])
        self.assertEqual(response.json()[0]['id_trade'], self.data[2]['id'])
        self.assertEqual(response.json()[0]['price'], float(self.data[2]['price']))
        self.assertEqual(response.json()[0]['quantity'], float(self.data[2]['qty']))
        self.assertEqual(response.json()[0]['quote_quantity'], float(self.data[0]['quoteQty']))
        self.assertEqual(response.json()[0]['timestamp'], self.int_to_date(
            self.data[2]['time']))
        self.assertEqual(response.json()[0]['is_buyer_maker'], self.data[2]['isBuyerMaker'])
        self.assertEqual(response.json()[0]['is_best_match'], self.data[2]['isBestMatch'])

        #validar segundo objeto
        self.assertEqual(response.json()[1]['symbol'], self.data[3]['symbol'])
        self.assertEqual(response.json()[1]['id_trade'], self.data[3]['id'])
        self.assertEqual(response.json()[1]['price'], float(self.data[3]['price']))
        self.assertEqual(response.json()[1]['quantity'], float(self.data[3]['qty']))
        self.assertEqual(response.json()[1]['quote_quantity'], float(self.data[3]['quoteQty']))
        self.assertEqual(response.json()[1]['timestamp'], self.int_to_date(self.data[3]['time']))
        self.assertEqual(response.json()[1]['is_buyer_maker'], self.data[3]['isBuyerMaker'])
        self.assertEqual(response.json()[1]['is_best_match'], self.data[3]['isBestMatch'])

    
    def test_get_HTList_by_price_hasta(self):
        #get general
        h_trades = HTrades()
        json = h_trades.transform_htrades(json=self.data)
        response = self.client.post(self.url, json, format('json')) #no deberia tener errores ya esta testeado
        response = self.client.get(self.url + '?price_hasta=1.5')

        # response ok?
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 2)
        
        #validar primer objeto
        self.assertEqual(response.json()[0]['symbol'], self.data[2]['symbol'])
        self.assertEqual(response.json()[0]['id_trade'], self.data[2]['id'])
        self.assertEqual(response.json()[0]['price'], float(self.data[2]['price']))
        self.assertEqual(response.json()[0]['quantity'], float(self.data[2]['qty']))
        self.assertEqual(response.json()[0]['quote_quantity'], float(self.data[2]['quoteQty']))
        self.assertEqual(response.json()[0]['timestamp'], self.int_to_date(self.data[2]['time']))
        self.assertEqual(response.json()[0]['is_buyer_maker'], self.data[2]['isBuyerMaker'])
        self.assertEqual(response.json()[0]['is_best_match'], self.data[2]['isBestMatch'])

        #validar segundo objeto
        self.assertEqual(response.json()[1]['symbol'], self.data[3]['symbol'])
        self.assertEqual(response.json()[1]['id_trade'], self.data[3]['id'])
        self.assertEqual(response.json()[1]['price'], float(self.data[3]['price']))
        self.assertEqual(response.json()[1]['quantity'], float(self.data[3]['qty']))
        self.assertEqual(response.json()[1]['quote_quantity'], float(self.data[3]['quoteQty']))
        self.assertEqual(response.json()[1]['timestamp'], self.int_to_date(self.data[3]['time']))
        self.assertEqual(response.json()[1]['is_buyer_maker'], self.data[3]['isBuyerMaker'])
        self.assertEqual(response.json()[1]['is_best_match'], self.data[3]['isBestMatch'])

    
    def test_get_HTList_by_price_desde(self):
        #get general
        h_trades = HTrades()
        json = h_trades.transform_htrades(json=self.data)
        response = self.client.post(self.url, json, format('json')) #no deberia tener errores ya esta testeado
        response = self.client.get(self.url + '?price_desde=3000.80')

        # response ok?
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 2)
        
        #validar primer objeto BTC
        self.assertEqual(response.json()[0]['symbol'], self.data[4]['symbol'])
        self.assertEqual(response.json()[0]['id_trade'], self.data[4]['id'])
        self.assertEqual(response.json()[0]['price'], float(self.data[4]['price']))
        self.assertEqual(response.json()[0]['quantity'], float(self.data[4]['qty']))
        self.assertEqual(response.json()[0]['quote_quantity'], float(self.data[4]['quoteQty']))
        self.assertEqual(response.json()[0]['timestamp'],self.int_to_date(self.data[4]['time']))
        self.assertEqual(response.json()[0]['is_buyer_maker'], self.data[4]['isBuyerMaker'])
        self.assertEqual(response.json()[0]['is_best_match'], self.data[4]['isBestMatch'])

        #validar segundo objeto BTC
        self.assertEqual(response.json()[1]['symbol'], self.data[5]['symbol'])
        self.assertEqual(response.json()[1]['id_trade'], self.data[5]['id'])
        self.assertEqual(response.json()[1]['price'], float(self.data[5]['price']))
        self.assertEqual(response.json()[1]['quantity'], float(self.data[5]['qty']))
        self.assertEqual(response.json()[1]['quote_quantity'], float(self.data[5]['quoteQty']))
        self.assertEqual(response.json()[1]['timestamp'],self.int_to_date(self.data[5]['time']))
        self.assertEqual(response.json()[1]['is_buyer_maker'], self.data[5]['isBuyerMaker'])
        self.assertEqual(response.json()[1]['is_best_match'], self.data[5]['isBestMatch'])

    
    def test_get_HTList_by_quantity_hasta(self):
        #get general
        h_trades = HTrades()
        json = h_trades.transform_htrades(json=self.data)
        response = self.client.post(self.url, json, format('json')) #no deberia tener errores ya esta testeado
        response = self.client.get(self.url + '?quantity_hasta=1.5')

        # response ok?
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 2)
       #validar primer objeto
        self.assertEqual(response.json()[0]['symbol'], self.data[4]['symbol'])
        self.assertEqual(response.json()[0]['id_trade'], self.data[4]['id'])
        self.assertEqual(response.json()[0]['price'], float(self.data[4]['price']))
        self.assertEqual(response.json()[0]['quantity'], float(self.data[4]['qty']))
        self.assertEqual(response.json()[0]['quote_quantity'], float(self.data[4]['quoteQty']))
        self.assertEqual(response.json()[0]['timestamp'],self.int_to_date(self.data[4]['time']))
        self.assertEqual(response.json()[0]['is_buyer_maker'], self.data[4]['isBuyerMaker'])
        self.assertEqual(response.json()[0]['is_best_match'], self.data[4]['isBestMatch'])

        #validar segundo objeto
        self.assertEqual(response.json()[1]['symbol'], self.data[5]['symbol'])
        self.assertEqual(response.json()[1]['id_trade'], self.data[5]['id'])
        self.assertEqual(response.json()[1]['price'], float(self.data[5]['price']))
        self.assertEqual(response.json()[1]['quantity'], float(self.data[5]['qty']))
        self.assertEqual(response.json()[1]['quote_quantity'], float(self.data[5]['quoteQty']))
        self.assertEqual(response.json()[1]['timestamp'], self.int_to_date(self.data[5]['time']))
        self.assertEqual(response.json()[1]['is_buyer_maker'], self.data[5]['isBuyerMaker'])
        self.assertEqual(response.json()[1]['is_best_match'], self.data[5]['isBestMatch'])

    
    def test_get_HTList_by_quantity_desde(self):
        #get general
        h_trades = HTrades()
        json = h_trades.transform_htrades(json=self.data)
        response = self.client.post(self.url, json, format('json')) #no deberia tener errores ya esta testeado
        response = self.client.get(self.url + '?quantity_desde=18')

        # response ok?
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 2)
       #validar primer objeto BTC
        self.assertEqual(response.json()[0]['symbol'], self.data[2]['symbol'])
        self.assertEqual(response.json()[0]['id_trade'], self.data[2]['id'])
        self.assertEqual(response.json()[0]['price'], float(self.data[2]['price']))
        self.assertEqual(response.json()[0]['quantity'], float(self.data[2]['qty']))
        self.assertEqual(response.json()[0]['quote_quantity'], float(self.data[2]['quoteQty']))
        self.assertEqual(response.json()[0]['timestamp'], self.int_to_date(self.data[2]['time']))
        self.assertEqual(response.json()[0]['is_buyer_maker'], self.data[2]['isBuyerMaker'])
        self.assertEqual(response.json()[0]['is_best_match'], self.data[2]['isBestMatch'])

        #validar segundo objeto BTC
        self.assertEqual(response.json()[1]['symbol'], self.data[3]['symbol'])
        self.assertEqual(response.json()[1]['id_trade'], self.data[3]['id'])
        self.assertEqual(response.json()[1]['price'], float(self.data[3]['price']))
        self.assertEqual(response.json()[1]['quantity'], float(self.data[3]['qty']))
        self.assertEqual(response.json()[1]['quote_quantity'], float(self.data[3]['quoteQty']))
        self.assertEqual(response.json()[1]['timestamp'], self.int_to_date(self.data[3]['time']))
        self.assertEqual(response.json()[1]['is_buyer_maker'], self.data[3]['isBuyerMaker'])
        self.assertEqual(response.json()[1]['is_best_match'], self.data[3]['isBestMatch'])
        
    
    def test_get_HTList_by_fecha_hasta(self):
        #get general
        h_trades = HTrades()
        json = h_trades.transform_htrades(json=self.data)
        response = self.client.post(self.url, json, format('json')) #no deberia tener errores ya esta testeado
        response = self.client.get(self.url + '?fecha_hasta=2018-10-31') #31 de octubre 2018

        # response ok?
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 2)
        
        #validar primer objeto BTC
        self.assertEqual(response.json()[0]['symbol'], self.data[4]['symbol'])
        self.assertEqual(response.json()[0]['id_trade'], self.data[4]['id'])
        self.assertEqual(response.json()[0]['price'], float(self.data[4]['price']))
        self.assertEqual(response.json()[0]['quantity'], float(self.data[4]['qty']))
        self.assertEqual(response.json()[0]['quote_quantity'], float(self.data[4]['quoteQty']))
        self.assertEqual(response.json()[0]['timestamp'], self.int_to_date(self.data[4]['time']))
        self.assertEqual(response.json()[0]['is_buyer_maker'], self.data[4]['isBuyerMaker'])
        self.assertEqual(response.json()[0]['is_best_match'], self.data[4]['isBestMatch'])
 
        #validar segundo objeto BTC
        self.assertEqual(response.json()[1]['symbol'], self.data[5]['symbol'])
        self.assertEqual(response.json()[1]['id_trade'], self.data[5]['id'])
        self.assertEqual(response.json()[1]['price'], float(self.data[5]['price']))
        self.assertEqual(response.json()[1]['quantity'], float(self.data[5]['qty']))
        self.assertEqual(response.json()[1]['quote_quantity'], float(self.data[5]['quoteQty']))
        self.assertEqual(response.json()[1]['timestamp'], self.int_to_date(self.data[5]['time']))
        self.assertEqual(response.json()[1]['is_buyer_maker'], self.data[5]['isBuyerMaker'])
        self.assertEqual(response.json()[1]['is_best_match'], self.data[5]['isBestMatch'])

    
    def test_get_HTList_by_fecha_desde(self):
        #get general
        h_trades = HTrades()
        json = h_trades.transform_htrades(json=self.data)
        response = self.client.post(self.url, json, format('json')) #no deberia tener errores ya esta testeado
        response = self.client.get(
            self.url + '?fecha_desde=2019-01-15')  # 15 enero 2019

        # response ok?
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 3)
        
        #validar primer objeto 
        self.assertEqual(response.json()[0]['symbol'], self.data[0]['symbol'])
        self.assertEqual(response.json()[0]['id_trade'], self.data[0]['id'])
        self.assertEqual(response.json()[0]['price'], float(self.data[0]['price']))
        self.assertEqual(response.json()[0]['quantity'], float(self.data[0]['qty']))
        self.assertEqual(response.json()[0]['quote_quantity'], float(self.data[0]['quoteQty']))
        self.assertEqual(response.json()[0]['timestamp'], self.int_to_date(self.data[0]['time']))
        self.assertEqual(response.json()[0]['is_buyer_maker'], self.data[0]['isBuyerMaker'])
        self.assertEqual(response.json()[0]['is_best_match'], self.data[0]['isBestMatch'])

        #validar segundo objeto 
        self.assertEqual(response.json()[1]['symbol'], self.data[1]['symbol'])
        self.assertEqual(response.json()[1]['id_trade'], self.data[1]['id'])
        self.assertEqual(response.json()[1]['price'], float(self.data[1]['price']))
        self.assertEqual(response.json()[1]['quantity'], float(self.data[1]['qty']))
        self.assertEqual(response.json()[1]['quote_quantity'], float(self.data[1]['quoteQty']))
        self.assertEqual(response.json()[1]['timestamp'], self.int_to_date(self.data[1]['time']))
        self.assertEqual(response.json()[1]['is_buyer_maker'], self.data[1]['isBuyerMaker'])
        self.assertEqual(response.json()[1]['is_best_match'], self.data[1]['isBestMatch'])

        #validar tercer objeto 
        self.assertEqual(response.json()[2]['symbol'], self.data[2]['symbol'])
        self.assertEqual(response.json()[2]['id_trade'], self.data[2]['id'])
        self.assertEqual(response.json()[2]['price'], float(self.data[2]['price']))
        self.assertEqual(response.json()[2]['quantity'], float(self.data[2]['qty']))
        self.assertEqual(response.json()[2]['quote_quantity'], float(self.data[2]['quoteQty']))
        self.assertEqual(response.json()[2]['timestamp'], self.int_to_date(self.data[2]['time']))
        self.assertEqual(response.json()[2]['is_buyer_maker'], self.data[2]['isBuyerMaker'])
        self.assertEqual(response.json()[2]['is_best_match'], self.data[2]['isBestMatch'])

    
    def test_get_HTList_by_fecha_desde_hasta(self):
        #get general
        h_trades = HTrades()
        json = h_trades.transform_htrades(json=self.data)
        response = self.client.post(self.url, json, format('json')) #no deberia tener errores ya esta testeado
        response = self.client.get(self.url + '?fecha_desde=2018-12-20&fecha_hasta=2019-01-01')

        # response ok?
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 1)
        
        #validar objeto
        self.assertEqual(response.json()[0]['symbol'], self.data[3]['symbol'])
        self.assertEqual(response.json()[0]['id_trade'], self.data[3]['id'])
        self.assertEqual(response.json()[0]['price'], float(self.data[3]['price']))
        self.assertEqual(response.json()[0]['quantity'], float(self.data[3]['qty']))
        self.assertEqual(response.json()[0]['quote_quantity'], float(self.data[3]['quoteQty']))
        self.assertEqual(response.json()[0]['timestamp'], self.int_to_date(self.data[3]['time']))
        self.assertEqual(response.json()[0]['is_buyer_maker'], self.data[3]['isBuyerMaker'])
        self.assertEqual(response.json()[0]['is_best_match'], self.data[3]['isBestMatch'])

    
    def test_get_last_from_symbol(self):
        #get general
        h_trades = HTrades()
        json = h_trades.transform_htrades(json=self.data)
        response = self.client.post(self.url, json, format('json')) #no deberia tener errores ya esta testeado
        response = self.client.get(self.url + '?last_from_symbol=ETHBTC')

        # response ok?
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 1)

        #validar segundo objeto ETHBTC
        self.assertEqual(response.json()[0]['symbol'], self.data[1]['symbol'])
        self.assertEqual(response.json()[0]['id_trade'], self.data[1]['id'])
        self.assertEqual(response.json()[0]['price'], float(self.data[1]['price']))
        self.assertEqual(response.json()[0]['quantity'], float(self.data[1]['qty']))
        self.assertEqual(response.json()[0]['quote_quantity'], float(self.data[1]['quoteQty']))
        self.assertEqual(response.json()[0]['timestamp'], self.int_to_date(self.data[1]['time']))
        self.assertEqual(response.json()[0]['is_buyer_maker'], self.data[1]['isBuyerMaker'])
        self.assertEqual(response.json()[0]['is_best_match'], self.data[1]['isBestMatch'])
