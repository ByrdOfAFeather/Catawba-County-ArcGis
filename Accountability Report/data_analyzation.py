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

# http://scikit-learn.org/stable/auto_examples/ensemble/plot_gradient_boosting_regression.html
params = dict(
	file_name='Polynomial Regression With Degree {} and Alpha {} & Title I school features',
 	location='Graphs/Machine Learning/Polynomial Regression', 
 	yaxis='English Percent Passing', 
 	xaxis='School Encoded Value', 
 	title='Schools plotted against English Percent Passing with Polynomial Estimators',
 	alpha=199000)

classification_params = dict(
	learning_rate=1,
	n_estimators=100,
	max_depth=3)

polynomial_results = omega.nc_database_polynomial_regressor(
	NC_database().regression_setup(target_subject='English', degree=7), **params)
gradient_boosting = omega.nc_database_gradient_booster_regressor(
	NC_database().classification_setup(target_subject='Biology', score_threshold=60), **classification_params) 

print(polynomial_results)
print(gradient_boosting.mean(), gradient_boosting.std() * 2)