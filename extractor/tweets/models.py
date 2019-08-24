from django.db import models
from django.utils import timezone


class TweetsModel(models.Model):
    username = models.CharField()
    text= models.CharField()
    fecha= models.DateTimeField()
    favs= models.IntegerField()
    rts= models.IntegerField()
    link= models.CharField()
    label = models.CharField()