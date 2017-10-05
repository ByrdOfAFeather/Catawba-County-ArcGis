# -*- coding: utf-8 -*-

from data_transformation_functions import merge_dicts, build_school_dict, build_grade_dict, build_grade_dataframe, setup_dicts, removesection
import matplotlib.pyplot as plt
import numpy as np 
from sklearn import svm
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
from sklearn.dummy import DummyRegressor
from sklearn.model_selection import GridSearchCV
import pandas as pd
import matplotlib.pyplot as plt 

def NC_Database_gradient_booster_regressor(**kwargs): pass


def NC_Database_Polynomial_Regressor(nc_data, **kwargs):
	'''Required Parameters in Kwargs: 
	degree -> int
	NC_database -> dataframe containing data (Probably NC data)
	alpha -> int
	'''
	X = nc_data[0]
	y = nc_data[1]
	X_train = nc_data[2]
	school_encoded_train = nc_data[3]
	y_train = nc_data[4]
	X_test = nc_data[5]
	school_encoded_test = nc_data[6]
	y_test = nc_data[7]

	ma = Ridge(alpha=kwargs['alpha'])
	ma.fit(X_train, y_train)

	alphas = np.array([i for i in range(150000, 200000, 1000)])
	grid = GridSearchCV(estimator=ma, param_grid=dict(alpha=alphas))
	grid.fit(X, y)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.scatter(school_encoded_train, y_train)
	plt.scatter(school_encoded_train, ma.predict(X_train))
	props = dict(boxstyle='round', facecolor='white', alpha=.5)
	ax.text(0.01, 0.026, 'Score = {}'.format(ma.score(X_train, y_train)), transform=ax.transAxes, verticalalignment='top', bbox=props)
	plt.title(kwargs['title'])
	plt.xlabel(kwargs['xaxis'])
	plt.ylabel(kwargs['yaxis'])
	if kwargs['file_name']:
		if kwargs['location']:
			plt.savefig('{}/{} Train'.format(kwargs['location'], kwargs['file_name']) + '.png')
		else:
			plt.savefig('Graphs/{}'.format(kwargs['file_name']) + '.png')
			
	mng = plt.get_current_fig_manager()
	mng.resize(*mng.window.maxsize())
	cross_validation = cross_val_score(ma, X_train, y_train)
	plt.show()
	
	# fig = plt.figure()
	# ax = fig.add_subplot(111)
	# plt.scatter(school_encoded_test, y_test)
	# plt.scatter(school_encoded_test, ma.predict(X_test))
	# props = dict(boxstyle='round', facecolor='white', alpha=.5)
	# ax.text(0.01, 0.026, 'Score = {}'.format(ma.score(X_test, y_test)), transform=ax.transAxes, verticalalignment='top', bbox=props)
	
	# if kwargs['file_name']:
	# 	if kwargs['location']:
	# 		plt.savefig('{}/{} Test'.format(kwargs['location'], kwargs['file_name']) + '.png')
	# 	else:
	# 		plt.savefig('Graphs/{}'.format(kwargs['file_name']) + '.png')
	
	# mng = plt.get_current_fig_manager()
	# mng.resize(*mng.window.maxsize())
	
	# plt.show()

	return {'cross_val_mean_train': cross_validation.mean(), 'cross_val_error_train': cross_validation.std() * 2, 'grid_best_score': grid.best_score_, 'grid_best_estimator': grid.grid_best_estimator_.alpha}