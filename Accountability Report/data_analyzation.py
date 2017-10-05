# -*- coding: utf-8 -*-

from data_classes import NC_database
import plot_functions as custplt
import matplotlib.pyplot as plt
import numpy as np 
from sklearn import svm
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
from sklearn.dummy import DummyRegressor
from sklearn.model_selection import GridSearchCV
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import shapefile
from descartes import PolygonPatch
import machine_learning_functions as omega


# http://scikit-learn.org/stable/auto_examples/ensemble/plot_gradient_boosting_regression.html


params = dict(
	file_name='Polynomial Regression With Degree {} and Alpha {} & Title I school features',
 	location='Graphs/Machine Learning/Polynomial Regression', 
 	yaxis='English Percent Passing', 
 	xaxis='School Encoded Value', 
 	title='Schools plotted against English Percent Passing with Polynomial Estimators',
 	alpha=50000)

results = omega.NC_Database_Polynomial_Regressor(NC_database().regression_setup(target_value='English', degree=7), **params)
print(results)
