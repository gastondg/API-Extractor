from django.db import models
from django.utils import timezone


class BusquedaModel(models.Model):
    
    id_busqueda = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(blank=False)
    
    ands = models.CharField(max_length=250, blank=True)
    phrase = models.CharField(max_length=250, blank=True)
    ors = models.CharField(max_length=250, blank=True)
    nots = models.CharField(max_length=250, blank=True)
    tags = models.CharField(max_length=250, blank=True)
    respondiendo = models.CharField(max_length=250, blank=True)
    mencionando = models.CharField(max_length=250, blank=True)
    From = models.CharField(max_length=250, blank=True)
    fecha_desde = models.DateField(blank=False, null=False)
    fecha_hasta = models.DateField(blank=False, null=False)
    fecha_peticion = models.DateField(default=timezone.now)
    fecha_finalizacion = models.DateField(blank=True, null=True)
    finalizado = models.BooleanField(default=False)

    
