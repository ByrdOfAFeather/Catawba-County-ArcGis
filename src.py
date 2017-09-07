from arcpy import Buffer_analysis, Intersect_analysis
from arcpy.da import SearchCursor


# C:\Users\ADongre\Desktop\Database & Geowords\matthew_a_byrd.gdb
def buffer_creation():
	Buffer_analysis('C:\Users\ADongre\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\Arcview.sde\sde.GIS.SCHOOLS',
		'C:\Users\ADongre\Desktop\Database & Geowords\matthew_a_byrd.gdb\schoolbufffix', 2640)
def Intersect_creation():
	Intersect_analysis(['C:\Users\ADongre\Desktop\Database & Geowords\matthew_a_byrd.gdb\schoolbufffix', 'C:\Users\ADongre\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\Arcview.sde\sde.GIS.CADASTRAL\sde.GIS.Parcels'], 'C:\Users\ADongre\Desktop\Database & Geowords\matthew_a_byrd.gdb\schoolbuffwparcel', )

array = []
for row in SearchCursor('C:\Users\ADongre\Desktop\Database & Geowords\matthew_a_byrd.gdb\schoolbuffwparcel', ['PIN']):
	temp = row[0]
	array.append(str(temp))
print(array)
