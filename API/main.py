from Connections.prices import build_df
from Connections.forex import pull
from Connections.data import companies, exchanges, forex, adr
from Wrangling.preprocessing import processing
from Wrangling.conversion import convert
from Wrangling.dates import add_date

df = build_df(exchanges, companies)
calculated_df = processing(df, adr)
rates = pull(forex)
converted_df = convert(forex, rates, df)
date_df = add_date(converted_df)

print(date_df)