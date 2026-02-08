from datetime import datetime

def add_date(df):
    date = datetime.now()
    df['DateTime'] = date
    return df