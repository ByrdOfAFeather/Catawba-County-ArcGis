# -*- coding: utf-8 -*-

import plot_functions as custplt
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
from descartes import PolygonPatch

regression_params = dict(
	file_name='Polynomial Regression With Degree {} and Alpha {} & Title I school features',
 	location='Graphs/Machine Learning/Polynomial Regression', 
 	yaxis='English Percent Passing', 
 	xaxis='School Encoded Value', 
 	title='Schools plotted against English Percent Passing with Polynomial Estimators',
 	alpha=199000)

classification_params = dict(
	learning_rate=1,
	n_estimators=950,
	max_depth=1,
	file_name='Gradient Boosted Machine max_depth 1 n_estimators 950 predictor = 2 classes - Biology',
	location='Graphs/Machine Learning/Gradient Boosted Machine',
	yaxis='0 - < 25%, 1 - 25% < x < 35%, 2 - 35% < x < 45%, 3 - 45% < x < 50%, 4 - 75% < x < 80%, 5 - 80% < x < 100%',
	xaxis='School Encoded Value',
	title='Gradient Boosting Machine classifying schools into score-based tiers')


# gradient_boosting = omega.nc_database_gradient_booster_regressor(
# 	NC_database().classification_setup(target_subject='Biology'), **classification_params) 

neural_network = omega.nc_database_nerual_network(
	NC_database().regression_setup(target_subject='Math', degree=6), **regression_params)




# print(gradient_boosting.mean(), gradient_boosting.std() * 2)