from .models import BusquedaModel
from .serializers import BusquedaSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


class BusquedaListCreate(generics.ListCreateAPIView):
    
    queryset = BusquedaModel.objects.all()
    serializer_class = BusquedaSerializer

    def post(self, request, *args, **kwargs):
      
        body = request.data  # deberia ser una lista de dict

        # obtengo el serializer pasando los datos del request
        busqueda_set = BusquedaSerializer(data=body, many=False)

        if busqueda_set.is_valid():
            busqueda_set.save()
            # si la busqueda es valida debemos:
            # 1. comprobar que Selenium no este ocupado
            # 2. empezas la busqueda
            
            return Response(busqueda_set.data, status=status.HTTP_201_CREATED)
            
        print(busqueda_set.errors)
        return Response({
            'error' : busqueda_set.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):

        filtros = {}

        if 'id_busqueda' in self.request.GET:
            filtros['id_busqueda'] = self.request.GET.get('id_busqueda')

        if 'user_id' in self.request.GET:
            filtros['user_id'] = self.request.GET.get('user_id')

        if 'finalizado' in self.request.GET:
                filtros['finalizado'] = self.request.GET.get('finalizado')
                # devuelve el no finalizado mas viejo, es decir el primero de la cola
                return HistoricalTradesModel.objects.filter(**filtros).order_by("fecha_peticion")[:1]
        
        if filtros:
            return HistoricalTradesModel.objects.filter(**filtros)
        else:
            return HistoricalTradesModel.objects.all()