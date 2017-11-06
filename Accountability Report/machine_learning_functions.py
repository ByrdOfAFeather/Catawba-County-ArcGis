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

def plot_data(predictions, x_values, y_values, title, 
	y, x, score, cross_val_score, file_name, location,
	test=False):
	
	fig = plt.figure(figsize=(16, 9)) 
	ax = fig.add_subplot(111) 

	plt.scatter(x_values, y_values, color='r') 
	plt.scatter(x_values, predictions, color='b') 
	plt.title(title)
	plt.ylabel(y)
	plt.xlabel(x)

	props = dict(boxstyle='round', facecolor='white', alpha=.5) 
	ax.text(0.01, 0.026, 'Score = {}'.format(score), transform=ax.transAxes, verticalalignment='top', bbox=props) 
	props = dict(boxstyle='round', facecolor='white', alpha=.5)
	ax.text(0.01, .974, 
		'Cross Validation Score = {}, Cross Validation Error = {}'.format(
			cross_val_score.mean(),
			 cross_val_score.std() * 2
			 ),  
		transform=ax.transAxes, verticalalignment='top', bbox=props)
	if file_name: 
		if location: 
			if test: plt.savefig('{}/{} Test'.format(location, file_name) + '.png') 
			else: plt.savefig('{}/{} Train'.format(location, file_name) + '.png') 
		else: 
			if test: plt.savefig('Graphs/{} Test'.format(file_name) + '.png') 
			else: plt.savefig('Graphs/{} Train'.format(file_name) + '.png') 
	plt.show() 


def nc_database_gradient_booster_regressor(nc_data, **kwargs): 
	''' Returns graphs based onthe nc_database and a gradient booster machine  
	nc_data - nc database 
	**kwargs: 
	REQUIRED - Title - String , xaxis - String, yaxis - String  
	OPTIONAL - file_name - String, location - String''' 

	X = nc_data[0] 
	y = nc_data[1] 
	X_train = nc_data[2] 
	school_encoded_train = nc_data[3] 
	y_train = nc_data[4] 
	X_test = nc_data[5] 
	school_encoded_test = nc_data[6] 
	y_test = nc_data[7] 

	model = GradientBoostingClassifier(learning_rate=kwargs['learning_rate'], n_estimators=kwargs['n_estimators'], max_depth=kwargs['max_depth']) 
	model.fit(X_train, y_train) 
	cross_score= cross_val_score(model, X, y, cv=4) 

	plot_data(model.predict(X_train), school_encoded_train, y_train, kwargs['title'], 
		kwargs['xaxis'], kwargs['yaxis'], 
		model.score(X_train, y_train), 
		cross_score, kwargs['file_name'], 
		kwargs['location'])	 

	plot_data(model.predict(X_test), school_encoded_test, y_test, kwargs['title'], 
		kwargs['xaxis'], kwargs['yaxis'], 
		model.score(X_test, y_test), 
		cross_score, kwargs['file_name'],
		kwargs['location'], test=True)	 

	return cross_score


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
	if classification: 
		model = MLPClassifier(hidden_layer_sizes=(690,)) 
	else: 
		model = MLPRegressor() 

	model.fit(X_train, y_train) 

	# Graphs Cross Validation and Score
	cross_score = cross_val_score(model, X, y, cv=4) 
	
	plot_data(model.predict(X_train), school_encoded_train, y_train, kwargs['title'], 
		kwargs['xaxis'], kwargs['yaxis'], 
		model.score(X_train, y_train), 
		cross_score, kwargs['file_name'],
		kwargs['location'])

	plot_data(model.predict(X_test), school_encoded_test, y_test, kwargs['title'], 
		kwargs['xaxis'], kwargs['yaxis'], 
		model.score(X_test, y_test), 
		cross_score, kwargs['file_name'],
		kwargs['location'], test=True)

	return cross_score 


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

	model = Ridge(alpha=kwargs['alpha']) 
	model.fit(X_train, y_train)

	cross_score = cross_val_score(model, X, y)

	plot_data(model.predict(X_train), school_encoded_train, y_train, kwargs['title'], 
		kwargs['xaxis'], kwargs['yaxis'], 
		model.score(X_train, y_train), 
		cross_score, kwargs['file_name'],
		kwargs['location'])
 
	plot_data(model.predict(X_test), school_encoded_train, y_test, kwargs['title'], 
		kwargs['xaxis'], kwargs['yaxis'], 
		model.score(X_test, y_test), 
		cross_score, kwargs['file_name'],
		kwargs['location'], test=True)

	return {'cross_val_mean_train': cross_validation.mean(), 'cross_val_error_train': cross_validation.std() * 2} 