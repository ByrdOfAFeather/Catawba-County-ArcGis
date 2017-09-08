from data_transformation_functions import build_school_list, build_dict
import xlrd
report = xlrd.open_workbook('acctsumm17.xlsx').sheet_by_index(0)
test = build_school_list(report, 'Northwest')
other_test = build_dict(report, test)
print(test)
print(other_test)
