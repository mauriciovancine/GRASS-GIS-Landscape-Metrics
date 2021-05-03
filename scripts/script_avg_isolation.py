## isolation
# python
python

# modules
import os, fnmatch
import grass.script as grass

# diretory
folder_path = r"D:\_data\Vanessa\_data_base\pontos"

# change to this folder
os.chdir(folder_path) 
print os.listdir(folder_path)

files = fnmatch.filter(os.listdir("."), "*.shp")
print files

# import raster
grass.run_command("r.in.gdal", input = "prodes_20131_albers_tif_bin_patch_clump_mata_limpa_AreaHA_eucdist", \
         output = ras)

shape = "point.shp" # EU EVITARIA CHAMAR UM OBJETO DE map POIS ESSE EH O NOME DE UM FUNCAO EM PYTHON

## average isolation
# import
name = shape.replace(".shp", "")
grass.run_command("v.in.ogr", input = shape, output = name, overwrite = True)

# Declare the function
def calculate_avg_isolation(in_shapefile_map, rast_dist_map, buffer_size = 1000, n_points = 1000):
    
    # name of output maps
    out_buffer_map = in_shapefile_map + "_buf" + str(buffer_size)
    out_points_map = in_shapefile_map + "_buf" + str(buffer_size) + "_rp" + str(n_points)
  
    # buffer
    grass.run_command("g.message", message = "Creating buffer of size " + str(buffer_size) + " m")
    grass.run_command("v.buffer", input = in_shapefile_map, output = out_buffer_map, distance = buffer_size, overwrite = True)
  
    # region
    grass.run_command("g.message", message = "Defining region of interest")
    grass.run_command("g.region", flags = "p", vector = out_buffer_map) 
  
    # create "n_points" points
    grass.run_command("g.message", message = "Generating " + str(n_points) + " inside buffer")
    grass.run_command("v.random", restrict = out_buffer_map, output = out_points_map, n = n_points, overwrite = True)
  
    # create attribute table
    grass.run_command("v.db.addtable", map = out_points_map)
  
    # add column 
    grass.run_command("v.db.addcolumn", map = out_points_map, columns = "dist double precision")
  
    # extract values
    grass.run_command("g.message", message = "Extracting distance values")
    grass.run_command("v.what.rast", map = out_points_map, raster = rast_dist_map, column = "dist")
  
    # export points
    grass.run_command("g.message", message = "Exporting points as a shapefile")
    #grass.run_command("v.out.ogr", input = out_points_map, type = "point", output = out_points_map + ".shp", overwrite = True)
    grass.run_command("db.out.ogr", input = out_points_map, output = out_points_map + ".csv")
