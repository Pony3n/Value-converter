import requests


def get_exchange_rate(from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()
    rate = data['rates'].get(to_currency)
    if rate:
        return rate
    else:
        raise ValueError("Invalid currency code")
