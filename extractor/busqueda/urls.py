from django.urls import path
from .views import BusquedaListCreate, ByBusquedaIdView, FinalizadasView, BusquedaFinalizada

app_name = 'busqueda'

urlpatterns = [
    path('', BusquedaListCreate.as_view(), name='create'),
    path('id_busqueda/<id_busqueda>', ByBusquedaIdView.as_view(), name="busquedaById"),
    path('finalizadas', FinalizadasView.as_view(), name='finalizadas'),
    path('busqueda_finalizada/<id_busqueda>', BusquedaFinalizada.as_view(), name='busqueda_finalizada'),

]