from .models import BusquedaModel
from .serializers import BusquedaSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from pprint import pprint
import subprocess
from datetime import datetime



class BusquedaListCreate(generics.ListCreateAPIView):
    
    queryset = BusquedaModel.objects.all()
    serializer_class = BusquedaSerializer

    def post(self, request, *args, **kwargs):
      
        body = request.data  # deberia ser una lista de dict

        # obtengo el serializer pasando los datos del request
        busqueda_set = BusquedaSerializer(data=body, many=False)
        #busqueda_set.data['fecha_peticion'] = datetime.now()

        if busqueda_set.is_valid():
            # busqueda_set.save()
            # guardamos la busqueda sin finalizar y ejecutamos la busqueda
            id_busqueda = busqueda_set.data['id_busqueda']
            # ejecutamos el subproceso
            #path = "/home/gastondg/Proyecto/API-Extractor"
            path_env = "/env/bin/python3"
            path_script ="/scripts/extractor_tweets.py"
            s1 = subprocess.run(path_env + " " + path_script + " " + str(id_busqueda) + " | at now >> prueba2.txt", shell=True)
            s2 = subprocess.run("/env/bin/python3 /scripts/prueba_print.py 3 | at now >> prueba_print.txt", shell = True)
            print("Imprimiendo resultados de s1: ")
            print(s1)
            print("Imprimiendo resultados de s2: ")
            print(s2)               
            return Response(busqueda_set.data, status=status.HTTP_201_CREATED)
       
        return Response({
            'error' : busqueda_set.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = BusquedaSerializer(queryset, many=True)
        return Response(serializer.data)


class ByBusquedaIdView(APIView):

    serializer_class = BusquedaSerializer

    def get(self, request, *args, **kwargs):
        """
        Get busqueda con ese id
        Devuelve una lista de un elemento
        """
        if 'id_busqueda' not in kwargs:
            return Response({
                'error': 'id_busqueda required'
            }, status=400)

        #busq = BusquedaModel.objects.filter(id_busqueda = kwargs['id_busqueda'])
        busq = BusquedaModel.objects.get(id_busqueda = kwargs['id_busqueda'])

        return Response(BusquedaSerializer(busq, many=False).data)


class ByUserIdView(APIView):

    serializer_class = BusquedaSerializer

    def get(self, request, *args, **kwargs):
        """
        Get busqueda con ese id
        Devuelve una lista de un elemento
        """
        if 'user' not in kwargs:
            return Response({
                'error': 'user id required'
            }, status=400)

        #busq = BusquedaModel.objects.filter(id_busqueda = kwargs['id_busqueda'])
        busq = BusquedaModel.objects.get(user = kwargs['user'])

        return Response(BusquedaSerializer(busq, many=False).data)


class FinalizadasView(generics.ListAPIView):
    """
    Devuelve las busquedas finalizadas
    """
    serializer_class = BusquedaSerializer

    def get_queryset(self):

        id_busqueda = self.request.query_params.get('id_busqueda')

        if id_busqueda:
            queryset = BusquedaModel.objects.filter(finalizado=True, id_busqueda=id_busqueda)
        else:
            queryset = BusquedaModel.objects.filter(finalizado=True)

        return queryset


class BusquedaFinalizada(APIView):
    
    queryset = BusquedaModel.objects.all()
    serializer_class = BusquedaSerializer

    def put(self, request, *args, **kwargs):
        """ 
        Actualiza la busqueda a Finalizada = True
        """
        if 'id_busqueda' not in kwargs:
            return Response({
                'error': 'id_busqueda required'
            }, status=400)

        busq = BusquedaModel.objects.filter(id_busqueda = kwargs['id_busqueda']).update(finalizado=True, 
                                            fecha_finalizacion = datetime.today().strftime('%Y-%m-%d'),
                                            tiene_tweets=True)

        if busq >= 1: 
            return Response(status=200)
        else:
            # si da 0 algo paso y no se pudo hacer el update
            # mirar log si ocurre este error
            return Response(status=500)
        
class BusquedaVacia(APIView):
    
    queryset = BusquedaModel.objects.all()
    serializer_class = BusquedaSerializer

    def put(self, request, *args, **kwargs):
        """ 
        Actualiza la busqueda a tiene_tweets = False
        """
        if 'id_busqueda' not in kwargs:
            return Response({
                'error': 'id_busqueda required'
            }, status=400)

        busq = BusquedaModel.objects.filter(id_busqueda = kwargs['id_busqueda']).update(finalizado=True, 
                                            fecha_finalizacion = datetime.today().strftime('%Y-%m-%d'),
                                            tiene_tweets=False)

        if busq >= 1: 
            return Response(status=200)
        else:
            # si da 0 algo paso y no se pudo hacer el update
            # mirar log si ocurre este error
            return Response(status=500)