from django.db import models
from django.utils import timezone


class TweetsModel(models.Model):
    
    username = models.CharField(max_length=250, blank=True)
    text= models.CharField(max_length=250, blank=True)
    fecha= models.DateTimeField(blank=False, null=False)
    favs= models.IntegerField(blank=False, null=False)
    rts= models.IntegerField(blank=False, null=False)
    link= models.CharField(max_length=250, blank=True)
    label = models.CharField(max_length=250, blank=True)