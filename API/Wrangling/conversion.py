def match_rates(forex, rates):
    exch = list(forex.keys())
    curr = list(forex.values())
    n = range(len(exch))
    applications = {exch[i]: rates.get(curr[i], None) for i in n}
    return applications, exch


def apply(df, applications): 
    for col in df:
        denominator = applications.get(col, 1)
        df[col] = df[col] / denominator  
    return df  
        

def calculate(df, exch):
    df['int_mean'] = df.drop(columns=['NYSE']).mean(axis=1, skipna=True)
    df['perc_diff'] = ((df["NYSE"] - df["int_mean"]) / df.mean(axis=1, skipna=True)) * 100
    return df

    
def convert(forex, rates, df):
    applications, exch = match_rates(forex, rates)
    converted_df = apply(df, applications)
    calculated_df = calculate(converted_df, exch)
    return calculated_df