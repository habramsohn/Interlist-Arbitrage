import yfinance as yf
import pandas as pd
import math


def get_info(company):
    # Pulled from Yahoo Finance
    info = yf.Lookup(query=company).stock
    info = info[["exchange","regularMarketPrice"]].drop_duplicates("exchange")
    info = {i[0]:i[1] for i in info.itertuples(index=False)}
    return info
    

def pull_prices(exchanges, info, company):
    n = range(len(exchanges))
    prices = [info.get(exchanges[i],math.nan) for i in n]
    return prices


def build_df(exchanges, companies):
    rows = []
    for company in companies:
        info = get_info(company)
        prices = pull_prices(exchanges, info, company)
        rows.append(prices)
    df = pd.DataFrame(index=companies, columns=exchanges, data=rows)
    return df