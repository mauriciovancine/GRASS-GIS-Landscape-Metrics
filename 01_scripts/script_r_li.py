#' ---
#' title: metricas de paisagem com r.li
#' author: mauricio vancine
#' date: 15-01-2020
#' ---

# informacoes -------------------------------------------------------------
# modulo
# https://gs.osgeo.org/grass78/manuals/r.li.html

# criar banco de dados grass gis ------------------------------------------
# directory
cd /home/mude/data/github/landscape-metrics-grass-gis/02_dados

# grassdb
mkdir grassdb
cd grassdb
grass -c epsg:31983 -e /home/mude/data/github/landscape-metrics-grass-gis/02_dados/grassdb/utm23s_sirgas2000

# initiate grass
grass /home/mude/data/github/landscape-metrics-grass-gis/02_dados/grassdb/utm23s_sirgas2000/PERMANENT --exec

# python ------------------------------------------------------------------
python

# bibliotecas -------------------------------------------------------------
import os
import grass.script as gs

# iniciar manjeador de camdas e visualizador
gs.run_command("g.gui")

# importar os dados -------------------------------------------------------
# diretorio
path = r"/home/mude/data/github/landscape-metrics-grass-gis/02_dados"

os.chdir(path)
os.listdir(path)

# import vector
gs.run_command("v.in.ogr", input = "SP_3543907_USO.shp", output = "uso")

# definir a region
gs.run_command("g.region", flags = "ap", vector = "uso")

# rasterizar
gs.run_command("v.to.rast", input = "uso", output = "uso", type = "area", use = "cat", label_column = "CLASSE_USO", overwrite = True)

# binarizar
gs.mapcalc("forest = if(uso == 4, 1, null())", overwrite = True)

# definir a region
gs.run_command("g.region", flags = "ap", raster = "forest", res = 90)

# rlisetup ----------------------------------------------------------------
gs.run_command("g.gui.rlisetup")

# name: rio_claro
# raster: forest
# sampling: whole map
# moving window
# method: keyboard
# type: rectangle
# size: 3 x 3

## indices based on patch number:

# calculates patch density index on a raster map, using a 4 neighbour algorithm
gs.run_command("r.li.patchdensity", input = "forest", output = "forest_patchdensity", conf = "rio_claro", overwrite = True)
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_patchdensity", \
	output = "SP_3543907_USO_raster_forest_null_patchdensity" + ".tif", format = "GTiff", overwrite = True)

# calculates patch number index on a raster map, using a 4 neighbour algorithm
gs.run_command("r.li.patchnum", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_patchnum", conf = "rio_claro", overwrite = True)
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_patchnum", \
	output = "SP_3543907_USO_raster_forest_null_patchnum" + ".tif", format = "GTiff", overwrite = True)


## indices based on patch dimension:
# calculates mean patch size index on a raster map, using a 4 neighbour algorithm
gs.run_command("r.li.mps", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_mps", conf = "rio_claro", overwrite = True)
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_mps", \
	output = "SP_3543907_USO_raster_forest_null_mps" + ".tif", format = "GTiff", overwrite = True)

# calculates coefficient of variation of patch area on a raster map
gs.run_command("r.li.padcv", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_padcv", conf = "rio_claro", overwrite = True)
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_padcv", \
	output = "SP_3543907_USO_raster_forest_null_padcv" + ".tif", format = "GTiff", overwrite = True)
 
# calculates range of patch area size on a raster map
gs.run_command("r.li.padrange", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_padrange", conf = "rio_claro", overwrite = True)
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_padrange", \
	output = "SP_3543907_USO_raster_forest_null_padrange" + ".tif", format = "GTiff", overwrite = True)

# calculates standard deviation of patch area a raster map
gs.run_command("r.li.padsd", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_padsd", conf = "rio_claro", overwrite = True)
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_padsd", \
	output = "SP_3543907_USO_raster_forest_null_padsd" + ".tif", format = "GTiff", overwrite = True)


## indices based on patch shape
# calculates shape index on a raster map
gs.run_command("r.li.shape", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_shape", conf = "rio_claro", overwrite = True)
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_shape", \
	output = "SP_3543907_USO_raster_forest_null_shape" + ".tif", format = "GTiff", overwrite = True)
 

## indices based on patch edge:
# calculates edge density index on a raster map, using a 4 neighbour algorithm
gs.run_command("r.li.edgedensity", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_edgedensity", conf = "rio_claro", overwrite = True)
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_edgedensity", \
	output = "SP_3543907_USO_raster_forest_null_edgedensity" + ".tif", format = "GTiff", overwrite = True)

gs.run_command("r.li.edgedensity", flags = "b", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_edgedensity_b", conf = "rio_claro", overwrite = True)
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_null_edgedensity_b", \
	output = "SP_3543907_USO_raster_forest_null_edgedensity_b" + ".tif", format = "GTiff", overwrite = True)

 
 ## indices based on patch attributes:
# calculates contrast Weighted Edge Density index on a raster map
#gs.run_command("r.li.cwed", input = "SP_3543907_USO_raster_forest_null", \
#	output = "SP_3543907_USO_raster_forest_null_cwed", conf = "rio_claro", overwrite = True)
 
# calculates mean pixel attribute index on a raster map
gs.run_command("r.li.mpa", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_mpa", conf = "rio_claro", overwrite = True)
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_mpa", \
	output = "SP_3543907_USO_raster_mpa" + ".tif", format = "GTiff", overwrite = True)


## diversity indices:
# calculates dominance diversity index on a raster map
gs.run_command("r.li.dominance", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_dominance", conf = "rio_claro", overwrite = True)
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_dominance", \
	output = "SP_3543907_USO_raster_dominance" + ".tif", format = "GTiff", overwrite = True)

# calculates Pielou eveness index on a raster map
gs.run_command("r.li.pielou", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_pielou", conf = "rio_claro", overwrite = True) 
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_pielou", \
	output = "SP_3543907_USO_raster_pielou" + ".tif", format = "GTiff", overwrite = True)

# calculates Renyi entropy on a raster map
gs.run_command("r.li.renyi", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_renyi_a05", alpha = "0.5",conf = "rio_claro", overwrite = True) 
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_renyi_a05", \
	output = "SP_3543907_USO_raster_renyi_a05" + ".tif", format = "GTiff", overwrite = True)

# calculates richness diversity index on a raster map
gs.run_command("r.li.richness", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_richness", conf = "rio_claro", overwrite = True) 
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_richness", \
	output = "SP_3543907_USO_raster_richness" + ".tif", format = "GTiff", overwrite = True)

# calculates Shannon diversity index on a raster map
gs.run_command("r.li.shannon", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_shannon", conf = "rio_claro", overwrite = True) 
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_shannon", \
	output = "SP_3543907_USO_raster_shannon" + ".tif", format = "GTiff", overwrite = True)

# calculates Simpson diversity index on a raster map
gs.run_command("r.li.simpson", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_simpson", conf = "rio_claro", overwrite = True) 
gs.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_simpson", \
	output = "SP_3543907_USO_raster_simpson" + ".tif", format = "GTiff", overwrite = True)
