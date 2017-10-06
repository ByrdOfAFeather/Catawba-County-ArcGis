# Accountablity Report Section:
Exploring trends in North Carolina Education data, focusing on the correlation between Education and Location. 

* Python Files:
	* data_analyzation.py - Main file for analyzing data 
	* data_transformation_functions.py - File for building dictionaries and formatting dataframes
	* plot_functions.py - File for plotting dataframes 

* Database Files: 
	* NCLONGLAD.csv - File taken from the National Center for Education Statistics, contains a multitude of information about schools in North Carolina, importantly the location. Created using a table maker: https://nces.ed.gov/ccd/elsi/tableGenerator.aspx
	* stratio.csv - File taken from the National Center for Education Statistics, contains school names and student teacher ratios. 
	* acctsumm15.csv - File Taken from North Carolina's Accountability Report section, contains the percent passing in three tests, as well as location information.  http://www.ncpublicschools.org/docs/accountability/reporting/acctsumm16.xlsx

* Graphs:
	* Biology, English, Math - Respectivly the school name plotted aganist it's percent passing grade level in the graph. 
	* BIOLOGY_AGAINST_LAT_LONG - Biology percent passing against the latitude & longitude of a school, no clear pattern here. 

* Maps: 
	* NC_Database Map - Map of schools from Purified.csv, colourized by biology percent passing. The darker the color, the higher the number. 

* ShapeFiles: 
	* NC_Map - Shape File of NC Map taken from: https://catalog.data.gov/dataset/tiger-line-shapefile-2013-state-north-carolina-current-county-subdivision-state-based 

* Machine Learning Experiments:
	* Machine Learning is complex, in an effort to learn from my failures, I'm archiving code that didn't work out very well. That's mostly what this section is made of. The literal machine learning experiments that are located in this project are focused on Polynomial regression in an attempt to predict test scores, as well as a gradient boosting machine in an attempt to classify schools based on test scores. 

