# -*- coding: utf-8 -*-
import pandas as pd
import xlrd


def build_school_dict(report, district_name): 
    '''Builds school dictionary given the sheet and district name 
    report: xlrd sheet object 
    district_name: string (Northwest, North Central, Western, Northeast, Southwest, Sandhils, Southeast, Piedmont Triad)'''
    schoolist = {}
    school_name_col = 2
    cell_no = -1 # Keeps track of the cell number as the iterations go through
    for items in report.col(3):
        cell_no += 1 
        district = report.cell_value(cell_no, 3)
        if district == district_name:
            schoolist[(report.cell_value(cell_no, school_name_col))] = [cell_no, district_name]
    return schoolist


def build_grade_dict(report, school_dict): 
    '''Builds a dictionary of school names to grade 
    report: xlrd sheet object
    school_dict: dictionary of schools formatted like {school_name: cellno}'''
    grade_list = {}
    for schools, listitems in school_dict.iteritems():
        math_grade = report.cell_value(listitems[0], 33).replace('>95', '95').replace('<10', '10').replace('<5', '5')
        bio_grade = report.cell_value(listitems[0], 36).replace('>95', '95').replace('<10', '10').replace('<5', '5')
        eng_grade = report.cell_value(listitems[0], 39).replace('>95', '95').replace('<10', '10').replace('<5', '5')
        school_grade = report.cell_value(listitems[0], 6)
        if [i for i in ['*', '', 'N/A'] if i in [str(math_grade), str(bio_grade), str(eng_grade), school_grade]]:
            pass
        else:
            if school_grade == "A+NG":
                school_grade = "A"
            grade_list[schools] = "%s, %s, %s, %s" %(str(math_grade), str(bio_grade), str(eng_grade), school_grade)
    return grade_list


def build_grade_dataframe(report, school_dict): 
    '''Builds a dictionary of school names to grade 
    report: xlrd sheet object
    school_dict: dictionary of schools formatted like {school_name: cellno}'''
    school_list = []
    math_list = []
    bio_list = []
    eng_list = [] 
    district_name_list = [] 
    school_name_list = []
    for schools, listitems in school_dict.iteritems():
        math_grade = report.cell_value(listitems[0], 33).replace('>95', '95').replace('<10', '10').replace('<5', '5')
        bio_grade = report.cell_value(listitems[0], 36).replace('>95', '95').replace('<10', '10').replace('<5', '5')
        eng_grade = report.cell_value(listitems[0], 39).replace('>95', '95').replace('<10', '10').replace('<5', '5')
        school_grade = report.cell_value(listitems[0], 6)
        if [i for i in ['*', '', 'N/A'] if i in [str(math_grade), str(bio_grade), str(eng_grade), school_grade]]:
            pass
        else:
            if school_grade == "A+NG":
                school_grade = "A"
            school_list.append(schools)
            math_list.append(float(math_grade))
            bio_list.append(float(bio_grade))
            eng_list.append(float(eng_grade))
            district_name_list.append(listitems[1])
            school_name_list.append(schools)

    dataframe = pd.DataFrame({'School': school_list, 'Math': math_list, 'Biology': bio_list, 'English': eng_list, 'District': district_name_list, 'School Name': school_name_list})
    dataframe.set_index(['School'], inplace=True)
    return dataframe


def merge_dicts(*dict_args):
    '''Merges X number of dicts
    source: http://bit.ly/2y72rHo'''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def setup_dicts():
    '''Gets schools by distrcit and combines them into 
    an overall dataframe as well as a grade dictionary'''
    report = xlrd.open_workbook('Databases/acctsumm15.xlsx').sheet_by_index(0)
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
    piedmont_schools = build_school_dict(report, 'Piedmont-Triad')
    piedmont_grades = build_grade_dict(report, piedmont_schools)
    overall_grades = merge_dicts(northwest_schools, north_central_schools, western_schools, northeast_schools, southwest_schools, sandhills_schools, southeast_schools, piedmont_schools)
    overall_dataframe = build_grade_dataframe(report, overall_grades)
    return (overall_dataframe, overall_grades)


def removesection(frame, *args):
    '''removes sections from a dataframe 
    frame = dataframe 
    *args = strings of columns that need to be removed

    returns frame - edited version of frame'''
    dframe = frame
    for sections in args:
        dframe = dframe.drop(frame[sections], axis=1)
    return dframe


def replace_item(frame, **kwargs):
    '''Replaces items in a frame
    frame = dataframe 
    **kwargs = dictionary with key=original item=replacement'''
    for search, replace in kwargs.items():
        frame = frame.replace(search, replace)
    return frame


def setup_nc_dataframe(overall_grades, overall_dataframe):
    NC_database = pd.DataFrame.from_csv('Databases/scrape.csv')
    return NC_database