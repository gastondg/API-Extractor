from rest_framework import serializers
from .models import TweetsModel


class TweetsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TweetsModel
        fields = '__all__'

    def create(self, validated_data):
        return TweetsModel.objects.create(**validated_data)