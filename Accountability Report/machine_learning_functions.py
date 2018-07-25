# -*- coding: utf-8 -*- 

import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingClassifier  


def plot_data(predictions, x_values, y_values, title,
              y, x, score, cross_val_score, file_name, location,
              test=False):
	"""
	Plots data with information and keys
	:param predictions: predictions from the neural network
	:param x_values: values to fill the x-axis
	:param y_values: actual values
	:param title: Title of the plot
	:param y: original data set y values
	:param x: original data set x values
	:param score: model score
	:param cross_val_score: model's cross validation score
	:param file_name: output file name
	:param location: output file location
	:param test: if it is test or train values
	"""

	# Sets up the pictures
	fig = plt.figure(figsize=(16, 9)) 
	ax = fig.add_subplot(111) 

	# Scatters the actual values and plots scatters prediction values
	plt.scatter(x_values, y_values, color='r') 
	plt.scatter(x_values, predictions, color='b') 
	plt.title(title)
	plt.ylabel(y)
	plt.xlabel(x)

	# Sets up the text describing the score of the model
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
	"""Returns graphs based on the nc_database and a gradient booster machine
	:param nc_data: nc database variable
	:param kwargs: REQUIRED - Title - String , xaxis - String, yaxis - String;
				   OPTIONAL - file_name - String, location - String
	"""
	# Gets the variables out of the setup for regression
	x = nc_data[0]
	y = nc_data[1] 
	x_train = nc_data[2]
	school_encoded_train = nc_data[3] 
	y_train = nc_data[4] 
	x_test = nc_data[5]
	school_encoded_test = nc_data[6] 
	y_test = nc_data[7] 

	# builds a model with specified params
	model = GradientBoostingClassifier(learning_rate=kwargs['learning_rate'], n_estimators=kwargs['n_estimators'],
	                                   max_depth=kwargs['max_depth'])
	model.fit(x_train, y_train)
	# Gets the cross_validation_score from the model
	cross_score = cross_val_score(model, x, y, cv=4)

	# Plots the data and saves the file
	plot_data(model.predict(x_train), school_encoded_train, y_train, kwargs['title'],
		kwargs['xaxis'], kwargs['yaxis'], 
		model.score(x_train, y_train),
		cross_score, kwargs['file_name'], 
		kwargs['location'])	 

	plot_data(model.predict(x_test), school_encoded_test, y_test, kwargs['title'],
		kwargs['xaxis'], kwargs['yaxis'], 
		model.score(x_test, y_test),
		cross_score, kwargs['file_name'],
		kwargs['location'], test=True)	 

	return cross_score


def nc_database_neural_network(nc_data, classification=None, **kwargs):
	"""Neural Network model for nc database
	:param nc_data: a nc database
	:param classification: if the neural network is to classify or regress
	:param kwargs: REQUIRED - Title - String , xaxis - String, yaxis - String;
				   OPTIONAL - file_name - String, location - String
	"""
	# Gets the variables out of the setup for regression
	x = nc_data[0]
	y = nc_data[1] 
	x_train = nc_data[2]
	school_encoded_train = nc_data[3] 
	y_train = nc_data[4] 
	x_test = nc_data[5]
	school_encoded_test = nc_data[6] 
	y_test = nc_data[7]

	# Sets up neural network based on pass values
	if classification: 
		model = MLPClassifier(hidden_layer_sizes=(690,)) 
	else: 
		model = MLPRegressor() 

	model.fit(x_train, y_train)

	# Graphs Cross Validation and Score
	cross_score = cross_val_score(model, x, y, cv=4)
	
	plot_data(model.predict(x_train), school_encoded_train, y_train, kwargs['title'],
		kwargs['xaxis'], kwargs['yaxis'], 
		model.score(x_train, y_train),
		cross_score, kwargs['file_name'],
		kwargs['location'])

	plot_data(model.predict(x_test), school_encoded_test, y_test, kwargs['title'],
		kwargs['xaxis'], kwargs['yaxis'], 
		model.score(x_test, y_test),
		cross_score, kwargs['file_name'],
		kwargs['location'], test=True)

	return cross_score 


def nc_database_polynomial_regressor(nc_data, **kwargs): 
	"""
	:param nc_data: nc_data variable

	Required Parameters in Kwargs:
	degree: integer value for degree of polynomial features
	alpha: Integer alpha term
	"""

	# Gets the variables out of the setup for regression
	x = nc_data[0]
	y = nc_data[1] 
	x_train = nc_data[2]
	school_encoded_train = nc_data[3] 
	y_train = nc_data[4] 
	x_test = nc_data[5]
	y_test = nc_data[7] 

	# sets up polynomial ridge regression model
	model = Ridge(alpha=kwargs['alpha'])
	model.fit(x_train, y_train)

	cross_score = cross_val_score(model, x, y)

	# Graphs Cross Validation and Score
	plot_data(model.predict(x_train), school_encoded_train, y_train, kwargs['title'],
		kwargs['xaxis'], kwargs['yaxis'], 
		model.score(x_train, y_train),
		cross_score, kwargs['file_name'],
		kwargs['location'])
 
	plot_data(model.predict(x_test), school_encoded_train, y_test, kwargs['title'],
		kwargs['xaxis'], kwargs['yaxis'], 
		model.score(x_test, y_test),
		cross_score, kwargs['file_name'],
		kwargs['location'], test=True)

	return {'cross_val_mean_train': cross_score.mean(), 'cross_val_error_train': cross_score.std() * 2}