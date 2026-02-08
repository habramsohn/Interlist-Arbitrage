import numpy as np
import pandas as pd

def preprocess(df):
    # Combine NMS and NYQ for convenience
    df["NYSE"] = df["NYQ"].fillna(df["NMS"])
    df.drop(["NYQ","NMS"],axis=1,inplace=True)
    # Pence > Pound
    df["LSE"] = df["LSE"] * .01
    
    # Remove secondary/mismatched listings from irrelevant exchanges     
    rules = [
        (["SAP","BP"],"JPX"),
        (["Sony","ASML","Mitsubishi UFJ","SAP"],"LSE"),
        ("Toyota Motor",["LSE","PAR"])
    ]
    
    for rule in rules:
        df.loc[rule] = np.nan
    return df
    

def get_adr_calculations(df, adr):
    companies = list(df.index)
    n = range(len(companies))
    calculations = np.array([adr[companies[i]] if companies[i] in adr else 1 for i in n])
    return calculations


def apply_calculations(df, calculations):
    prices = np.array(df["NYSE"])
    new_prices = prices / calculations
    df["NYSE"] = new_prices


def processing(df, adr):
    df = preprocess(df)
    calculations = get_adr_calculations(df, adr)
    apply_calculations(df,calculations)