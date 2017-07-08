import quandl
import pandas as pd

# df = quandl.get('FMAC/HPI_AK',authtoken="HsXsy_dUq9xsVwMgHEg4")
# print(df.head())

fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')

# This is a list of all of the dataframes on the webpage
#print(fiddy_states)

# This is the first dataframe on the webpage
#print(fiddy_states[0])

# This is the first column of the first dataframe on the webpage
#print(fiddy_states[0][0])

for abbv in fiddy_states[0][0][1:]:
    print("FMAC/HPI_"+str(abbv))

