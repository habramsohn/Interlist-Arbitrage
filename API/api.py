from Connections.prices import build_df
from Connections.forex import pull
from Connections.data import companies, exchanges, forex, adr
from Wrangling.preprocessing import processing
from Wrangling.conversion import convert
from Wrangling.dates import add_date
from timeit import default_timer as timer

def main(exchanges, companies):
    start = timer()
    df = build_df(exchanges, companies)
    processing(df, adr)
    rates = pull(forex)
    converted_df = convert(forex, rates, df)
    date_df = add_date(converted_df)
    end = timer()
    print(date_df)
    print(end - start)

if __name__ == "__main__":
    main(exchanges, companies)