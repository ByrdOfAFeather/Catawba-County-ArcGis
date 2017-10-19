
from bs4 import BeautifulSoup as bs
from data_classes import NC_database
import urllib2 as url
import requests as re 
# <input type="text" name="InstName" size="36"> 

def get_reduced_lunch(NC_DataFrame):

	base_link = 'https://nces.ed.gov/ccd/schoolsearch/'

	data = {
	"Search": "1",
	"SchoolID": "",
	"Address": "",
	"City": "",
	"State": "",
	"Zip": "",
	"Miles": "",
	"County": "",
	"PhoneAreaCode": "",
	"Phone": "",
	"DistrictName": "",
	"DistrictID": "",
	"SchoolType": "1",
	"SchoolType": "2",
	"SchoolType": "3",
	"SchoolType": "4",
	"SpecificSchlTypes": "all",
	"IncGrade": "-1",
	"LoGrade": "-1",
	"HiGrade": "-1"
	}

	for names in NC_DataFrame.database['SchoolNamePublicSchool201415']:
		print(names)
		data["InstName"] = names
		search_result = re.post('https://nces.ed.gov/ccd/schoolsearch/school_list.asp', params=data)
		print(search_result.url)
		result = bs(search_result.text, 'lxml')
		link = result.find(text=names).find_parent("a", href=True)
		
		stats_page = base_link + link['href']
		stats_page = bs(re.get(stats_page).content, 'lxml')
		
		free_lunch = stats_page.find(text='Free lunch eligible: ').find_parent('td').contents[1]
		reduced_lunch = stats_page.find(text='Reduced-price lunch eligible: ').find_parent('td').contents[1]

		NC_DataFrame.loc[NC_DataFrame.SchoolNamePublicSchool201415==names, "Reduced_lunch"] = int(reduced_lunch)
		print(NC_DataFrame.database['Reduced_lunch'])


get_reduced_lunch(NC_database())
	