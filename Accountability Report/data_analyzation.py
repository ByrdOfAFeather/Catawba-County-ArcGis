from data_transformation_functions import build_school_dict, build_grade_dict
from plot_functions import plot_schools
import matplotlib.pyplot as plt
import numpy as np 
from sklearn.preprocessing import LabelEncoder
import xlrd
import pandas as pd
from pandas.tools.plotting import scatter_matrix
report = xlrd.open_workbook('acctsumm17.xlsx').sheet_by_index(0)
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


print(northwest_dataframe)
s = northwest_dataframe[0]
northwest_dataframe.join(s.apply(lambda x: pd.Series(x.split(', '))), how='left', lsuffix='_left', rsuffix='_right')
print('--------------------------------')
print(northwest_dataframe)
print(northwest_dataframe.reset_index()[[0]])
scatter_matrix(northwest_dataframe, diagonal='kde')



