import xlrd
from data_transformation_functions import setup_nc_dataframe, setup_dicts, remove_section
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split


class NCDatabase:
	def __init__(self):
		self.report = xlrd.open_workbook('Databases/acctsumm15.xlsx').sheet_by_index(0)
		self.overall = setup_dicts()
		self.overall_dataframe = self.overall[0]
		self.overall_grades = self.overall[1]
		self.database = setup_nc_dataframe(self.overall_grades, self.overall_dataframe)

	def classification_setup(self, target_subject='Math', score_threshold=None):
		"""Sets up the NC Database for classification based on input
		:param target_subject: Target subject, valid options are "Math", "English", or "Biology"
		:param score_threshold: Optional to split the database into two classes, below and above the threshold"""

		# Given a score threshold: there are only two classes, one less than the score and one greater than the score
		if score_threshold:
			self.database.loc[self.database[target_subject] < score_threshold, target_subject] = 0
			self.database.loc[self.database[target_subject] >= score_threshold, target_subject] = 1
		
		else:
			# Splits into 8 classes
			self.database[target_subject][(self.database[target_subject] < 14)] = 0
			self.database[target_subject][(self.database[target_subject] >= 14) & (self.database[target_subject] < 25)] = 1
			self.database[target_subject][(self.database[target_subject] >= 25) & (self.database[target_subject] < 37)] = 2
			self.database[target_subject][(self.database[target_subject] >= 37) & (self.database[target_subject] < 50)] = 3
			self.database[target_subject][(self.database[target_subject] >= 50) & (self.database[target_subject] < 63)] = 4
			self.database[target_subject][(self.database[target_subject] >= 63) & (self.database[target_subject] < 75)] = 5
			self.database[target_subject][(self.database[target_subject] >= 75) & (self.database[target_subject] < 87.5)] = 6
			self.database[target_subject][(self.database[target_subject] >= 87.5) & (self.database[target_subject] < 100)] = 7

		# Sets up an encoder to encode school names
		x_plot_encoder = LabelEncoder()
		# Gets the full y-value vector
		y = self.database[target_subject].values.astype(float)
		# Removes the irrelevant sections of the original data set
		x = remove_section(self.database, ['Biology', 'Math', 'English', 'StateNamePublicSchoolLatestavailableyear',
		                                  'LocationAddress1PublicSchool201415', 'LocationCityPublicSchool201415',
		                                  'LocationZIPPublicSchool201415', 'TitleISchoolStatusPublicSchool201415',
		                                  'LowestGradeOfferedPublicSchool201415',
		                                  'HighestGradeOfferedPublicSchool201415', 'District',
		                                  'Grades912StudentsPublicSchool201415',
		                                  'Grade12offeredPublicSchool201415',
		                                  'Grade11offeredPublicSchool201415',
		                                  'Grade10offeredPublicSchool201415',
		                                  'Grade9offeredPublicSchool201415'])

		# Gets a dataset without the names of the schools
		x_without_school_names = remove_section(x, ['SchoolNamePublicSchool201415'])
		# Gets training and validation sets
		x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=.7, random_state=225530)

		# Fits an encoder to the school names in the training set
		x_train.SchoolNamePublicSchool201415 = x_plot_encoder.fit_transform(x_train.SchoolNamePublicSchool201415)

		# gets the integer values of the school names as they are encoded
		school_encoded_train = x_train.SchoolNamePublicSchool201415.astype(int)

		# removes the school names from the training set
		x_train = remove_section(x_train, ['SchoolNamePublicSchool201415'])

		# creates a standard scaler and fits it to x_train
		ka = StandardScaler().fit(x_train)
		# scales x_train
		x_train = ka.transform(x_train)

		# Does the previous steps to the testing set
		x_test.SchoolNamePublicSchool201415 = x_plot_encoder.fit_transform(x_test.SchoolNamePublicSchool201415)
		school_encoded_test = x_test.SchoolNamePublicSchool201415
		x_test = remove_section(x_test, ['SchoolNamePublicSchool201415',])
		x_test = ka.transform(x_test)

		# writes the database out to a csv
		try:
			x.to_csv('Databases/classification.csv')
		except IOError:
			print("Error writing database to file! Continuing...")

		# Returns the segmented values for model building functions
		return x_without_school_names, y, x_train, school_encoded_train, y_train, x_test, school_encoded_test, y_test

	def regression_setup(self, target_subject='Math', degree=2):
		"""Setups NC Database for regression
		:param target_subject: Target subject, valid options are "Math", "English", or "Biology"
		:param degree: Optional definition to declare the degree of polynomial features"""

		# sets up target values
		y = self.database[target_subject].astype(float).values

		# Removes irrelevant values
		x = remove_section(self.database, ['Biology', 'Math', 'English', 'StateNamePublicSchoolLatestavailableyear',
		                                  'LocationAddress1PublicSchool201415', 'LocationCityPublicSchool201415',
		                                  'LocationZIPPublicSchool201415', 'TitleISchoolStatusPublicSchool201415',
		                                  'LowestGradeOfferedPublicSchool201415',
		                                  'HighestGradeOfferedPublicSchool201415', 'District',
		                                  'Grades912StudentsPublicSchool201415',
		                                  'Grade12offeredPublicSchool201415',
		                                  'Grade11offeredPublicSchool201415',
		                                  'Grade10offeredPublicSchool201415',
		                                  'Grade9offeredPublicSchool201415'])
		# Creates an encoder
		x_plot_encoder = LabelEncoder()

		# Gets rid of schools names and splits the data sets
		x_without_school_names = remove_section(x, ['SchoolNamePublicSchool201415'])
		x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=.7, random_state=225)

		# Fits the encoder to the school names and remove the sections
		x_train.SchoolNamePublicSchool201415 = x_plot_encoder.fit_transform(x_train.SchoolNamePublicSchool201415)
		school_encoded_train = x_train.SchoolNamePublicSchool201415.astype(int)
		x_train = remove_section(x_train, ['SchoolNamePublicSchool201415'])

		# Creates polynomial features
		x_train = PolynomialFeatures(degree).fit_transform(x_train)
		ka = StandardScaler().fit(x_train)
		x_train = ka.transform(x_train)

		# sets the same features up on the test set
		x_test.SchoolNamePublicSchool201415 = x_plot_encoder.fit_transform(x_test.SchoolNamePublicSchool201415)
		school_encoded_test = x_test.SchoolNamePublicSchool201415
		x_test = remove_section(x_test, ['SchoolNamePublicSchool201415',])
		x_test = PolynomialFeatures(degree).fit_transform(x_test)
		x_test = ka.transform(x_test)

		# Saves a copy of the current database
		try:
			x.to_csv('Databases/regression.csv')
		except IOError:
			print("Failed to save the database to file! Continuing....")
		
		return x_without_school_names, y, x_train, school_encoded_train, y_train, x_test, school_encoded_test, y_test
