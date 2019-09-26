from django.db import models
from django.utils import timezone


class BusquedaModel(models.Model):
    user = models.IntegerField()
    id_busqueda = models.IntegerField(blank=False)
    nombre = models.CharField(max_length=250,blank=False,null=False)
    ands = models.CharField(max_length=250,blank=True)
    phrase = models.CharField(max_length=250,blank=True)
    ors = models.CharField(max_length=250,blank=True)
    nots = models.CharField(max_length=250,blank=True)
    tags = models.CharField(max_length=250,blank=True)
    respondiendo = models.CharField(max_length=250,blank=True)
    mencionando = models.CharField(max_length=250,blank=True)
    From = models.CharField(max_length=250,blank=True)
    fecha_desde = models.DateField(blank=True,null=True)
    fecha_hasta = models.DateField(blank=True,null=True)
    fecha_peticion = models.DateTimeField(default=timezone.now,blank=True,null=True)
    fecha_finalizacion = models.DateField(blank=True,null=True)
    finalizado = models.BooleanField(default=False)
    es_cuenta = models.BooleanField(null = True)
    tiene_tweets = models.BooleanField(null = True)

    def __str__(self):
        return str(self.user)+' '+str(self.fecha_peticion)

    
