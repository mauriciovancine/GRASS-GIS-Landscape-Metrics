### script edge distance ###

# Maurício Humberto Vancine - mauricio.vancine@gmail.com
# 06/10/2017

###----------------------------------------------------------------------------------------###

# start python
python 

# import modules
import os
import grass.script as grass

###----------------------------------------------------------------------------------------###

# directory
fo = r"E:\github_mauriciovancine\GRASS-GIS-Landscape-Metrics\grassdb_edge"
os.chdir(fo)
print os.listdir(fo)

###----------------------------------------------------------------------------------------###

# import
grass.run_command("v.in.ogr", input = "map_Unesp.shp", output = "map_Unesp")

# define region and resolution
grass.run_command("g.region", flags = "ap", vector = "map_Unesp", res = 5)

# vector to raster
grass.run_command("v.to.rast", input = "map_Unesp", output = "map_Unesp_raster", \
	type = "area", use = "attr", attribute_column = "class", overwrite = True)

# select forest
grass.mapcalc("map_Unesp_raster_forest_1_0 = if(map_Unesp_raster == 1, 1, 0)", overwrite = True)

###----------------------------------------------------------------------------------------###

# forest null
grass.mapcalc("map_Unesp_raster_forest_null = if(map_Unesp_raster_forest_1_0 == 1, 1, null())", overwrite = True)

# matrix null
grass.mapcalc("map_Unesp_raster_matrix_null = if(map_Unesp_raster_forest_1_0 == 1, null(), 1)", overwrite = True)

# forest distance
grass.run_command("r.grow.distance", input = "map_Unesp_raster_forest_null", \
	distance = "map_Unesp_raster_forest_null_distance", overwrite = True)

# matrix distance
grass.run_command("r.grow.distance", input = "map_Unesp_raster_matrix_null", \
	distance = "map_Unesp_raster_matrix_null_distance", overwrite = True)

# distance outside forest
ex = "map_Unesp_raster_forest_null_distance_outside_forest = map_Unesp_raster_forest_null_distance * map_Unesp_raster_matrix_null"
grass.mapcalc(ex, overwrite = True)

# distance inside forest
ex = "map_Unesp_raster_matrix_null_distance_inside_forest =  map_Unesp_raster_matrix_null_distance * map_Unesp_raster_forest_null * -1"
grass.mapcalc(ex, overwrite = True)

# composite raster distance
grass.run_command("r.patch", input = "map_Unesp_raster_forest_null_distance_outside_forest,\
	map_Unesp_raster_matrix_null_distance_inside_forest", \
	output = "map_Unesp_raster_distance_edge")

# export
grass.run_command("r.out.gdal", flags = "fc", input = "map_Unesp_raster_distance_edge", type = "Int32", \
	output = "map_Unesp_raster_distance_edge.tif", overwrite = True)

###----------------------------------------------------------------------------------------###