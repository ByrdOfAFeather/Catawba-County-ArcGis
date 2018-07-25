# -*- coding: utf-8 -*-
import pandas as pd
import xlrd


def build_school_dict(report, district_name): 
	"""Builds school dictionary given the sheet and district name
	:param report: xlrd sheet object
	:param district_name: string (Northwest, North Central, Western, Northeast, Southwest, Sandhils, Southeast, Piedmont Triad)
	"""
	# Starts from the second column and keeps track of the cell number starting from 0
	school_list = {}
	school_name_col = 2
	cell_no = -1  # Keeps track of the cell number as the iterations go through
	for _ in report.col(3):
		cell_no += 1
		district = report.cell_value(cell_no, 3)
		if district == district_name:
			school_list[(report.cell_value(cell_no, school_name_col))] = [cell_no, district_name]
	return school_list


def build_grade_dict(report, school_dict): 
	"""Builds a dictionary of school names to grade
	:param report: xlrd sheet object
	:param school_dict: dictionary of schools formatted like {school_name: cellno}"""
	grade_list = {}

	for schools, list_items in school_dict.iteritems():
		# Replaces values to be represented as ints
		math_grade = report.cell_value(list_items[0], 33).replace('>95', '95').replace('<10', '10').replace('<5', '5')
		bio_grade = report.cell_value(list_items[0], 36).replace('>95', '95').replace('<10', '10').replace('<5', '5')
		eng_grade = report.cell_value(list_items[0], 39).replace('>95', '95').replace('<10', '10').replace('<5', '5')
		school_grade = report.cell_value(list_items[0], 6)

		# Removes non-int values from the list
		if [i for i in ['*', '', 'N/A'] if i in [str(math_grade), str(bio_grade), str(eng_grade), school_grade]]:
			pass
		else:
			# Replaces A's to A [A + NG is relatively meaningless in terms of this project]
			if school_grade == "A+NG":
				school_grade = "A"
			grade_list[schools] = "%s, %s, %s, %s" %(str(math_grade), str(bio_grade), str(eng_grade), school_grade)
	return grade_list


def build_grade_dataframe(report, school_dict): 
	"""Builds a dictionary of school names to grade
	:param report: xlrd sheet object
	:param school_dict: dictionary of schools formatted like {school_name: cellno}"""
	# Declares empty lists
	school_list = []
	math_list = []
	bio_list = []
	eng_list = []
	district_name_list = []
	school_name_list = []

	# Loops and removes and replaces values that can't be stored as integers
	for schools, listitems in school_dict.items():
		math_grade = report.cell_value(listitems[0], 33).replace('>95', '95').replace('<10', '10').replace('<5', '5')
		bio_grade = report.cell_value(listitems[0], 36).replace('>95', '95').replace('<10', '10').replace('<5', '5')
		eng_grade = report.cell_value(listitems[0], 39).replace('>95', '95').replace('<10', '10').replace('<5', '5')
		if [i for i in ['*', '', 'N/A'] if i in [str(math_grade), str(bio_grade), str(eng_grade)]]:
			pass
		else:
			school_list.append(schools)
			math_list.append(float(math_grade))
			bio_list.append(float(bio_grade))
			eng_list.append(float(eng_grade))
			district_name_list.append(listitems[1])
			school_name_list.append(schools)

	# Builds a dataframe with built lists
	dataframe = pd.DataFrame({'School': school_list, 'Math': math_list, 'Biology': bio_list,
	                          'English': eng_list, 'District': district_name_list, 'School Name': school_name_list})
	dataframe.set_index(['School'], inplace=True)
	return dataframe


def merge_dicts(*dict_args):
	"""Merges X number of dicts
	:param dict_args: n number of dicts
	source: http://bit.ly/2y72rHo"""
	result = {}
	for dictionary in dict_args:
		result.update(dictionary)
	return result


