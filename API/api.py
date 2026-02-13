from .Connections.prices import build_df
from .Connections.forex import pull
from .Connections.data import companies, exchanges, forex, adr
from .Wrangling.preprocessing import processing
from .Wrangling.conversion import convert
from .Wrangling.dates import add_date

def main(exchanges, companies):
    init = build_df(exchanges, companies)
    processing(init, adr)
    rates = pull(forex)
    calculated_df = convert(forex, rates, init)
    df = add_date(calculated_df)   
    return df

if __name__ == "__main__":
    df = main(exchanges, companies)    
