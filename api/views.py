from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConversionSerializer
from .services import get_exchange_rate


class ConvertCurrency(APIView):
    """
    Представление, для отображения актуальной информации по валюте.
    """
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
