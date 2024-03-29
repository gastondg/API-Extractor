from rest_framework import serializers
from .models import BusquedaModel


class BusquedaSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusquedaModel
        fields = '__all__'
        fields = [  
                    'user',
                    'id_busqueda',
                    'nombre',
                    'ands',
                    'phrase',
                    'ors',
                    'nots',
                    'tags',
                    'respondiendo',
                    'mencionando',
                    'From',
                    'fecha_desde',
                    'fecha_hasta',
                    'fecha_peticion',
                    'fecha_finalizacion',
                    'finalizado',
                    'es_cuenta',
                    'tiene_tweets', 
                    ]

    def create(self, validated_data):
        return BusquedaModel.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.save()
        return instance