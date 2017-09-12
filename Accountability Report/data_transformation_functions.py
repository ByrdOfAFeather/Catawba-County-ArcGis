import pandas as pd
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
            schoolist[(report.cell_value(cell_no, school_name_col))] = cell_no
    return schoolist
def build_grade_dict(report, school_dict): 
    '''Builds a dictionary of school names to grade 
    report: xlrd sheet object
    school_dict: dictionary of schools formatted like {school_name: cellno}'''
    grade_list = {}
    for schools, cell_no in school_dict.iteritems():
        math_grade = report.cell_value(cell_no, 33).replace('>95', '95').replace('<10', '10').replace('<5', '5')
        bio_grade = report.cell_value(cell_no, 36).replace('>95', '95').replace('<10', '10').replace('<5', '5')
        eng_grade = report.cell_value(cell_no, 39).replace('>95', '95').replace('<10', '10').replace('<5', '5')
        school_grade = report.cell_value(cell_no, 6)
        if [i for i in ['*', '', 'N/A'] if i in [str(math_grade), str(bio_grade), str(eng_grade), school_grade]]:
            pass
        else:
            if school_grade == "A+NG":
                school_grade = "A"

            grade_list[schools] = "%s, %s, %s, %s" %(str(math_grade), str(bio_grade), str(eng_grade), school_grade)
    return grade_list

