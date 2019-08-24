from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from .serializers import HistoricalTradesSerializer
from .models import HistoricalTradesModel
import pandas as pd


class HistoricalTradesListCreateView(ListCreateAPIView):
    
    serializer_class = HistoricalTradesSerializer

    def post(self, request, *args, **kwargs):
        
        body = request.data #deberia ser una lista de dict

        # obtengo el serializer pasando los datos del request
        historical_set = HistoricalTradesSerializer(data=body, many=True)

        if historical_set.is_valid():
            historical_set.save()
            return Response(historical_set.data, status=status.HTTP_201_CREATED)
        
        return Response({
            'error' : historical_set.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):

        filtros = {}
        
        if 'symbol' in self.request.GET:
            filtros['symbol'] = self.request.GET.get('symbol')

        if 'id_trade' in self.request.GET:
            filtros['id_trade'] = self.request.GET.get('id_trade')

        if 'price_hasta' in self.request.GET:
            filtros['price__lte'] = self.request.GET.get('price_hasta')

        if 'price_desde' in self.request.GET:
            filtros['price__gte'] = self.request.GET.get('price_desde')

        if 'quantity_hasta' in self.request.GET:
            filtros['quantity__lte'] = self.request.GET.get('quantity_hasta')

        if 'quantity_desde' in self.request.GET:
            filtros['quantity__gte'] = self.request.GET.get('quantity_desde')

        if 'fecha_hasta' in self.request.GET:
            filtros['timestamp__lte'] = self.request.GET.get('fecha_hasta')

        if 'fecha_desde' in self.request.GET:
            filtros['timestamp__gte'] = self.request.GET.get('fecha_desde')

        if 'is_buyer_marker' in self.request.GET:
            filtros['is_buyer_marker'] = self.request.GET.get('is_buyer_marker')

        if 'is_best_match' in self.request.GET:
            filtros['is_best_match'] = self.request.GET.get('is_best_match')
        
        if ('last_from_symbol' in self.request.GET):
                filtros['symbol'] = self.request.GET.get('last_from_symbol')

                return HistoricalTradesModel.objects.filter(**filtros).order_by("-timestamp")[:1]
        
        if filtros:
            return HistoricalTradesModel.objects.filter(**filtros)
        else:
            return HistoricalTradesModel.objects.all()
