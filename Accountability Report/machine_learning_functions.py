# -*- coding: utf-8 -*-

from data_transformation_functions import merge_dicts, build_school_dict, build_grade_dict, build_grade_dataframe, setup_dicts, removesection
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from sklearn import svm
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import Ridge
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingClassifier 

def nc_database_gradient_booster_regressor(nc_data, **kwargs):
	''' Returns graphs based onthe nc_database and a gradient booster machine 
	nc_data - nc database
	**kwargs:
	REQUIRED - Title - String , xaxis - String, yaxis - String 
	OPTIONAL - file_name - String, location - String'''

	fig = plt.figure(figsize=(16, 9))
	ax = fig.add_subplot(111)

	X = nc_data[0]
	y = nc_data[1]
	X_train = nc_data[2]
	school_encoded_train = nc_data[3]
	y_train = nc_data[4]
	X_test = nc_data[5]
	school_encoded_test = nc_data[6]
	y_test = nc_data[7]

	nemisis_k = GradientBoostingClassifier(learning_rate=kwargs['learning_rate'], n_estimators=kwargs['n_estimators'], max_depth=kwargs['max_depth'])
	nemisis_k.fit(X_train, y_train)

	plt.scatter(school_encoded_train, y_train, color='r')
	plt.scatter(school_encoded_train, nemisis_k.predict(X_train), color='b')

	plt.title(kwargs['title'])
	plt.xlabel(kwargs['xaxis'])
	plt.ylabel(kwargs['yaxis'])
	
	props = dict(boxstyle='round', facecolor='white', alpha=.5)
	ax.text(0.01, 0.026, 'Score = {}'.format(nemisis_k.score(X_train, y_train)), transform=ax.transAxes, verticalalignment='top', bbox=props)

	if kwargs['file_name']:
		if kwargs['location']:
			plt.savefig('{}/{} Train'.format(kwargs['location'], kwargs['file_name']) + '.png')
		else:
			plt.savefig('Graphs/{}'.format(kwargs['file_name']) + '.png')
	
	plt.show()

	fig = plt.figure(figsize=(16, 9))
	ax = fig.add_subplot(111)

	plt.scatter(school_encoded_test, y_test, color='g')
	plt.scatter(school_encoded_test, nemisis_k.predict(X_test), color='y')

	props = dict(boxstyle='round', facecolor='white', alpha=.5)
	ax.text(0.01, 0.026, 'Score = {}'.format(nemisis_k.score(X_test, y_test)), transform=ax.transAxes, verticalalignment='top', bbox=props)
	
	plt.title(kwargs['title'])
	plt.xlabel(kwargs['xaxis'])
	plt.ylabel(kwargs['yaxis'])
	
	if kwargs['file_name']:
		if kwargs['location']:
			plt.savefig('{}/{} Test'.format(kwargs['location'], kwargs['file_name']) + '.png')
		else:
			plt.savefig('Graphs/{}'.format(kwargs['file_name']) + '.png')

	plt.show()

	cross_validation = cross_val_score(nemisis_k, X, y)
	return cross_validation


def nc_database_nerual_network(nc_data, classification=None, **kwargs):
	'''Nerual Network model for nc database'''
	X = nc_data[0]
	y = nc_data[1]
	X_train = nc_data[2]
	school_encoded_train = nc_data[3]
	y_train = nc_data[4]
	X_test = nc_data[5]
	school_encoded_test = nc_data[6]
	y_test = nc_data[7]

	fig = plt.figure(figsize=(16, 9))
	ax = fig.add_subplot(111)
	if classification:
		ultra_k = MLPClassifier(hidden_layer_sizes=(100000,), alpha=1)
	else:
		ultra_k = MLPRegressor(hidden_layer_sizes=(100000,), alpha=5000)

	ultra_k.fit(X_train, y_train)

	plt.scatter(school_encoded_train, y_train)
	plt.scatter(school_encoded_train, ultra_k.predict(X_train))


	props = dict(boxstyle='round', facecolor='white', alpha=.5)
	ax.text(0.01, 0.026, 'Score = {}'.format(ultra_k.score(X_train, y_train)), transform=ax.transAxes, verticalalignment='top', bbox=props)


	plt.show()

	fig = plt.figure(figsize=(16, 9))
	ax = fig.add_subplot(111)

	plt.scatter(school_encoded_test, y_test)
	plt.scatter(school_encoded_test, ultra_k.predict(X_test))


	props = dict(boxstyle='round', facecolor='white', alpha=.5)
	ax.text(0.01, 0.026, 'Score = {}'.format(ultra_k.score(X_test, y_test)), transform=ax.transAxes, verticalalignment='top', bbox=props)

	plt.show()
	cross_validation = cross_val_score(ultra_k, X, y, cv=9)
	return cross_validation

def nc_database_polynomial_regressor(nc_data, **kwargs):
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

	fig = plt.figure(figsize=(16, 9))
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

	cross_validation = cross_val_score(ma, X, y)
	plt.show()
	
	fig = plt.figure(figsize=(16, 9))
	ax = fig.add_subplot(111)

	plt.scatter(school_encoded_test, y_test)
	plt.scatter(school_encoded_test, ma.predict(X_test))

	props = dict(boxstyle='round', facecolor='white', alpha=.5)
	ax.text(0.01, 0.026, 'Score = {}'.format(ma.score(X_test, y_test)), transform=ax.transAxes, verticalalignment='top', bbox=props)

	plt.title(kwargs['title'])
	plt.xlabel(kwargs['xaxis'])
	plt.ylabel(kwargs['yaxis'])

	
	if kwargs['file_name']:
		if kwargs['location']:
			plt.savefig('{}/{} Test'.format(kwargs['location'], kwargs['file_name']) + '.png')
		else:
			plt.savefig('Graphs/{}'.format(kwargs['file_name']) + '.png')
	
	plt.show()



	return {'cross_val_mean_train': cross_validation.mean(), 'cross_val_error_train': cross_validation.std() * 2}