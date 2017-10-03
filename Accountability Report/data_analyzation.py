# -*- coding: utf-8 -*-

from data_transformation_functions import merge_dicts, build_school_dict, build_grade_dict, build_grade_dataframe, setup_dicts, setup_NC_DATAFRAME, removesection
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


overall_dataframe = setup_dicts()[0]
overall_grades = setup_dicts()[1]

NC_database = setup_NC_DATAFRAME(overall_grades, overall_dataframe)
params = dict(NC_database=NC_database, degree=6, alpha=6500, file_name='Polynomial Regression With Degree 6 and Alpha 1500', location='Graphs/Machine Learning/Polynomial Regression', yaxis='Math Percent Passing', xaxis='School Encoded Value', title='Schools plotted against Math Percent Passing with Polynomial Estimators')
results = omega.NC_Database_Polynomial_Regressor(**params)
print(results)