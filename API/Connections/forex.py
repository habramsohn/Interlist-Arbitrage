import requests
from data import forex


def url(forex):
    currencies = ",".join(list(forex.values()))
    url = f"https://api.frankfurter.dev/v1/latest?base=USD&symbols={currencies}"
    return url


def pull(url):
    response = requests.get(url)
    return response, response.status_code
    

pull(url(forex))