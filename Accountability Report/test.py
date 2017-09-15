l1=range(2000) 
l2=range(1000,3000) 
d1 = {} 
l3 = []
for key in l1: 
	d1[key] = True # Value associated to key is not important and can be any value 
for key2 in l2: 
	if key2 in d1:
		print(d1)
		print(key2) 
		l3.append(key2) 
print("Intersection is : %s" % (l3,))