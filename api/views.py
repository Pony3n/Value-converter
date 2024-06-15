import redis

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from django.conf import settings

from .serializers import ConversionSerializer
from .services import get_exchange_rate


CACHE_TIME_LIMIT = 10


class ConvertCurrency(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('from', openapi.IN_QUERY, description="From currency", type=openapi.TYPE_STRING),
            openapi.Parameter('to', openapi.IN_QUERY, description="To currency", type=openapi.TYPE_STRING),
            openapi.Parameter('value', openapi.IN_QUERY, description="Value to convert", type=openapi.TYPE_NUMBER)
        ],
        responses={200: openapi.Response('Success', ConversionSerializer)}
    )
    def get(self, request):
        data = {
            'from_currency': request.query_params.get('from'),
            'to_currency': request.query_params.get('to'),
            'value': request.query_params.get('value')
        }

        serializer = ConversionSerializer(data=data)
        if serializer.is_valid():
            from_currency = serializer.validated_data['from']
            to_currency = serializer.validated_data['to']
            value = serializer.validated_data['value']

            try:
                rate = get_exchange_rate(from_currency, to_currency)
                result = value * rate
                return Response({'result': result}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'error': f'Введите число {e}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_redis(request):
    """
    Функция для проверки подключения к Redis
    """
    try:
        redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])
        redis_client.set('test_key', 'test_value', CACHE_TIME_LIMIT,)
        value = redis_client.get('test_key').decode('utf-8')
        return Response({'status': 'success', 'value': value})
    except redis.ConnectionError as error:
        return Response({'status': 'error', 'message': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
