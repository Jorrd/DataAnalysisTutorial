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
    #df.rename(columns={'Value':"United States (NSA)"}, inplace=True)
    return df

#grab_initial_state_data()

fig = plt.figure()
ax1 = plt.subplot2grid((1,1),(0,0))


HPI_data = pd.read_pickle('fiddy_states3.pickle')

TX1yr = HPI_data['TX'].resample('A', how='ohlc')
print(TX1yr.head())

HPI_data['TX'].plot(ax = ax1, label='Monthly TX HPI')
TX1yr.plot(ax = ax1, label='Yearly TX HPI')


plt.legend(loc=4)
plt.show()
