from Connections.prices import build_df
from Connections.forex import pull
from Connections.data import companies, exchanges, forex, adr
from Wrangling.preprocessing import processing
from Wrangling.conversion import convert
from Wrangling.dates import add_date

def main(exchanges, companies):
    df = build_df(exchanges, companies)
    processing(df, adr)
    rates = pull(forex)
    converted_df = convert(forex, rates, df)
    date_df = add_date(converted_df)
    print(date_df)

if __name__ == "__main__":
    main(exchanges, companies)