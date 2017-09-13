from data_transformation_functions import merge_dicts, build_school_dict, build_grade_dict, build_grade_dataframe
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

overall_grades = merge_dicts(northwest_schools, north_central_schools, western_schools, northeast_schools, southwest_schools, 
							 sandhills_schools, southeast_schools, piedmont_schools)
k = LabelEncoder()
overall_dataframe = build_grade_dataframe(report, overall_grades)
overall_dataframe['District'] = k.fit_transform(overall_dataframe['District'])

scatter_matrix(overall_dataframe, diagonal='kde')
plt.show()

relation_matrix = overall_dataframe.corr()
print(relation_matrix)

