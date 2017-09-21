## SVM CLASSIFICATION ATTEMPT - FAILED, ALWAYS GUESSED 0 ### 
NC_database['Omega'] = list(zip(NC_database.LatitudePublicSchool201415, NC_database.LongitudePublicSchool201415))
save = np.array(list(NC_database.Biology.values), dtype=np.float)
values = NC_database.Biology >= 70 
negvalues = NC_database.Biology < 70

col_name = 'Biology'
NC_database.loc[values, col_name] = 1 
NC_database.loc[negvalues, col_name] = 0

y_list = NC_database['Biology'].values
print(y_list)
print(y_list.shape)
X = NC_database['Omega'].values
X = np.array(list(X), dtype=np.float)
this = np.array(list(NC_database.LatitudePublicSchool201415), dtype=np.float)
that = np.array(list(NC_database.LongitudePublicSchool201415), dtype=np.float)
omegasprem = svm.SVC()
omegasprem.fit(X, y_list)
print(omegasprem.predict(np.reshape((33, 111), (1,2))))

print(omegasprem.score(X, y_list))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(this, that, omegasprem.predict(X), 'd')
ax.scatter(this, that, NC_database.Biology)
plt.show()
