NC_database = setup_NC_DATAFRAME(overall_grades, overall_dataframe)
NC_database['Omega'] = list(zip(NC_database.LatitudePublicSchool201415, NC_database.LongitudePublicSchool201415))
map = Basemap(llcrnrlon=-88.007771,llcrnrlat=28.8933355,urcrnrlon=-72.758747,urcrnrlat=39.793274,
        projection='lcc',lat_0=34.741513, lon_0=-78.534434)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.add_collection3d(map.drawcoastlines(linewidth=0.25))
ax.add_collection3d(map.drawstates())
list_of_points = list(map(list(NC_database.LongitudePublicSchool201415.astype(float)), list(NC_database.LatitudePublicSchool201415.astype(float))))
print(NC_database.LongitudePublicSchool201415.astype(float))
print(NC_database.LongitudePublicSchool201415.astype(float).shape)
r_list_of_points = []
for values in list_of_points:
	for values in values:
		r_list_of_points.append(values)
list_of_points = r_list_of_points
print(list_of_points)

print(len(list_of_points))

long_list = []
for index in range(1, len(list_of_points), 2):
	long_list.append(list_of_points[index])
lat_list = []
for index in range(0, len(list_of_points), 2):
	lat_list.append(list_of_points[index])

print(len(lat_list))
print(len(long_list))
print(NC_database.Biology.astype(float).shape)

ax.scatter(long_list, lat_list, NC_database.Biology.astype(float))
map.scatter(lat_list, long_list)


plt.show()