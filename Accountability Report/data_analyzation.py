# -*- coding: utf-8 -*-

from data_transformation_functions import merge_dicts, build_school_dict, build_grade_dict, build_grade_dataframe
from plot_functions import plot_schools
import matplotlib.pyplot as plt
import numpy as np 
from sklearn.preprocessing import LabelEncoder
import xlrd
import pandas as pd
from pandas.tools.plotting import scatter_matrix
report = xlrd.open_workbook('Databases/acctsumm17.xlsx').sheet_by_index(0)
northwest_schools = build_school_dict(report, 'Northwest') # form = {School: cellnumber}
northwest_grades = build_grade_dict(report, northwest_schools) # form = {Math, bio, eng, school}
northwest_dataframe = pd.DataFrame.from_dict(northwest_grades, orient='index')
north_central_schools = build_school_dict(report, 'North Central')
north_central_grades = build_grade_dict(report, north_central_schools)
western_schools = build_school_dict(report, 'Western')
western_grades = build_grade_dict(report, western_schools)
northeast_schools = build_school_dict(report, 'Northeast')
northeast_grades = build_grade_dict(report, northeast_schools)
southwest_schools = build_school_dict(report, 'Southwest')
southwest_grades = build_grade_dict(report, southwest_schools)
sandhills_schools = build_school_dict(report, 'Sandhills')
sandhills_grades = build_grade_dict(report, sandhills_schools)
southeast_schools = build_school_dict(report, 'Southeast')
southeast_grades = build_grade_dict(report, southeast_schools)
piedmont_schools = build_school_dict(report, 'Piedmont Triad')
piedmont_grades = build_grade_dict(report, piedmont_schools)

overall_grades = merge_dicts(northwest_schools, north_central_schools, western_schools, northeast_schools, southwest_schools, sandhills_schools, southeast_schools, piedmont_schools)
# k = LabelEncoder()
overall_dataframe = build_grade_dataframe(report, overall_grades)
# scatter_matrix(overall_dataframe, diagonal='kde')
# plt.show()

# relation_matrix = overall_dataframe.corr()
# print(relation_matrix)



### DATABASE COMBINATIONS ###
NC_database = pd.DataFrame.from_csv('Databases/NCLONGLAD.csv', encoding="utf-8")
NC_database.drop_duplicates(inplace=True)
overall_dataframe.drop_duplicates(inplace=True)
NC_database['exists'] = NC_database['School Name [Public School] 2014-15'].isin(overall_grades.keys())
NC_database = NC_database.drop(NC_database[NC_database['exists'] == False].index)
NC_database.drop('exists', axis=1, inplace=True)
NC_database = pd.merge(left=NC_database, right=overall_dataframe, left_on='School Name [Public School] 2014-15', right_on='School Name')
NC_database = NC_database.replace('â€'.decode('utf-8'), 'NaN')
NC_database = NC_database.replace('†'.decode('utf-8'), 'NaN')
NC_database = NC_database.replace('1-Yes', 1)
NC_database = NC_database.replace('2-No', 0)
NC_database.drop(['Location Address 3 [Public School] 2014-15', 'Location Address 2 [Public School] 2014-15', 'School Name', 'District'], axis=1, inplace=True)
NC_database['Grades 9-12 Students [Public School] 2014-15'] = NC_database['Grades 9-12 Students [Public School] 2014-15'].replace('NaN', 999999)
NC_database['Total Students All Grades (Excludes AE) [Public School] 2014-15'] = NC_database['Total Students All Grades (Excludes AE) [Public School] 2014-15'].replace('NaN', 999999)
NC_database['Location ZIP4 [Public School] 2014-15'] = NC_database['Location ZIP4 [Public School] 2014-15'].replace('NaN', 999999)
NC_database['Latitude [Public School] 2014-15'] = NC_database['Latitude [Public School] 2014-15'].replace('NaN', 99999)
NC_database['Longitude [Public School] 2014-15'] = NC_database['Longitude [Public School] 2014-15'].replace('NaN', 99999)
NC_database.to_csv('Databases/omega.csv')

### DATABASE SEPERATIONS ###
CORR_database = NC_database
CORR_database = CORR_database.replace('NaN', 999)
CORR_database = CORR_database.drop(CORR_database[CORR_database['Magnet School [Public School] 2014-15'] == 999].index)
CORR_database = CORR_database.drop(CORR_database[CORR_database['Charter School [Public School] 2014-15'] == 999].index)
CORR_database = CORR_database.drop(CORR_database[CORR_database['Title I Eligible School [Public School] 2014-15'] == 999].index)
CORR_database = CORR_database.drop(CORR_database[CORR_database['Grades 9-12 Students [Public School] 2014-15'] == 999999].index)

omega = CORR_database.corr()
print(omega)
