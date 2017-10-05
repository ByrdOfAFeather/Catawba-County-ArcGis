import matplotlib.pyplot as plt 
from sklearn.preprocessing import LabelEncoder
import numpy as np

def plot_schools(grade_dict, index_of_grade, yax, file_name=[]):
	'''Plots school encoded values as a function of the grades
	grade_dict = dictionary with school names and grades
	index_of_grade = index of grade - math, bio, english 
	yax = Name of the y-axes - math, bio, english
	file_name = the name of the file that the image is saved as (optional)'''
	fig = plt.figure(figsize=(16, 9))
	labeler = LabelEncoder()
	labeler = labeler.fit(list(grade_dict.keys()))
	indexes = labeler.transform(grade_dict.keys())
	grade_values = []
	for items in grade_dict.values():
		print("Finished here")
		grade_values.append(float(items.split(',')[index_of_grade]))
	axes = plt.gca()
	mean = sum(grade_values)/len(grade_values)
	plt.scatter(indexes, grade_values)
	plt.xticks(indexes, list(grade_dict.keys()), rotation=70, size=7, ha='right')
	plt.ylabel(yax)
	plt.xlabel('School Name')
	axes.set_ylim([0, 100])
	y = range(0, 100)
	for x in indexes:
		x_list = []
		for values in y:
			x_list.append(x)
		plt.plot(x_list, y, '--', linewidth=.2, color='black')
	
	plt.axhline(mean, 0, 32, label='Mean')
	plt.subplots_adjust(bottom=.30)
	plt.legend()
	print("Got here")
	if file_name:
		plt.savefig('Graphs/Biology/V1/' + file_name + '.png')
	plt.show()
