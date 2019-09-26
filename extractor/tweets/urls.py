from django.urls import path
from .views import TweetsListCreate, ByBusquedaIdView

app_name = 'tweets'

urlpatterns = [
    path('', TweetsListCreate.as_view(), name='create'),
    path('id_busqueda/<id_busqueda>', ByBusquedaIdView.as_view(), name="busquedaById"),
]