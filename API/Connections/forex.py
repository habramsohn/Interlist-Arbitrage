import requests


def define_currencies(forex):
    currencies = ",".join(list(forex.values()))
    # Daily updates
    url = f"https://api.frankfurter.dev/v1/latest?base=USD&symbols={currencies}"
    return url


def pull(forex):
    url = define_currencies(forex)
    response = requests.get(url).json()
    rates = response["rates"]
    rates["USD"] = 1
    return rates