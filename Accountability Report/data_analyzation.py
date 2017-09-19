# -*- coding: utf-8 -*-

from data_transformation_functions import merge_dicts, build_school_dict, build_grade_dict, build_grade_dataframe, setup_dicts, setup_NC_DATAFRAME
from plot_functions import plot_schools
import matplotlib.pyplot as plt
import numpy as np 
from sklearn import svm
from sklearn.preprocessing import LabelEncoder
import xlrd
import pandas as pd
from pandas.tools.plotting import scatter_matrix
from mpl_toolkits.mplot3d import Axes3D


overall_dataframe = setup_dicts()[0]
overall_grades = setup_dicts()[1]



### DATABASE COMBINATIONS ###
NC_database = setup_NC_DATAFRAME(overall_grades, overall_dataframe)
# NC_database.to_csv('Databases/Purified.csv')
NC_database['Omega'] = list(zip(NC_database.LatitudePublicSchool201415, NC_database.LongitudePublicSchool201415))
save = np.array(list(NC_database.Biology.values), dtype=np.float)
values = NC_database.Biology >= 70 
negvalues = NC_database.Biology < 70

col_name = 'Biology'
NC_database.loc[values, col_name] = 1 
NC_database.loc[negvalues, col_name] = 0





y_list = NC_database['Biology'].values
print(y_list)
print(y_list.shape)
X = NC_database['Omega'].values
X = np.array(list(X), dtype=np.float)
this = np.array(list(NC_database.LatitudePublicSchool201415), dtype=np.float)
that = np.array(list(NC_database.LongitudePublicSchool201415), dtype=np.float)
omegasprem = svm.SVC(kernel='linear')
omegasprem.fit(X, y_list)
print(omegasprem.predict(np.reshape((36, -80), (1, 1))))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(this, that, save)
plt.show()















# ### DATABASE SEPERATIONS ###
# CORR_database = CORR_database.drop(CORR_database[CORR_database['MagnetSchoolPublicSchool201415'] == 999].index)
# CORR_database = CORR_database.drop(CORR_database[CORR_database['CharterSchoolPublic School201415'] == 999].index)
# CORR_database = CORR_database.drop(CORR_database[CORR_database['TitleIEligibleSchoolPublicSchool201415'] == 999].index)
# CORR_database = CORR_database.drop(CORR_database[CORR_database['Grades912StudentsPublicSchool201415'] == 999999].index)

