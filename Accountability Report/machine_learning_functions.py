# -*- coding: utf-8 -*-

from data_transformation_functions import merge_dicts, build_school_dict, build_grade_dict, build_grade_dataframe, setup_dicts, setup_NC_DATAFRAME, removesection
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
import matplotlib.pyplot as plt 

def NC_Database_gradient_booster_regressor(**kwargs): pass


def NC_Database_Polynomial_Regressor(**kwargs):
	'''Required Parameters in Kwargs: 
	degree -> int
	NC_database -> dataframe containing data (Probably NC data)
	alpha -> int
	'''
	y = kwargs['NC_database'].Math.astype(float).values
	X = removesection(kwargs['NC_database'], ['Biology', 'Math', 'English', 'StateNamePublicSchoolLatestavailableyear', 'LocationAddress1PublicSchool201415', 
		'LocationCityPublicSchool201415', 'LocationZIPPublicSchool201415', 'TitleISchoolStatusPublicSchool201415', 'LowestGradeOfferedPublicSchool201415', 
		'HighestGradeOfferedPublicSchool201415', 'District', 'Grades912StudentsPublicSchool201415'])

	X_plot_encoder = LabelEncoder()

	X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8, random_state=225)

	X_train.SchoolNamePublicSchool201415 = X_plot_encoder.fit_transform(X_train.SchoolNamePublicSchool201415)
	school_encoded_train = X_train.SchoolNamePublicSchool201415.astype(int)
	X_train = removesection(X_train, ['SchoolNamePublicSchool201415'])
	X_train = PolynomialFeatures(kwargs['degree']).fit_transform(X_train)
	ka = StandardScaler().fit(X_train)
	X_train = ka.transform(X_train)
	ma = Ridge(alpha=kwargs['alpha'])

	ma.fit(X_train, y_train)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.scatter(school_encoded_train, y_train)
	plt.scatter(school_encoded_train, ma.predict(X_train))
	props = dict(boxstyle='round', facecolor='white', alpha=.5)
	ax.text(0.01, 0.026, 'Score = {}'.format(ma.score(X_train, y_train)), transform=ax.transAxes, verticalalignment='top', bbox=props)
	plt.title(kwargs['title'])
	plt.xlabel(kwargs['xaxis'])
	plt.ylabel(kwargs['yaxis'])
	if kwargs['file_name']:
		if kwargs['location']:
			plt.savefig('{}/{} Train'.format(kwargs['location'], kwargs['file_name']) + '.png')
		else:
			plt.savefig('Graphs/{}'.format(kwargs['file_name']) + '.png')
			
	mng = plt.get_current_fig_manager()
	mng.resize(*mng.window.maxsize())
	plt.show()
	
	X_test.SchoolNamePublicSchool201415 = X_plot_encoder.fit_transform(X_test.SchoolNamePublicSchool201415)
	school_encoded_test = X_test.SchoolNamePublicSchool201415
	X_test = removesection(X_test, ['SchoolNamePublicSchool201415',])
	X_test = PolynomialFeatures(kwargs['degree']).fit_transform(X_test)
	X_test = ka.transform(X_test)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.scatter(school_encoded_test, y_test)
	plt.scatter(school_encoded_test, ma.predict(X_test))
	props = dict(boxstyle='round', facecolor='white', alpha=.5)
	ax.text(0.01, 0.026, 'Score = {}'.format(ma.score(X_test, y_test)), transform=ax.transAxes, verticalalignment='top', bbox=props)
	
	if kwargs['file_name']:
		if kwargs['location']:
			plt.savefig('{}/{} Test'.format(kwargs['location'], kwargs['file_name']) + '.png')
		else:
			plt.savefig('Graphs/{}'.format(kwargs['file_name']) + '.png')

	plt.show()

	cross_validation = cross_val_score(ma, X_test, y_test)
	secondary_validation = cross_val_score(ma, X_train, y_train)
	return {'cross_val_mean_train': cross_validation.mean(), 'cross_val_error_train': cross_validation.std() * 2, 'cross_val_mean_test': secondary_validation.mean(), 'cross_val_error_test': secondary_validation.std() * 2}