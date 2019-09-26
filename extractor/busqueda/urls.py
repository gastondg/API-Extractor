from django.urls import path
from .views import BusquedaListCreate, ByBusquedaIdView, FinalizadasView, BusquedaFinalizada, ByUserIdView, BusquedaVacia

app_name = 'busqueda'

urlpatterns = [
    path('', BusquedaListCreate.as_view(), name='create'),
    path('id_busqueda/<id_busqueda>', ByBusquedaIdView.as_view(), name="busquedaById"),
    path('user/<user>', ByUserIdView.as_view(), name="userById"),
    path('finalizadas', FinalizadasView.as_view(), name='finalizadas'),
    path('busqueda_finalizada/<id_busqueda>', BusquedaFinalizada.as_view(), name='busqueda_finalizada'),
    path('busqueda_vacia/<id_busqueda>', BusquedaFinalizada.as_view(), name='busqueda_vacia'),

]