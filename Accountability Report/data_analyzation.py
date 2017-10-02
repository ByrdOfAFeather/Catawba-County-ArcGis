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

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.5, random_state=225)

X_train.SchoolNamePublicSchool201415 = X_plot_encoder.fit_transform(X_train.SchoolNamePublicSchool201415)
school_encoded_train = X_train.SchoolNamePublicSchool201415.astype(int)
X_train = removesection(X_train, ['SchoolNamePublicSchool201415'])
X_train = PolynomialFeatures(degree=4).fit_transform(X_train)
ka = StandardScaler().fit(X_train)
X_train = ka.transform(X_train)

ma = Ridge()


ma.fit(X_train, y_train)

fig = plt.figure()
ax = fig.add_subplot(111)
plt.scatter(school_encoded_train, y_train)
plt.scatter(school_encoded_train, ma.predict(X_train))
props = dict(boxstyle='round', facecolor='white', alpha=.5)
ax.text(0.01, 0.026, 'Score = {}'.format(ma.score(X_train, y_train)), transform=ax.transAxes, verticalalignment='top', bbox=props)
	
plt.show()

X_test.SchoolNamePublicSchool201415 = X_plot_encoder.fit_transform(X_test.SchoolNamePublicSchool201415)
school_encoded_test = X_test.SchoolNamePublicSchool201415
X_test = removesection(X_test, ['SchoolNamePublicSchool201415',])
X_test = PolynomialFeatures(degree=4).fit_transform(X_test)
X_test = ka.transform(X_test)

fig = plt.figure()
ax = fig.add_subplot(111)
plt.scatter(school_encoded_test, y_test)
plt.scatter(school_encoded_test, ma.predict(X_test))
props = dict(boxstyle='round', facecolor='white', alpha=.5)
ax.text(0.01, 0.026, 'Score = {}'.format(ma.score(X_test, y_test)), transform=ax.transAxes, verticalalignment='top', bbox=props)
plt.show()

cross_validation = cross_val_score(ma, X_test, y_test, cv=10)
secondary_validation = cross_val_score(ma, X_train, y_train, cv=10)
print("Accuracy: {} (+/- {})" .format(cross_validation.mean(), cross_validation.std() * 2))
print("Accuracy: {} (+/- {})" .format(secondary_validation.mean(), secondary_validation.std() * 2))




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
