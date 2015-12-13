
import arcpy
import os
from ftp_test import get_data
import zipfile
import sys

arcpy.env.overwriteOutput = 1

if arcpy.CheckExtension("Spatial") == "Available":

    arcpy.CheckOutExtension("Spatial")
else:
    arcpy.AddMessage("Unable to get spatial analyst extension")
    sys.exit(0)


# C:\Users\negra\PycharmProjects\Data_Utility\data\random_counties.zip
print "Welcome to Zack's Data Utility program!\nThis program will convert your shapefiles into high resolution DEMs\n" \
      "Warning: There may be errors if your shapefile is not in the WGS84 data\n" \
      "The output after the program has run will be in the C:\ drive with the filename image\n"
shapefile = raw_input("Enter the path of the zipped shapefile\n")
zipped_shape = open(shapefile, 'rb')
z = zipfile.ZipFile(zipped_shape)
for name in z.namelist():
    if name[-3:] == 'shp':
        shapefile = name
    z.extract(name, "data")

shapefile = 'data/' + shapefile

"""
This block creates variable that are linked to shapefile paths
and establishes other necessary global variables. I am using Georgia
as a test shapefile but it will eventually be a parameter
"""

box_list = []
boxes = 'data/NED_Reference/ned_13arcsec_g.shp'
nameField = "FILE_ID"

# C:\Users\negra\PycharmProjects\Data_Utility\data\random_counties.zip
"""
This block creates a File Geodatabase and a raster dataset inside the
geodatabase. The try/accept clauses are because the program will throw an
exception if the geodatbase ro the raster dataset already exists
the exceptions need to be changed to be more specific
"""
try:
    arcpy.management.CreateFileGDB(os.path.dirname(os.path.abspath(__file__)), "data/datastore")
except:
    pass

try:
    arcpy.CreateMosaicDataset_management("data/datastore.gdb", "mosaick_dataset", 'data/NED_Reference/ned_13arcsec_g.shp' )
except:
    pass
"""
This creates feature layers using the variables that point
to the shapefiles. The feature layer is given a name that
can be referenced later on. A feature layer is required to be
created in order to work with the data in the shapefile
"""

arcpy.MakeFeatureLayer_management(boxes, "boxes")
arcpy.MakeFeatureLayer_management(shapefile, "shapefile")

# This selects the tile reference from the tile reference grid that intersects with the shape file
arcpy.SelectLayerByLocation_management("boxes", "INTERSECT", "shapefile")

# C:\Users\negra\PycharmProjects\Data_Utility\data\random_counties.zip

"""
This iterates through the selected tiles of the boxes feature
layer and extracts gets their file id which will be used as a
parameter in the URL to download the tile file
"""
with arcpy.da.SearchCursor("boxes", (nameField,)) as cursor:
        for row in cursor:
            box_list.append(row[0])

"""
This iterates through the list of tiles and
downloads each one using the get_data function
"""
get_data(box_list[0])
for box in box_list:
    get_data(box)

"""
This creates the file paths to the rastesr that have been
downloaded and puts them in the list raster_list
"""
raster_list = []
for index in box_list:
    name = 'img' + index + '_13.img'
    raster_list.append('data/rasters/' + name)


"This unzips the zipfiles that the rasters come in and extracts .img file"
for index in box_list:
    zipped_file = open(index + '.zip', 'rb')
    z = zipfile.ZipFile(zipped_file)
    for name in z.namelist():
        if name == 'img' + index + '_13.img':
            raster_list.append('data/rasters/' + name)
            z.extract(name, "data/rasters")


arcpy.management.AddRastersToMosaicDataset("data/datastore.gdb/mosaick_dataset", "Raster Dataset", raster_list)


arcpy.MakeFeatureLayer_management(shapefile, 'currentMask')
ExRas = arcpy.sa.ExtractByMask("data/datastore.gdb/mosaick_dataset", 'currentMask')
# ExRas.save("C:\\Users\negra\\PycharmProjects\\Data_Utility\\output_image")
ExRas.save("C:\\image")
arcpy.CheckInExtension("Spatial")

