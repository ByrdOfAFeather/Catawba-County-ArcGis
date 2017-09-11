import matplotlib.pyplot as plt 
from sklearn.preprocessing import LabelEncoder
import numpy as np

def plot_schools(grade_dict, index_of_grade):
	labeler = LabelEncoder()
	labeler = labeler.fit(list(grade_dict.keys()))
	indexes = labeler.transform(grade_dict.keys())
	grade_values = []
	for items in grade_dict.values():
		grade_values.append(items.split(',')[index_of_grade])
	axes = plt.gca()
	plt.scatter(indexes, grade_values)
	plt.xticks(indexes, list(grade_dict.keys()), rotation=70, size=7, ha='right')
	axes.set_ylim([0, 100])
	for x in indexes:
		for y in grade_values: 
			x_list = []
			y = np.arange(0, float(y)+1)
			for values in y:
				x_list.append(x)
			plt.plot(x_list, y, '--', linewidth=.2, color='black')
	plt.show()
