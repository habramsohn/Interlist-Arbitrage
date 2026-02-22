import pandas as pd
from sqlalchemy import select, func, text, create_engine, MetaData, Table, Column, Float, DateTime, String
from sqlalchemy_utils import database_exists, create_database
import pymysql
import os 
from dotenv import load_dotenv
from data import exchanges

load_dotenv(override=True)

exchanges = [ex for ex in exchanges if ex not in ["NYQ","NMS"]]

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

port = "3306"

url = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@localhost:{port}/{DB_NAME}"

def check_existing(engine):
    if not database_exists(engine.url):
        create_database(engine.url)
    metadata = MetaData()
    columns = [Column(f'{ex}', Float) for ex in exchanges]
    table = Table(
        'tickerstorage',
        metadata,
        Column('index', String(30)),
        Column('id', Float, primary_key=True, autoincrement=True),
        *columns,
        Column("NYSE", Float),
        Column("int_mean", Float),
        Column("perc_diff", Float),
        Column("DateTime", DateTime)
    )
    metadata.create_all(engine)
        

def check_count(conn, added):
    nrows = conn.execute(text("SELECT COUNT(*) FROM tickerstorage")).scalar()
    if nrows >= 20000:
        conn.execute(f"""DELETE FROM tickerstorage
                        WHERE DateTime IN (
                            SELECT DateTime FROM (
                                SELECT DateTime FROM tickerstorage
                                ORDER BY DateTime ASC
                                LIMIT {added}
                            ) as tmp
                        )""")

def insert_data(df):
    engine = create_engine(url)
    check_existing(engine)
    with engine.connect() as conn:  
        added = df.to_sql("tickerstorage", con=conn, if_exists="append", index=False)
        check_count(conn, added)
        conn.commit()