### script landscape metrics v02 ###

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
fo = r"E:\github\GRASS-Landscape-Metrics\grassdb\RIO_CLARO"
os.chdir(fo)
print os.listdir(fo)

# import vector of land use
grass.run_command("v.in.ogr", input = "SP_3543907_USO.shp", output = "SP_3543907_USO2", \
    overwrite = True)

# define region and resolution
grass.run_command("g.region", flags = "ap", vector = "SP_3543907_USO2", res = 300)

# vector to raster
grass.run_command("v.to.rast", input = "SP_3543907_USO2", output = "SP_3543907_USO_raster", \
	type = "area", use = "cat", label_column = "CLASSE_USO", overwrite = True)

# select forest class
# with 0 #
grass.mapcalc("SP_3543907_USO_raster_forest = if(SP_3543907_USO_raster == 4, 1, 0)", overwrite = True)

# with null #
grass.mapcalc("SP_3543907_USO_raster_forest_null = if(SP_3543907_USO_raster == 4, 1, null())", overwrite = True)

# select no forest
grass.mapcalc("SP_3543907_USO_raster_noforest_null = if(SP_3543907_USO_raster == 4, null(), 1)", overwrite = True)


###----------------------------------------------------------------------------------------###

## 1. percentage of forest ##

# diameter = 3 pixels = diameter = 90 m
# moving window 
grass.run_command("r.neighbors", flags = "c", input = "SP_3543907_USO_raster_forest", \
	output = "SP_3543907_USO_raster_forest_avg_3_sel", method = "average", selection = "SP_3543907_USO_raster_forest", \
	size = "3", overwrite = True)

# percentage
grass.mapcalc("SP_3543907_USO_raster_forest_avg_3_sel_pct = SP_3543907_USO_raster_forest_avg_3_sel * 100", overwrite = True)

# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_avg_3_pct", \
	output = "SP_3543907_USO_raster_forest_avg_3_pct" + ".tif", format = "GTiff", overwrite = True)

###----------------------------------------------------------------------------------------###

## 2. structural connectivity ##

# clump
grass.run_command("r.clump", flags = "d", input = "SP_3543907_USO_raster_forest", \
	output = "SP_3543907_USO_raster_forest_clump", overwrite = True)

# forest clump 
ex = "SP_3543907_USO_raster_forest_clump_patch = SP_3543907_USO_raster_forest_clump * SP_3543907_USO_raster_forest"
grass.mapcalc(ex, overwrite = True)

# forest clump clean
ex = "SP_3543907_USO_raster_forest_clump_patch_clean = if(SP_3543907_USO_raster_forest_clump_patch > 0, \
SP_3543907_USO_raster_forest_clump_patch, null())"
grass.mapcalc(ex, overwrite = True)

# area
grass.run_command("r.stats", flags = "al", input = "SP_3543907_USO_raster_forest_clump_patch_clean", \
	output = "SP_3543907_USO_raster_forest_clump_patch_clean_area.txt", overwrite = True)

# replace space into equal
fi = open("SP_3543907_USO_raster_forest_clump_patch_clean_area.txt", "r")
fi_da = fi.read()
fi.close()

fi_da_e = fi_da.replace("  ", "=")
fi_da_e_s = fi_da_e.split("*")

fi = open("SP_3543907_USO_raster_forest_clump_patch_clean_area.txt", "w")
fi.write(fi_da_e_s[0])
fi.close()

# reclass
grass.run_command("r.reclass", input = "SP_3543907_USO_raster_forest_clump_patch_clean", \
	output = "SP_3543907_USO_raster_forest_clump_patch_clean_area_m2", \
	rules = "SP_3543907_USO_raster_forest_clump_patch_clean_area.txt", verbose = False, quiet = True, overwrite = True)

# area in hectares
ex = "SP_3543907_USO_raster_forest_clump_patch_clean_area_ha = SP_3543907_USO_raster_forest_clump_patch_clean_area_m2 * 0.0001"
grass.mapcalc(ex, overwrite = True)

# with 0 #
# area no habitat equal 0
ex = "SP_3543907_USO_raster_forest_clump_patch_clean_area_ha_0 = if(SP_3543907_USO_raster_forest == 0, 0, SP_3543907_USO_raster_forest_clump_patch_clean_area_ha)"
grass.mapcalc(ex, overwrite = True)

# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_clump_patch_clean_area_ha_0", \
	output = "SP_3543907_USO_raster_forest_clump_patch_clean_area_ha_0" + ".tif", format = "GTiff", overwrite = True)


