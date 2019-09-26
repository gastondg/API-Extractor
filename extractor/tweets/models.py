from django.db import models
from django.utils import timezone


class TweetsModel(models.Model):
    
    username = models.CharField(max_length=250, blank=True)
    text= models.CharField(max_length=350, blank=True)
    fecha= models.DateTimeField(blank=False, null=False)
    likes= models.IntegerField(blank=False, null=False)
    replies= models.IntegerField(blank=False, null=False)
    rts= models.IntegerField(blank=False, null=False)
    url= models.CharField(max_length=250, blank=True)
    label = models.CharField(max_length=250, blank=True)
    id_busqueda = models.IntegerField()
    nube = models.CharField(max_length=350, blank=True)