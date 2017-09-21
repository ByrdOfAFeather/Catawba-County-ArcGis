# -*- coding: utf-8 -*-

from data_transformation_functions import merge_dicts, build_school_dict, build_grade_dict, build_grade_dataframe, setup_dicts, setup_NC_DATAFRAME
import plot_functions as custplt
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
