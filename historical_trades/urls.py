from django.urls import path
from .views import HistoricalTradesListCreateView

app_name = 'historical_trades'

urlpatterns = [
    path('', HistoricalTradesListCreateView.as_view(), name='create')
]
