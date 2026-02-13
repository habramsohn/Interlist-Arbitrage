import pandas as pd
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
import os 
from dotenv import load_dotenv

load_dotenv(override=True)

DB_INSTANCE = os.getenv("DB_INSTANCE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_NAME = os.getenv("DB_NAME")

connector = Connector()

def getconn():
    connection = connector.connect(
        DB_INSTANCE,
        "pymysql",
        user=DB_USERNAME,
        db="tickerstorage")
    return connection

def insert_data(df):
    engine = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn)
    with engine.connect() as conn:  
        df.to_sql(DB_NAME, con=conn, if_exists="append", index=False)