from django.urls import path

from .views import ConvertCurrency
from .views import check_redis


urlpatterns = [
    path('api/rates/', ConvertCurrency.as_view(), name='convert-currency'),
    path('check_redis/', check_redis, name='check_redis')
]
