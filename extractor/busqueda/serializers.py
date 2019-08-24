from rest_framework import serializers
from .models import BusquedaModel


class BusquedaSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusquedaModel
        fields = '__all__'

    def create(self, validated_data):
        return BusquedaModel.objects.create(**validated_data)