# with null #
# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_clump_patch_clean_area_ha", \
	output = "SP_3543907_USO_raster_forest_clump_patch_clean_area_ha_null" + ".tif", format = "GTiff", overwrite = True)

###----------------------------------------------------------------------------------------###

## 3. functional connectivity

# diameter 3 pixels = gap of 60 m
# moving window 
grass.run_command("r.neighbors", input = "SP_3543907_USO_raster_forest", \
	output = "SP_3543907_USO_raster_forest_gap_60m", method = "maximum", size = "3", overwrite = True)

# select gap
ex = "SP_3543907_USO_raster_forest_gap_60m_temp = if(SP_3543907_USO_raster_forest_gap_60m == 0, null(), \
SP_3543907_USO_raster_forest_gap_60m)"
grass.mapcalc(ex, overwrite = True)

# clump
grass.run_command("r.clump", flags = "d", input = "SP_3543907_USO_raster_forest_gap_60m_temp", \
	output = "SP_3543907_USO_raster_forest_gap_60m_temp_clump", overwrite = True)

# forest clump
ex = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch = SP_3543907_USO_raster_forest_gap_60m_temp_clump * SP_3543907_USO_raster_forest"
grass.mapcalc(ex, overwrite = True)

# forest clump clean
ex = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean = if(SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch > 0, \
SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch, null())"
grass.mapcalc(ex, overwrite = True)

# area
grass.run_command("r.stats", flags = "al", input = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean", \
	output = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area.txt", overwrite = True)

# replace space into equal
fi = open("SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area.txt", "r")
fi_da = fi.read()
fi.close()

fi_da_e = fi_da.replace("  ", "=")
fi_da_e_s = fi_da_e.split("*")

fi = open("SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area.txt", "w")
fi.write(fi_da_e_s[0])
fi.close()

# reclass
grass.run_command("r.reclass", input = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean", \
	output = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area_m2", \
	rules = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area.txt", verbose = False, quiet = True, overwrite = True)

# area in hectares
ex = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area_ha = SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area_m2 * 0.0001"
grass.mapcalc(ex, overwrite = True)

# with 0 #
# area no habitat equal 0
ex = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area_ha_0 = if(SP_3543907_USO_raster_forest == 0, 0, SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area)"
grass.mapcalc(ex, overwrite = True)

# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area_ha_0", \
	output = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area_ha_0" + ".tif", format = "GTiff", overwrite = True)


# with null #
# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area_ha", \
	output = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area_ha_null" + ".tif", format = "GTiff", overwrite = True)


# emma #
# moving window 
grass.run_command("r.neighbors", flags = "c", input = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area_ha", \
	output = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area_ha_gap_60m", method = "maximum", size = "3", overwrite = True)

grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area_ha_gap_60m", \
	output = "SP_3543907_USO_raster_forest_gap_60m_temp_clump_patch_clean_area_ha_gap_60m_null" + ".tif", format = "GTiff", overwrite = True)

###----------------------------------------------------------------------------------------###

## 4. core

## 4.1 core area
# diameter 3 pixels = edge of 30 m
# moving window 
grass.run_command("r.neighbors", input = "SP_3543907_USO_raster_forest", \
	output = "SP_3543907_USO_raster_forest_core_30m", method = "minimum", size = "3", overwrite = True)

# clump
grass.run_command("r.clump", flags = "d", input = "SP_3543907_USO_raster_forest_core_30m", \
	output = "SP_3543907_USO_raster_forest_core_30m_clump", overwrite = True)

# forest clump
ex = "SP_3543907_USO_raster_forest_core_30m_clump_patch = SP_3543907_USO_raster_forest_core_30m_clump * SP_3543907_USO_raster_forest_core_30m"
grass.mapcalc(ex, overwrite = True)

# forest clump clean
ex = "SP_3543907_USO_raster_forest_core_30m_clump_patch_clean = if(SP_3543907_USO_raster_forest_core_30m_clump_patch > 0, \
SP_3543907_USO_raster_forest_core_30m_clump_patch, null())"
grass.mapcalc(ex, overwrite = True)

# area
grass.run_command("r.stats", flags = "al", input = "SP_3543907_USO_raster_forest_core_30m_clump_patch_clean", \
	output = "SP_3543907_USO_raster_forest_core_30m_clump_patch_clean_area.txt", overwrite = True)

# replace space into equal
fi = open("SP_3543907_USO_raster_forest_core_30m_clump_patch_clean_area.txt", "r")
fi_da = fi.read()
fi.close()

fi_da_e = fi_da.replace("  ", "=")
fi_da_e_s = fi_da_e.split("*")

fi = open("SP_3543907_USO_raster_forest_core_30m_clump_patch_clean_area.txt", "w")
fi.write(fi_da_e_s[0])
fi.close()

# reclass
grass.run_command("r.reclass", input = "SP_3543907_USO_raster_forest_core_30m_clump_patch_clean", \
	output = "SP_3543907_USO_raster_forest_core_30m_clump_patch_clean_area_m2", \
	rules = "SP_3543907_USO_raster_forest_core_30m_clump_patch_clean_area.txt", verbose = False, quiet = True, overwrite = True)

# area in hectares
ex = "SP_3543907_USO_raster_forest_core_30m_clump_patch_clean_area_ha = SP_3543907_USO_raster_forest_core_30m_clump_patch_clean_area_m2 * 0.0001"
grass.mapcalc(ex, overwrite = True)

# with 0 #
ex = "SP_3543907_USO_raster_forest_core_30m_clump_patch_clean_area_ha_0 = if(SP_3543907_USO_raster_forest_core_30m == 0, 0, SP_3543907_USO_raster_forest_core_30m_clump_patch_clean_area_ha)"
grass.mapcalc(ex, overwrite = True)

# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_core_30m_clump_patch_clean_area_ha_0", \
	output = "SP_3543907_USO_raster_forest_core_30m_clump_patch_clean_area_ha_0" + ".tif", format = "GTiff", overwrite = True)


