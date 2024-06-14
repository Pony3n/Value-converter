from rest_framework import serializers


class ConversionSerializer(serializers.Serializer):
    from_currency = serializers.CharField(max_length=3, source='from')
    to_currency = serializers.CharField(max_length=3, source='to')
    value = serializers.FloatField()
