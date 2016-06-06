## Overview

This script simplifies the process of downloading high resolution DEMs, combining them into a raster dataset and clipping out
a shapefile that covers multiple tiles. The DEMs come [from the USGS](http://nationalmap.gov/3dep_prodserv.html) at 1/3 arc-second resolution, which is the highest resolution seamless DEM dataset of the entire coterminous US. This script also works for shapefiles whose extent only covers one tile.

## Usage

Run the elevation_reference.py file. The program will then query you for a path to the zipped shape file you need to get
the DEM for. The USGS tiles are aproximately 300 megabytes each, so depending on internet speed and extent of shapefile, they will take a
long time to download so be prepared to wait. Once the processed has finished the output image will be found in the C:\image folder in the ADF format.
This format is readable by both QGIS and ArcGIS

## Future Plans
Right now none of the files are deleted at the end of the program. This will be the next immediate step. Ultimately the program will use the GDAL
library and function on both Windows and Linux.