# with null #
# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_core_30m_clump_patch_clean_area_ha", \
	output = "SP_3543907_USO_raster_forest_core_30m_clump_patch_clean_area_ha_null" + ".tif", format = "GTiff", overwrite = True)


## 4.2 core percentage
# diameter = 3 pixels = 90 m
# moving window 
grass.run_command("r.neighbors", flags = "c", input = "SP_3543907_USO_raster_forest_core_30m", \
	output = "SP_3543907_USO_raster_forest_core_30m_avg_3", selection = "SP_3543907_USO_raster_forest_core_30m", \
	method = "average", size = "3", overwrite = True)

# percentage
grass.mapcalc("SP_3543907_USO_raster_forest_core_30m_avg_3_pct = SP_3543907_USO_raster_forest_core_30m_avg_3 * 100", overwrite = True)

# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_core_30m_avg_3_pct", \
	output = "SP_3543907_USO_raster_forest_core_30m_avg_3_pct" + ".tif", format = "GTiff", overwrite = True)

###----------------------------------------------------------------------------------------###

## 5. edge

## 5.1 edge area
# edge 30 m
ex = "SP_3543907_USO_raster_forest_edge_30m = SP_3543907_USO_raster_forest - SP_3543907_USO_raster_forest_core_30m"
grass.mapcalc(ex, overwrite = True)

# clump
grass.run_command("r.clump", flags = "d", input = "SP_3543907_USO_raster_forest_edge_30m", \
	output = "SP_3543907_USO_raster_forest_edge_30m_clump", overwrite = True)

# forest clump
ex = "SP_3543907_USO_raster_forest_edge_30m_clump_patch = SP_3543907_USO_raster_forest_edge_30m_clump * SP_3543907_USO_raster_forest_edge_30m"
grass.mapcalc(ex, overwrite = True)

# forest clump clean
ex = "SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean = if(SP_3543907_USO_raster_forest_edge_30m_clump_patch > 0, \
SP_3543907_USO_raster_forest_edge_30m_clump_patch, null())"
grass.mapcalc(ex, overwrite = True)

# area
grass.run_command("r.stats", flags = "al", input = "SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean", \
	output = "SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean_area.txt", overwrite = True)

# replace space into equal
fi = open("SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean_area.txt", "r")
fi_da = fi.read()
fi.close()

fi_da_e = fi_da.replace("  ", "=")
fi_da_e_s = fi_da_e.split("*")

fi = open("SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean_area.txt", "w")
fi.write(fi_da_e_s[0])
fi.close()

# reclass
grass.run_command("r.reclass", input = "SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean", \
	output = "SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean_area_m2", \
	rules = "SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean_area.txt", verbose = False, quiet = True, overwrite = True)

# area in hectares
ex = "SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean_area_ha = SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean_area_m2 * 0.0001"
grass.mapcalc(ex, overwrite = True)


# with 0 #
ex = "SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean_area_ha_0 = if(SP_3543907_USO_raster_forest_edge_30m == 0, 0, SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean_area_ha)"
grass.mapcalc(ex, overwrite = True)

# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean_area_ha_0", \
	output = "SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean_area_ha_0" + ".tif", format = "GTiff", overwrite = True)


# with null #
# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean_area_ha", \
	output = "SP_3543907_USO_raster_forest_edge_30m_clump_patch_clean_area_ha_null" + ".tif", format = "GTiff", overwrite = True)


## 5.2 edge percentage
# diameter = 3 pixels = 90 m
# moving window 
grass.run_command("r.neighbors", flags = "c", input = "SP_3543907_USO_raster_forest_edge_30m", \
	output = "SP_3543907_USO_raster_forest_edge_30m_avg_3", selection = "SP_3543907_USO_raster_forest_edge_30m", \
	method = "average", size = "3", overwrite = True)

# percentage
grass.mapcalc("SP_3543907_USO_raster_forest_edge_30m_avg_3_pct = SP_3543907_USO_raster_forest_edge_30m_avg_3 * 100", overwrite = True)

# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_edge_30m_avg_3_pct", \
	output = "SP_3543907_USO_raster_forest_edge_30m_avg_3_pct" + ".tif", format = "GTiff", overwrite = True)


###----------------------------------------------------------------------------------------###

# 6. distance from edge
# edge null
ex = "SP_3543907_USO_raster_forest_edge_30m_null = if(SP_3543907_USO_raster_forest_edge_30m > 0, 1, null())"
grass.mapcalc(ex, overwrite = True)

# forest edge distance
grass.run_command("r.grow.distance", input = "SP_3543907_USO_raster_forest_edge_30m_null", \
	distance = "SP_3543907_USO_raster_forest_edge_30m_null_distance", overwrite = True)

# distance outside forest
ex = "SP_3543907_USO_raster_forest_edge_30m_null_distance_outside_forest = SP_3543907_USO_raster_forest_edge_30m_null_distance * SP_3543907_USO_raster_noforest_null"
grass.mapcalc(ex, overwrite = True)

# distance inside forest
ex = "SP_3543907_USO_raster_forest_edge_30m_null_distance_inside_forest = SP_3543907_USO_raster_forest_edge_30m_null_distance * SP_3543907_USO_raster_forest_null"
grass.mapcalc(ex, overwrite = True)

# negative distance inside forest
ex = "SP_3543907_USO_raster_forest_edge_30m_null_distance_inside_forest_neg = if(SP_3543907_USO_raster_forest_edge_30m_null_distance_inside_forest > 0, \
SP_3543907_USO_raster_forest_edge_30m_null_distance_inside_forest * -1, 0)"
grass.mapcalc(ex, overwrite = True)

# composite raster distance
grass.run_command("r.patch", input = "SP_3543907_USO_raster_forest_edge_30m_null_distance_inside_forest_neg,\
	SP_3543907_USO_raster_forest_edge_30m_null_distance_outside_forest", \
	output = "SP_3543907_USO_raster_forest_edge_30m_null_distance_edge")

# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_edge_30m_null_distance_edge", \
	output = "SP_3543907_USO_raster_forest_edge_30m_null_distance_edge" + ".tif", format = "GTiff", overwrite = True)



###----------------------------------------------------------------------------------------###

# 7. diversity

# diversity
# grass.run_command("r.diversity", input = "SP_3543907_USO_raster", prefix = "diversity", \
# 	size = 3, alpha = .5, overwrite = True)

# # export
# li = grass.list_grouped("rast", pattern = "diversity*")["PERMANENT"]
# print li

# for i in li:
#   grass.run_command("r.out.gdal", flags = "c", input = i, output = i + ".tif", format = "GTiff", overwrite = True)

###----------------------------------------------------------------------------------------###


# rlisetup
grass.run_command("g.gui.rlisetup")

# name: rio_claro
# raster: SP_3543907_USO_raster_forest_null
# sampling: whole map
# moving window
# method: keyboard
# type: rectangle
# size: 3 x 3


