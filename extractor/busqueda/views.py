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
            busqueda_set.save()
            # guardamos la busqueda sin finalizar y ejecutamos la busqueda
            id_busqueda = busqueda_set.data['id_busqueda']
            # ejecutamos el subproceso
            path_env = "/env/bin/python3"
            subprocess.run(path_env + ' /scripts/extractor_tweets.py ' + str(id_busqueda) + ' | at now', shell=True)
            # env/bin/python3    
            return Response(busqueda_set.data, status=status.HTTP_201_CREATED)
        print("imprimiendo errores")
        print(busqueda_set.errors)
        return Response({
            'error' : busqueda_set.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = BusquedaSerializer(queryset, many=True)
        return Response(serializer.data)

    """ def get_queryset(self):

        filtros = {}

        if 'id_busqueda' in self.request.GET:
            filtros['id_busqueda'] = self.request.GET.get('id_busqueda')

        if 'user_id' in self.request.GET:
            filtros['user_id'] = self.request.GET.get('user_id')

        if 'finalizado' in self.request.GET:
                filtros['finalizado'] = self.request.GET.get('finalizado')
                # devuelve el no finalizado mas viejo, es decir el primero de la cola
                return BusquedaModel.objects.filter(**filtros).order_by("fecha_peticion")[:1]
        
        if filtros:
            return BusquedaModel.objects.filter(**filtros)
        else:
            return BusquedaModel.objects.all() """

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
        