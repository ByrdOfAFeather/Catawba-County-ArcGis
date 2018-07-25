# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import shapefile
import machine_learning_functions as omega
from sklearn import svm
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
from sklearn.dummy import DummyRegressor
from sklearn.model_selection import GridSearchCV
from data_classes import NC_database
from pandas.tools.plotting import scatter_matrix
from mpl_toolkits.mplot3d import Axes3D
from web_scrapping import get_reduced_lunch

regression_params = dict(
	file_name='Polynomial Regression With Degree {} and Alpha {} & Title I school features',
 	location='Graphs/Machine Learning/Polynomial Regression', 
 	yaxis='English Percent Passing', 
 	xaxis='School Encoded Value', 
 	title='Schools plotted against English Percent Passing with Polynomial Estimators',
 	alpha=199000
 	)

classification_params = dict(
	learning_rate=1,
	n_estimators=900,
	max_depth=1,
	alpha=100,
	file_name='ENGLISH 2 CLASSES - 2nd test Gradient Machine With web scraping learning_rate 1 n_estimators 900 max_depth 1 alpha 100',
	location='Graphs/Machine Learning/Gradient Boosted Machine/',
	xaxis='0 - x < 60%, 1 - x >= 60%',
	yaxis='School Encoded Value',
	title='Gradient Boosting Machine classifying schools into score-based tiers'
	)

neural_network_classification_params = dict(
	file_name='ENGLISH 2 CLSSES - 2nd test Neural Network hidden_layer_size 690',
	location='Graphs/Machine Learning/Neural Network',
	xaxis='0 - x < 60%, 1 - x >= 60%',
	yaxis='School Encoded Value',
	title='Neural Network classifying schools into score-based tiers'
	)

database = NC_database().classification_setup(target_subject='English', score_threshold=60)

# Creates a model based on a gradient boosting machine
gradient_boosting = omega.nc_database_gradient_booster_regressor(
  	database,
	**classification_params
)

# Creates a model based on a regular feed-forward neural network trained for classification
neural_network_classification = omega.nc_database_nerual_network(
	database,
	classification=True,
	**neural_network_classification_params
)

# prints estimates of accuracy of models
print(gradient_boosting.mean(), gradient_boosting.std() * 2)
print(neural_network_classification.mean(), neural_network_classification.std() * 2)