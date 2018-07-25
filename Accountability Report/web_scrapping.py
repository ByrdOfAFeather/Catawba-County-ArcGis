
from bs4 import BeautifulSoup as bs
from data_classes import NC_database
import pandas as pd
import urllib2 as url
import requests as re 


def get_reduced_lunch(nc_dataframe):
	"""simply searches every school in the data frame to find free and reduced lunches percentages"""
	base_link = 'https://nces.ed.gov/ccd/schoolsearch/'

	data = [
		("Search", "1"),
		("SchoolID", ""),
		("Address", ""),
		("City", ""),
		("State", ""),
		("Zip", ""),
		("Miles", ""),
		("County", ""),
		("PhoneAreaCode", ""),
		("Phone", ""),
		("DistrictName", ""),
		("DistrictID", ""),
		("SpecificSchlTypes", "all"),
		("IncGrade", "-1"),
		("LoGrade", "-1"),
		("HiGrade", "-1"),
		("SchoolType", "1"),
		("SchoolType", "2"),
		("SchoolType", "3"),
		("SchoolType", "4")
	]

	for names in nc_dataframe.database['SchoolNamePublicSchool201415']:
		print(names)
		data.append(("InstName", names))
		search_result = re.post('https://nces.ed.gov/ccd/schoolsearch/school_list.asp', params=data)
		data.pop()
		print(search_result.url)
		result = bs(search_result.text, 'lxml')
		if result.find(text=names.upper()):
			link = result.find(text=names.upper()).find_parent('a', href=True)
		elif result.find(text=names.lower()):
			link = result.find(text=names.lower()).find_parent('a', href=True)
		elif result.find(text=names):
			link = result.find(text=names).find_parent('a', href=True)
		else:
			nc_dataframe.database = nc_dataframe.database.drop(
				nc_dataframe.database[nc_dataframe.database['SchoolNamePublicSchool201415'] == names].index)
		
		stats_page = base_link + link['href']
		stats_page = bs(re.get(stats_page).content, 'lxml')
		
		free_lunch = stats_page.find(text='Free lunch eligible: ').find_parent('td').contents[1].replace(",", "")
		reduced_lunch = stats_page.find(text='Reduced-price lunch eligible: ')\
			.find_parent('td').contents[1].replace(",", "")

		try:
			print('----------------FREE LUNCH {}------------------'.format(free_lunch))
		except UnicodeEncodeError:
			print('UNICODE ERROR')
		
		try:
			nc_dataframe.database.loc[
				nc_dataframe.database.SchoolNamePublicSchool201415 == names, 'Reduced Lunch'
			] = int(reduced_lunch)
			nc_dataframe.database.loc[
				nc_dataframe.database.SchoolNamePublicSchool201415 == names, 'Free Lunch'
			] = int(free_lunch)
			try:
				nc_dataframe.database.loc[nc_dataframe.database.SchoolNamePublicSchool201415 == names, 'Percent Lunch'] = float(
					(float(free_lunch) + float(reduced_lunch)) /
				 	(float(nc_dataframe.database.loc[
					            nc_dataframe.database.SchoolNamePublicSchool201415 == names,
				 		'TotalStudentsAllGradesExcludesAEPublicSchool201415'])
				    )
				)
			except TypeError:
				nc_dataframe.database = nc_dataframe.database[nc_dataframe.database.SchoolNamePublicSchool201415 != names]

		except UnicodeEncodeError:
			print('UNICODE ERROR')
			pass

	nc_dataframe.database['Free Lunch'] = pd.to_numeric(nc_dataframe.database['Free Lunch'])
	nc_dataframe.database['Reduced Lunch'] = pd.to_numeric(nc_dataframe.database['Reduced Lunch'])
	nc_dataframe.database['Percent Lunch'] = pd.to_numeric(nc_dataframe.database['Percent Lunch'])
	nc_dataframe.database.to_csv('Databases/scrape.csv')
	return nc_dataframe.database