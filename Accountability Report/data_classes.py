import xlrd
from data_transformation_functions import setup_nc_dataframe, setup_dicts, removesection
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split 

class NC_database:
	def __init__(self):
		self.report = xlrd.open_workbook('Databases/acctsumm15.xlsx').sheet_by_index(0)
		self.overall = setup_dicts()
		self.overall_dataframe = self.overall[0]
		self.overall_grades = self.overall[1]
		self.database = setup_nc_dataframe(self.overall_grades, self.overall_dataframe)

	def classification_setup(self, target_value='math', score_threshold=60):
		y = self.database[target_value].values.astype(float).values
		X = removesection(self.database, ['Biology', 'Math', 'English', 'StateNamePublicSchoolLatestavailableyear', 'LocationAddress1PublicSchool201415', 
			'LocationCityPublicSchool201415', 'LocationZIPPublicSchool201415', 'TitleISchoolStatusPublicSchool201415', 'LowestGradeOfferedPublicSchool201415', 
			'HighestGradeOfferedPublicSchool201415', 'District', 'Grades912StudentsPublicSchool201415'])


	def regression_setup(self, target_value='Math', degree=2):
		y = self.database[target_value].astype(float).values
		X_without_school_names = removesection(self.database, ['SchoolNamePublicSchool201415'])
		X = removesection(self.database, ['Biology', 'Math', 'English', 'StateNamePublicSchoolLatestavailableyear', 'LocationAddress1PublicSchool201415', 
			'LocationCityPublicSchool201415', 'LocationZIPPublicSchool201415', 'LowestGradeOfferedPublicSchool201415', 
			'HighestGradeOfferedPublicSchool201415', 'District', 'Grades912StudentsPublicSchool201415'])

		X_plot_encoder = LabelEncoder()

		X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8, random_state=225)

		X_train.SchoolNamePublicSchool201415 = X_plot_encoder.fit_transform(X_train.SchoolNamePublicSchool201415)
		school_encoded_train = X_train.SchoolNamePublicSchool201415.astype(int)
		X_train = removesection(X_train, ['SchoolNamePublicSchool201415'])
		X_train = PolynomialFeatures(degree).fit_transform(X_train)
		ka = StandardScaler().fit(X_train)
		X_train = ka.transform(X_train)

		X_test.SchoolNamePublicSchool201415 = X_plot_encoder.fit_transform(X_test.SchoolNamePublicSchool201415)
		school_encoded_test = X_test.SchoolNamePublicSchool201415
		X_test = removesection(X_test, ['SchoolNamePublicSchool201415',])
		X_test = PolynomialFeatures(degree).fit_transform(X_test)
		X_test = ka.transform(X_test)
		
		return (X_without_school_names, y, X_train, school_encoded_train, y_train, X_test, school_encoded_test, y_test)