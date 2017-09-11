from data_transformation_functions import build_school_dict, build_grade_dict
from plot_functions import plot_schools
import matplotlib.pyplot as plt
import numpy as np 
from sklearn.preprocessing import LabelEncoder
import xlrd
report = xlrd.open_workbook('acctsumm17.xlsx').sheet_by_index(0)
northwest_schools = build_school_dict(report, 'Northwest') # form = {School: cellnumber}
northwest_grades = build_grade_dict(report, northwest_schools) # form = {Math, bio, eng, school}
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

plot_schools(northwest_grades, 0)
plot_schools(north_central_grades, 0)
plot_schools(western_grades, 0)
plot_schools(northeast_grades, 0)
plot_schools(southwest_grades, 0)
plot_schools(sandhills_grades, 0)
plot_schools(southeast_grades, 0)
plot_schools(piedmont_grades, 0)
