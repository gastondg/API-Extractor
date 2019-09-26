from .models import TweetsModel
from .serializers import TweetsSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class TweetsListCreate(generics.ListCreateAPIView):
    
    queryset = TweetsModel.objects.all()
    serializer_class = TweetsSerializer

    def post(self, request, *args, **kwargs):
      
        body = request.data  # deberia ser una lista de dict

        # obtengo el serializer pasando los datos del request
        tweets_set = TweetsSerializer(data=body, many=True)

        if tweets_set.is_valid():
            tweets_set.save()
            
            return Response(tweets_set.data, status=status.HTTP_201_CREATED)
        
        print(tweets_set.errors)
        return Response({
            'error' : tweets_set.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ByBusquedaIdView(APIView):

    serializer_class = TweetsSerializer

    def get(self, request, *args, **kwargs):
        """
        Get tweets por id de busqueda
        Devuelve una lista de un elemento
        """
        if 'id_busqueda' not in kwargs:
            return Response({
                'error': 'id_busqueda required'
            }, status=400)

        tweets = TweetsModel.objects.filter(id_busqueda = kwargs['id_busqueda'])

        return Response(TweetsSerializer(tweets, many=True).data)