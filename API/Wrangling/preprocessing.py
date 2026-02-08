import numpy as np
import pandas as pd

def preprocess(df):
    # Combine NMS and NYQ for convenience
    df["NYSE"] = df["NYQ"].fillna(df["NMS"])
    df.drop(["NYQ","NMS"],axis=1,inplace=True)
    # Pence > Pound
    df["LSE"] = df["LSE"] * .01
    # Remove secondary/mismatched listings from irrelevant exchanges 
    df.loc["BP","JPX"] = np.nan
    df.loc[["Sony","ASML"],"LSE"] = np.nan
    df.loc["Mitsubishi UFJ","LSE"] = np.nan
    df.loc["SAP","LSE"] = np.nan
    # Update JPX SAP
    df.loc["SAP", "JPX"] = df.loc["SAP", "JPX"] * 16
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