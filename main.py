from API.Connections.prices import build_df
from API.Connections.forex import pull
from API.Wrangling.preprocessing import processing
from API.Wrangling.conversion import convert
from API.Wrangling.dates import add_date
from data import companies, exchanges, forex, adr
from sql import insert_data
from datetime import datetime

def time_check():
    hour = datetime.now().hour
    if hour < 9 or hour > 16:
        return True
    else: return False

def data(exchanges, companies):
    init = build_df(exchanges, companies)
    processing(init, adr)
    rates = pull(forex)
    calculated_df = convert(forex, rates, init)
    df = add_date(calculated_df)   
    return df

if __name__ == "__main__":
    if time_check():
       exit()
    
    df = data(exchanges, companies)  
    insert_data(df)