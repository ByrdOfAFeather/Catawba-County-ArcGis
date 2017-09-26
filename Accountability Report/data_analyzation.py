# -*- coding: utf-8 -*-

from data_transformation_functions import merge_dicts, build_school_dict, build_grade_dict, build_grade_dataframe, setup_dicts, setup_NC_DATAFRAME, removesection
import plot_functions as custplt
import matplotlib.pyplot as plt
import numpy as np 
from sklearn import svm
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import Ridge
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import shapefile
from descartes import PolygonPatch


overall_dataframe = setup_dicts()[0]
overall_grades = setup_dicts()[1]

NC_database = setup_NC_DATAFRAME(overall_grades, overall_dataframe)
y = NC_database.Biology.astype(float).values
X = removesection(NC_database, ['Biology', 'Math', 'English', 'StateNamePublicSchoolLatestavailableyear', 'LocationAddress1PublicSchool201415', 
	'LocationCityPublicSchool201415', 'LocationZIPPublicSchool201415', 'TitleISchoolStatusPublicSchool201415', 'LowestGradeOfferedPublicSchool201415', 
	'HighestGradeOfferedPublicSchool201415', 'District', 'Grades912StudentsPublicSchool201415'])
X_plot_encoder = LabelEncoder()
X.SchoolNamePublicSchool201415 = X_plot_encoder.fit_transform(X.SchoolNamePublicSchool201415)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8, random_state=225)

print(y_train)
print(y_train.shape)
k = Ridge(alpha=1)
s = PolynomialFeatures(2).fit(X_train)
k.fit(s, y_train)
print(k.score(s, y_train))
print(k.coef_)
plt.scatter(X_train.SchoolNamePublicSchool201415.astype(float), y_train)
plt.plot(X_train.SchoolNamePublicSchool201415, k.predict(s))
plt.show()






### DATABASE SEPERATIONS ###
# CORR_database = NC_database
# CORR_database = CORR_database.drop(CORR_database[CORR_database['MagnetSchoolPublicSchool201415'] == 999].index)
# CORR_database = CORR_database.drop(CORR_database[CORR_database['CharterSchoolPublicSchool201415'] == 999].index)
# CORR_database = CORR_database.drop(CORR_database[CORR_database['TitleIEligibleSchoolPublicSchool201415'] == 999].index)
# CORR_database = CORR_database.drop(CORR_database[CORR_database['Grades912StudentsPublicSchool201415'] == 999999].index)
# CORR_database['StudentTeacherRatio'] = pd.to_numeric(CORR_database['StudentTeacherRatio'])
# CORR_database['LatitudePublicSchool201415'] = pd.to_numeric(CORR_database['LatitudePublicSchool201415'])
# CORR_database['LongitudePublicSchool201415'] = pd.to_numeric(CORR_database['LongitudePublicSchool201415'])
# corr_matrix = CORR_database.corr()
# print(corr_matrix)