def setup_dicts():
	"""Gets schools by district and combines them into
	an overall dataframe as well as a grade dictionary"""
	report = xlrd.open_workbook('Databases/acctsumm15.xlsx').sheet_by_index(0)
	northwest_schools = build_school_dict(report, 'Northwest')  # form = {School: cellnumber}
	north_central_schools = build_school_dict(report, 'North Central')
	western_schools = build_school_dict(report, 'Western')
	northeast_schools = build_school_dict(report, 'Northeast')
	southwest_schools = build_school_dict(report, 'Southwest')
	sandhills_schools = build_school_dict(report, 'Sandhills')
	southeast_schools = build_school_dict(report, 'Southeast')
	piedmont_schools = build_school_dict(report, 'Piedmont-Triad')
	overall_grades = merge_dicts(northwest_schools, north_central_schools, western_schools, northeast_schools,
								 southwest_schools, sandhills_schools, southeast_schools, piedmont_schools)
	overall_dataframe = build_grade_dataframe(report, overall_grades)
	return overall_dataframe, overall_grades


def remove_section(frame, *args):
	"""removes sections from a dataframe
	:param frame: dataframe
	:param args: strings of columns that need to be removed

	returns frame - edited version of frame"""

	dframe = frame
	for sections in args:
		dframe = dframe.drop(frame[sections], axis=1)
	return dframe


def replace_item(frame, **kwargs):
	"""Replaces items in a frame
	:param frame: dataframe
	:param kwargs: dictionary with key=original item=replacement"""

	for search, replace in kwargs.items():
		frame = frame.replace(search, replace)
	return frame


def setup_nc_dataframe(overall_grades, overall_dataframe):
	"""Sets up NC_database
	:param overall_grades: dictionary with grades attached to school names
	:param overall_dataframe: dataframe with schools attached to their data
	:param overall_grades: can be obtained through setup_dicts()
	:param overall_dataframe: can be obtained through setup_dicts()"""

	# setups the NC database
	nc_database = pd.DataFrame.from_csv('Databases/NCLONGLAD.csv', encoding="utf-8")
	st_ratio = pd.DataFrame.from_csv('Databases/stratio.csv', encoding="utf-8")
	nc_database['StudentTeacherRatio'] = st_ratio['Pupil/Teacher Ratio [Public School] 2014-15']

	nc_database['exists'] = nc_database['School Name [Public School] 2014-15'].isin(overall_grades.keys())
	nc_database = nc_database.drop(nc_database[nc_database['exists'] == False].index)
	nc_database = pd.merge(left=nc_database, right=overall_dataframe, left_on='School Name [Public School] 2014-15',
	                       right_on='School Name')

	replacements = {'â€'.decode('utf-8'): 'NaN', '†'.decode('utf-8'): 'NaN', '1-Yes': 1, '2-No': 0,
	                '1-Regular school': 1, '2-Special education school': 2, '3-Vocational school': 3,
	                '4-Alternative/other school': 4,
	                '4-Eligible for Title I SWP provides no program': 4, '6-Not eligible for either TAS or SWP': 6,
	                '5-Eligible for Title I SWP provides SWP program': 5,
	                '1-Eligible for Title I TAS provides no program': 1,
	                '3-Eligible for Title I SWP provides TAS program': 3,
	                '2-Eligible for Title I TAS provides TAS program': 2}
	nc_database = replace_item(nc_database, **replacements)
	nc_database = remove_section(nc_database, ['Location Address 3 [Public School] 2014-15',
	                                          'Location Address 2 [Public School] 2014-15', 'School Name',
	                                          'Location ZIP4 [Public School] 2014-15', 'exists'])

	nc_database['Grades 9-12 Students [Public School] 2014-15'] = nc_database[
		'Grades 9-12 Students [Public School] 2014-15'].replace('NaN', 999999)
	nc_database['Total Students All Grades (Excludes AE) [Public School] 2014-15'] = nc_database[
		'Total Students All Grades (Excludes AE) [Public School] 2014-15'].replace('NaN', 999999)
	nc_database['Latitude [Public School] 2014-15'] = nc_database['Latitude [Public School] 2014-15'].replace('NaN',
	                                                                                                          99999)
	nc_database['Longitude [Public School] 2014-15'] = nc_database['Longitude [Public School] 2014-15'].replace('NaN',
	                                                                                                            99999)

	new_columns = []
	for columns in nc_database.columns.values:
		new_columns.append(
			columns.replace('-', '').replace(' ', '').replace('[', '').replace(']', '').replace('(', '').replace(')',
			                                                                                                     ''))

	nc_database.columns = new_columns
	return nc_database
