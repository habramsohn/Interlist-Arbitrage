from API.Connections.prices import build_df
from API.Connections.forex import pull
from API.Wrangling.preprocessing import processing
from API.Wrangling.conversion import convert
from API.Wrangling.dates import add_date
from data import companies, exchanges, forex, adr
from sql import insert_data
from datetime import datetime
from datetime import date

# Run when NYSE is open 
def time_check():
    hour = datetime.now().hour
    hourrange = range(9,17)
    day = date.today().weekday()
    dayrange = range(1,6)
    minute = datetime.now().minute
    open_hours = (range(9,17),range(1,6))
    
    if hour == 9 and minute < 30:
        minute = False
    if minute and hour in hourrange and day in dayrange:
        return False 
    else: 
        return True

def data(exchanges, companies):
    init = build_df(exchanges, companies)
    processing(init, adr)
    rates = pull(forex)
    calculated_df = convert(forex, rates, init)
    df = add_date(calculated_df)   
    df.reset_index(inplace=True)
    return df

if __name__ == "__main__":
    if time_check():
        exit()
    df = data(exchanges, companies)
    insert_data(df)