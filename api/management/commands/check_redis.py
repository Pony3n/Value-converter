import redis
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Check Redis connection'

    def handle(self, *args, **kwargs):
        redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])

        try:
            redis_client.set('test_key', 'test_value')
            value = redis_client.get('test_key').decode('utf-8')
            self.stdout.write(self.style.SUCCESS(f'Successfully connected to Redis! Value: {value}'))
        except redis.ConnectionError as e:
            self.stdout.write(self.style.ERROR(f'Failed to connect to Redis: {e}'))
