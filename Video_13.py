# https://www.youtube.com/watch?v=FvamL5oA_EE&list=PLQVvvaa0QuDc-3szzjeP6N6b0aDrrKyL-&index=13

import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

def mortgage_30y():
	df = quandl.get("FMAC/MORTG", trim_start="1975-01-01", authtoken="HsXsy_dUq9xsVwMgHEg4")
	df["Value"] = (df["Value"] - df["Value"][0]) / df["Value"][0] * 100.0
	df = df.resample('M').mean()
	df.columns = ['M30']
	return df


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
    return df

m30 = mortgage_30y()
HPI_data = pd.read_pickle('fiddy_states3.pickle')
HPI_bench = HPI_Benchmark()

state_HPI_M30 = HPI_data.join(m30)

print(state_HPI_M30.corr()['M30'].describe())


#print(HPI_data.head())

