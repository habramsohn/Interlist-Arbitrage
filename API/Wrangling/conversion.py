def match_rates(forex, rates):
    exch = list(forex.keys())
    curr = list(forex.values())
    n = range(len(exch))
    applications = {exch[i]: rates.get(curr[i], None) for i in n}
    return applications


def apply(df, applications): 
    for col in df:
        denominator = applications.get(col, 1)
        df[col] = df[col] / denominator  
    return df  
        
    
def convert(forex, rates, df):
    applications = match_rates(forex, rates)
    converted_df = apply(df, applications)
    converted_df['int_mean'] = df.drop(columns=['NYSE']).mean(axis=1, skipna=True)
    return converted_df