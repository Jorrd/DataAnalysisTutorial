# https://www.youtube.com/watch?v=uLqmM6ExPvo

import quandl
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from statistics import mean
style.use('fivethirtyeight')

def create_labels(cur_hpi, fut_hpi):
	if fut_hpi > cur_hpi:
		return 1
	else:
		return 0

# This is very pointless but we're just showing that a custom function can be used
def moving_average(values):
	return mean(values)


housing_data = pd.read_pickle('HPI.pickle')

housing_data = housing_data.pct_change()
housing_data.replace([np.inf, -np.inf], np.nan, inplace=True)
housing_data['US_HPI_future'] = housing_data['Bench'].shift(-1)
housing_data.dropna(inplace=True)

# print(housing_data[['US_HPI_future','Bench']].head())

housing_data['Label'] = list(map(create_labels, housing_data['Bench'], housing_data['US_HPI_future']))

print(housing_data['Label'])

housing_data['ma_apply_example'] = pd.rolling_apply(housing_data['M30'], 10, moving_average)

print(housing_data.tail())
