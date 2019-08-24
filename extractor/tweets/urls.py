from django.urls import path
from .views import TweetsListCreate

app_name = 'tweets'

urlpatterns = [
    path('', TweetsListCreate.as_view(), name='create'),
]