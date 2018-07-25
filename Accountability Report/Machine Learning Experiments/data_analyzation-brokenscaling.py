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
columns = []

X_plot_encoder = LabelEncoder()

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.5, random_state=225)

X_train.SchoolNamePublicSchool201415 = X_plot_encoder.fit_transform(X_train.SchoolNamePublicSchool201415)
schoolname = X_train.SchoolNamePublicSchool201415.values.astype(float)
X_train = removesection(X_train, ['SchoolNamePublicSchool201415',])
X_train = X_train.as_matrix()
ait = StandardScaler().fit_transform(X_train)
X_train = ait

def polynomial_regression_function(degree, alpha, x, y, plot_title='Default', x_lbl='Default', y_lbl='Default', file_name='', location=''):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	k = Ridge(alpha=alpha, fit_intercept=False)
	s = PolynomialFeatures(degree=degree).fit_transform(X_train)
	
	k.fit(s, y_train)
	plt.xlabel(x_lbl)
	plt.ylabel(y_lbl)
	plt.title(plot_title)
	plt.scatter(schoolname, y_train)
	plt.scatter(schoolname, k.predict(s), color='r')
	
	props = dict(boxstyle='round', facecolor='white', alpha=.5)
	ax.text(0.01, 0.026, 'Score = {}'.format(k.score(s, y)), transform=ax.transAxes, verticalalignment='top', bbox=props)
	
	if file_name:
		if location:
			plt.savefig('Graphs/{}/{}'.format(location, file_name) + '.png')
		else:
			plt.savefig('Graphs/{}'.format(file_name) + '.png')
	plt.show()
	
	return {'score': k.score(s, y), 'model': k, 'polynomialx': s, 'degree':degree}


k_dict = polynomial_regression_function(1, 1, X_train, y_train, plot_title='Polynomial model with alpha=1 degree=5', x_lbl='School encoded (each increase in 1, represents a new school)', y_lbl='Biology Percent Passing')
model = k_dict['model']

X_test.SchoolNamePublicSchool201415 = X_plot_encoder.fit_transform(X_test.SchoolNamePublicSchool201415)
schoolname = X_test.SchoolNamePublicSchool201415.values.astype(float)
X_test = removesection(X_test, ['SchoolNamePublicSchool201415',])
for columns in X_test.columns.values:
	X_test[columns] = X_test[columns].apply(pd.to_numeric)
X_test = X_test.as_matrix()
ait = StandardScaler().fit_transform(X_test)
X_test = PolynomialFeatures(degree=k_dict['degree']).fit_transform(X_test)

plt.scatter(schoolname, y_test)
plt.scatter(schoolname, model.predict(X_test), color='r')
dummy = DummyRegressor()
dummy.fit(X_test, y_test)
plt.plot(schoolname, dummy.predict(X_test), color='g')

plt.show()

cross_validation = cross_val_score(model, X_test, y_test)
print("Accuracy: {} (+/- {})" .format(cross_validation.mean(), cross_validation.std() * 2))
print('Dummy: {}'.format(dummy.score(X_test, y_test)))



### DATABASE SEPERATIONS ###
# CORR_database = NCDatabase
# CORR_database = CORR_database.drop(CORR_database[CORR_database['MagnetSchoolPublicSchool201415'] == 999].index)
# CORR_database = CORR_database.drop(CORR_database[CORR_database['CharterSchoolPublicSchool201415'] == 999].index)
# CORR_database = CORR_database.drop(CORR_database[CORR_database['TitleIEligibleSchoolPublicSchool201415'] == 999].index)
# CORR_database = CORR_database.drop(CORR_database[CORR_database['Grades912StudentsPublicSchool201415'] == 999999].index)
# CORR_database['StudentTeacherRatio'] = pd.to_numeric(CORR_database['StudentTeacherRatio'])
# CORR_database['LatitudePublicSchool201415'] = pd.to_numeric(CORR_database['LatitudePublicSchool201415'])
# CORR_database['LongitudePublicSchool201415'] = pd.to_numeric(CORR_database['LongitudePublicSchool201415'])
# corr_matrix = CORR_database.corr()
# print(corr_matrix)
