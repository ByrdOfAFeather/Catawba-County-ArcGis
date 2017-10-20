
from bs4 import BeautifulSoup as bs
from data_classes import NC_database
import urllib2 as url
import requests as re 
# <input type="text" name="InstName" size="36"> 

def get_reduced_lunch(NC_DataFrame):

	base_link = 'https://nces.ed.gov/ccd/schoolsearch/'
	school_type_params = '&SchoolType=1&SchoolType=2&SchoolType=3&SchoolType=4'

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

	for names in NC_DataFrame.database['SchoolNamePublicSchool201415']:
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
		else: continue
		
		stats_page = base_link + link['href']
		stats_page = bs(re.get(stats_page).content, 'lxml')
		
		free_lunch = stats_page.find(text='Free lunch eligible: ').find_parent('td').contents[1].replace(",", "")
		reduced_lunch = stats_page.find(text='Reduced-price lunch eligible: ').find_parent('td').contents[1].replace(",", "")

		try:
			print('----------------FREE LUNCH {}------------------'.format(free_lunch))
		except UnicodeEncodeError:
			print('UNICODE ERROR')
		
		try:
			NC_DataFrame.database.loc[NC_DataFrame.database.SchoolNamePublicSchool201415==names, 'Reduced_lunch'] = int(reduced_lunch)
			NC_DataFrame.database.loc[NC_DataFrame.database.SchoolNamePublicSchool201415==names, 'Free Lunch'] = int(free_lunch)
			NC_DataFrame.database.loc[NC_DataFrame.database.SchoolNamePublicSchool201415==names, 'Percent Lunch'] = float( ( int(free_lunch) + int(reduced_lunch) ) / ( int(NC_DataFrame.database.loc[NC_DataFrame.database.SchoolNamePublicSchool201415==names, 'TotalStudentsAllGradesExcludesAEPublicSchool201415'] ) )) 
		except UnicodeEncodeError:
			print('UNICODE ERROR')
			pass


	NC_DataFrame.database.to_csv('Databases/scrape.csv')
	return NC_DataFrame


# https://nces.ed.gov/ccd/schoolsearch/school_list.asp?City=&Search=1&SchoolID=&SchoolType=4&Zip=&DistrictID=&LoGrade=-1&DistrictName=&HiGrade=-1&SpecificSchlTypes=all&InstName=Chatham+Charter&County=&Phone=&State=&Miles=&IncGrade=-1&Address=&PhoneAreaCode=
# https://nces.ed.gov/ccd/schoolsearch/school_list.asp?Search=1&InstName=Chatham+Charter&SchoolID=&Address=&City=&State=&Zip=&Miles=&County=&PhoneAreaCode=&Phone=&DistrictName=&DistrictID=&SchoolType=1&SchoolType=2&SchoolType=3&SchoolType=4&SpecificSchlTypes=all&IncGrade=-1&LoGrade=-1&HiGrade=-1