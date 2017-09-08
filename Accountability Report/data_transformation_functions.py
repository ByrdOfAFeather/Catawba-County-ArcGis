def build_school_list(report, district_name): 
    schoolist = {}
    school_name_col = 2
    cell_no = -1 # Keeps track of the cell number as the iterations go through
    for items in report.col(3):
        cell_no += 1 
        district = report.cell_value(cell_no, 3)
        if district == district_name:
            schoolist[(report.cell_value(cell_no, school_name_col))] = cell_no
    return schoolist
def build_dict(report, school_list): 
    grade_list = {}
    for schools, cell_no in school_list.iteritems():
        math_grade = report.cell_value(cell_no, 33)
        bio_grade = report.cell_value(cell_no, 36)
        eng_grade = report.cell_value(cell_no, 39)
        school_grade = report.cell_value(cell_no, 6)
        grade_list[schools] = "%s %s %s %s" %(math_grade, bio_grade, eng_grade, school_grade)