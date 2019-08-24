from django.urls import path
from .views import BusquedaListCreate

app_name = 'busqueda'

urlpatterns = [
    path('', BusquedaListCreate.as_view(), name='create')
]