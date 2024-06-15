import requests
import redis

from django.conf import settings


redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])
CACHE_TIME_LIMIT = 300


def get_exchange_rate(from_currency, to_currency):
    cache_key = f'exchange_rate:{from_currency}_{to_currency}'
    cached_rate = redis_client.get(cache_key)
    if cached_rate:
        return float(cached_rate)

    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()
    rate = data['rates'].get(to_currency)
    if rate:
        redis_client.setex(cache_key, CACHE_TIME_LIMIT, rate)
        return rate
    else:
        raise ValueError("Invalid currency code")
