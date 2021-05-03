# initiate python
python

# import libraries
import os
import grass.script as grass

# define function for extract multi points
def extract_multi_points(input, raster):
    # input = points
    # raster = raster
    
    # name of colums
    colunm = str(raster)
    
    # add column 
    grass.run_command("g.message", message = "--Add column--")
    grass.run_command("v.db.addcolumn", map = input, columns = colunm + " double precision", quiet = True)
    
    # extract values
    grass.run_command("g.message", message = "--Extracting values--")
    grass.run_command("v.what.rast", map = input, raster = raster, column = colunm, quiet = True)

# list rasters
ra = grass.list_grouped("rast", pattern = "*")["PERMANENT"]
print ra

# extract
for i in ra:
    extract_multi_points(input = "points", raster = i)

