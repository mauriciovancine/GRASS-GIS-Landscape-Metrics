#' ---
#' title: metricas de paisagem com r.li
#' author: mauricio vancine
#' date: 15-01-2020
#' ---

# informacoes -------------------------------------------------------------

# artigo



# rlisetup
#grass.run_command("g.gui.rlisetup")

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
	output = "SP_3543907_USO_raster_forest_null_patchdensity", conf = "rio_claro", overwrite = True)
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
