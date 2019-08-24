from django.db import models


class HistoricalTradesModel(models.Model):
    symbol = models.CharField(max_length=100)
    id_trade = models.IntegerField()
    price = models.FloatField()
    quantity = models.FloatField()
    quote_quantity = models.FloatField()
    timestamp = models.DateTimeField()
    is_buyer_maker = models.BooleanField()
    is_best_match = models.BooleanField()

