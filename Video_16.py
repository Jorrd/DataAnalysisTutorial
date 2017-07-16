# https://www.youtube.com/watch?v=t4319ffzRg0

import quandl
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from statistics import mean
from sklearn import svm, preprocessing, cross_validation

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

print(housing_data.head())

x = np.array(housing_data.drop(['Label', 'US_HPI_future'], 1))
x = preprocessing.scale(x)

y = np.array(housing_data['Label'])

x_train, x_test, y_train, y_test = cross_validation.train_test_split(x, y, test_size=0.2)

clf = svm.SVC(kernel='linear')
clf.fit(x_train, y_train)

print(clf.score(x_test, y_test))
