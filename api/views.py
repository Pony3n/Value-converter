from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import ConversionSerializer
from .services import get_exchange_rate


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
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=ConversionSerializer,
        responses={200: 'Conversion successful', 400: 'Bad request'}
    )
    def post(self, request):
        serializer = ConversionSerializer(data=request.data)
        if serializer.is_valid():
            from_currency = serializer.validated_data['from']
            to_currency = serializer.validated_data['to']
            value = serializer.validated_data['value']

            try:
                rate = get_exchange_rate(from_currency, to_currency)
                result = value * rate
                return Response({'result': result}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)