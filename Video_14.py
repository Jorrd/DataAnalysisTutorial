# https://www.youtube.com/watch?v=pxZy5jHID_A

import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')


def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fiddy_states[0][0][1:]

def grab_initial_state_data():
    states = state_list()

    main_df = pd.DataFrame()

    for abbv in states:
        query = "FMAC/HPI_"+str(abbv)
        df = quandl.get(query, authtoken="HsXsy_dUq9xsVwMgHEg4")
        df.rename(columns={'Value':str(abbv)}, inplace=True)
        #print(df[abbv].head())
        df[abbv] = (df[abbv] - df[abbv][0]) / df[abbv][0] * 100.0


        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    print(main_df.head())

    pickle_out = open('fiddy_states3.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()

def HPI_Benchmark():
    df = quandl.get("FMAC/HPI_USA", authtoken="HsXsy_dUq9xsVwMgHEg4")
    df["Value"] = (df["Value"] - df["Value"][0]) / df["Value"][0] * 100.0
    df.columns = ['Bench']
    return df

def mortgage_30y():
    df = quandl.get("FMAC/MORTG", trim_start="1975-01-01", authtoken="HsXsy_dUq9xsVwMgHEg4")
    df["Value"] = (df["Value"] - df["Value"][0]) / df["Value"][0] * 100.0
    df = df.resample('M').mean()
    df.columns = ['M30']
    return df

def sp500_data():
    df = quandl.get("YAHOO/INDEX_GSPC", trim_start="1975-01-01", authtoken="HsXsy_dUq9xsVwMgHEg4")
    df["Adjusted Close"] = (df["Adjusted Close"]-df["Adjusted Close"][0]) / df["Adjusted Close"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Adjusted Close':'sp500'}, inplace=True)
    df = df['sp500']
    return df

def gdp_data():
    df = quandl.get("BCB/4385", trim_start="1975-01-01", authtoken="HsXsy_dUq9xsVwMgHEg4")
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Value':'GDP'}, inplace=True)
    df = df['GDP']
    return df

def us_unemployment():
    df = quandl.get("ECPI/JOB_G", trim_start="1975-01-01", authtoken="HsXsy_dUq9xsVwMgHEg4")
    df["Unemployment Rate"] = (df["Unemployment Rate"]-df["Unemployment Rate"][0]) / df["Unemployment Rate"][0] * 100.0
    df=df.resample('1D').mean()
    df=df.resample('M').mean()
    return df


# sp500 = sp500_data()
US_GDP = gdp_data()
US_unemp = us_unemployment()
m30 = mortgage_30y()
HPI_data = pd.read_pickle('fiddy_states3.pickle')
HPI_bench = HPI_Benchmark()

HPI = HPI_data.join([HPI_bench, m30, US_unemp, US_GDP])
HPI.dropna(inplace=True)

print(HPI)
HPI.to_pickle('HPI.pickle')
# print(HPI.corr())

