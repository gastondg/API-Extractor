from rest_framework import serializers
from .models import HistoricalTradesModel


class HistoricalTradesSerializer(serializers.ModelSerializer):

    class Meta:
        model = HistoricalTradesModel
        fields = ('symbol', 'id_trade', 'price', 'quantity', 'quote_quantity',
                  'timestamp', 'is_buyer_maker', 'is_best_match')

    def create(self, validated_data):
        return HistoricalTradesModel.objects.create(**validated_data)