## indices based on patch number:
# calculates patch density index on a raster map, using a 4 neighbour algorithm
grass.run_command("r.li.patchdensity", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_patchdensity", conf = "rio_claro_cicle90m", overwrite = True)
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_patchdensity", \
	output = "SP_3543907_USO_raster_forest_null_patchdensity" + ".tif", format = "GTiff", overwrite = True)

# calculates patch number index on a raster map, using a 4 neighbour algorithm
grass.run_command("r.li.patchnum", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_patchnum", conf = "rio_claro", overwrite = True)
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_patchnum", \
	output = "SP_3543907_USO_raster_forest_null_patchnum" + ".tif", format = "GTiff", overwrite = True)


## indices based on patch dimension:
# calculates mean patch size index on a raster map, using a 4 neighbour algorithm
grass.run_command("r.li.mps", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_mps", conf = "rio_claro", overwrite = True)
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_mps", \
	output = "SP_3543907_USO_raster_forest_null_mps" + ".tif", format = "GTiff", overwrite = True)

# calculates coefficient of variation of patch area on a raster map
grass.run_command("r.li.padcv", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_padcv", conf = "rio_claro", overwrite = True)
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_padcv", \
	output = "SP_3543907_USO_raster_forest_null_padcv" + ".tif", format = "GTiff", overwrite = True)
 
# calculates range of patch area size on a raster map
grass.run_command("r.li.padrange", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_padrange", conf = "rio_claro", overwrite = True)
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_padrange", \
	output = "SP_3543907_USO_raster_forest_null_padrange" + ".tif", format = "GTiff", overwrite = True)

# calculates standard deviation of patch area a raster map
grass.run_command("r.li.padsd", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_padsd", conf = "rio_claro", overwrite = True)
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_padsd", \
	output = "SP_3543907_USO_raster_forest_null_padsd" + ".tif", format = "GTiff", overwrite = True)


## indices based on patch shape
# calculates shape index on a raster map
grass.run_command("r.li.shape", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_shape", conf = "rio_claro", overwrite = True)
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_shape", \
	output = "SP_3543907_USO_raster_forest_null_shape" + ".tif", format = "GTiff", overwrite = True)
 

## indices based on patch edge:
# calculates edge density index on a raster map, using a 4 neighbour algorithm
grass.run_command("r.li.edgedensity", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_edgedensity", conf = "rio_claro", overwrite = True)
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_edgedensity", \
	output = "SP_3543907_USO_raster_forest_null_edgedensity" + ".tif", format = "GTiff", overwrite = True)

grass.run_command("r.li.edgedensity", flags = "b", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_edgedensity_b", conf = "rio_claro", overwrite = True)
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_edgedensity_b", \
	output = "SP_3543907_USO_raster_forest_null_edgedensity_b" + ".tif", format = "GTiff", overwrite = True)

 
 ## indices based on patch attributes:
# calculates contrast Weighted Edge Density index on a raster map
#grass.run_command("r.li.cwed", input = "SP_3543907_USO_raster_forest_null", \
#	output = "SP_3543907_USO_raster_forest_null_cwed", conf = "rio_claro", overwrite = True)
 
# calculates mean pixel attribute index on a raster map
grass.run_command("r.li.mpa", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_mpa", conf = "rio_claro", overwrite = True)
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_mpa", \
	output = "SP_3543907_USO_raster_mpa" + ".tif", format = "GTiff", overwrite = True)


## diversity indices:
# calculates dominance diversity index on a raster map
grass.run_command("r.li.dominance", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_dominance", conf = "rio_claro", overwrite = True)
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_dominance", \
	output = "SP_3543907_USO_raster_dominance" + ".tif", format = "GTiff", overwrite = True)

# calculates Pielou eveness index on a raster map
grass.run_command("r.li.pielou", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_pielou", conf = "rio_claro", overwrite = True) 
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_pielou", \
	output = "SP_3543907_USO_raster_pielou" + ".tif", format = "GTiff", overwrite = True)

# calculates Renyi entropy on a raster map
grass.run_command("r.li.renyi", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_renyi_a05", alpha = "0.5",conf = "rio_claro", overwrite = True) 
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_renyi_a05", \
	output = "SP_3543907_USO_raster_renyi_a05" + ".tif", format = "GTiff", overwrite = True)

# calculates richness diversity index on a raster map
grass.run_command("r.li.richness", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_richness", conf = "rio_claro", overwrite = True) 
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_richness", \
	output = "SP_3543907_USO_raster_richness" + ".tif", format = "GTiff", overwrite = True)

# calculates Shannon diversity index on a raster map
grass.run_command("r.li.shannon", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_shannon", conf = "rio_claro", overwrite = True) 
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_shannon", \
	output = "SP_3543907_USO_raster_shannon" + ".tif", format = "GTiff", overwrite = True)

# calculates Simpson diversity index on a raster map
grass.run_command("r.li.simpson", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_simpson", conf = "rio_claro", overwrite = True) 
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_simpson", \
	output = "SP_3543907_USO_raster_simpson" + ".tif", format = "GTiff", overwrite = True)


###----------------------------------------------------------------------------------------###

# clean
grass.run_command("g.remove", flags = "f", type = "raster", pattern = "*raster*")

###----------------------------------------------------------------------------------------###
