### script split distance ###

# Maurício Humberto Vancine - mauricio.vancine@gmail.com
# 23/12/2017

###----------------------------------------------------------------------------------------###

# start python
python 

# import modules
import os
import grass.script as grass

###----------------------------------------------------------------------------------------###

# directory
fo = r"E:\github\GRASS-Landscape-Metrics\grassdb_sd"
os.chdir(fo)
print os.listdir(fo)

###----------------------------------------------------------------------------------------###

# import
grass.run_command("v.in.ogr", input = "limite_rio_claro_ibge2015_albers_sad69.shp", output = "limit_rc", \
    overwrite = True)

grass.run_command("r.in.gdal", input = "simple_river_rc_albers_sad69.tif", output = "simple_river", \
    overwrite = True)

grass.run_command("r.in.gdal", input = "patch_rc_albers_sad69.tif", output = "patch", overwrite = True)

grass.run_command("r.in.gdal", input = "patch_rc_id_albers_sad69.tif", output = "patch_id", overwrite = True)

# region
grass.run_command("g.region", flags = "ap", vector = "limit_rc", res = "30")

# slipt distance:
grass.run_command("r.grow.distance", input = "simple_river", distance = "simple_river_dist", overwrite = True)

grass.mapcalc("simple_river_dist_patch = if(patch > 0, simple_river_dist, null())", overwrite = True)

grass.run_command("r.stats.zonal", base = "patch_id", cover = "simple_river_dist_patch", \
	method = "min", output = "simple_river_dist_patch_min")

grass.mapcalc("split_distance = simple_river_dist_patch_min / patch", overwrite = True)

grass.mapcalc("split_distance_in = simple_river_dist_patch / patch", overwrite = True)

# Transform it into a function

#--------------------------------
# Function calculate_split_distance
def calculate_split_distance(water_map = '', patch_size_map = '', patch_id_map = '',
                             options = ['min_per_patch', 'per_pixel'], resolution = None):
    '''
    Function calculate_split_distance

    This function calculates metrics of habitat split distance per patch or per pixel.
    All non habitat cells are set to a NULL value of habitat split dstance. 
    Describe it better here.

    Parameters
    ----------
    water_map: string
        Name of the raster map of water bodies (e.g., rivers, lakes).
    patch_size_map: string
        Name of the raster map of patch size.
    patch_id_map: string
        Name of the raster map of patch ID (all the pixels of the same patch present the same
        identifying number).
    options: list with strings; {'min_per_patch', 'per_pixel'}
        Options to be calculated: 'min_per_patch' and 'per_pixel'. 
        The option 'min_per_patch' calculates, for each habitat patch, the habitat split distance as:
        min(dist_pixels_of_the_patch_to_nearest_river)/patch_area. The same value is set to all 
        cells of the same patch.
        The option 'per_pixel' calculates the habitat split distance as:
        dist_each_pixel_to_nearest_river/patch_area. Therefore pixels of the same patch generally differ
        in their split distance value.
        *** Should we also include an r.stats.zonal for this per pixel map?
    resolution: integer or float; default is None
        Resolution to be considered when calculating split distance. If None (default), the resolution
        is the same of patch_size_map.

    Returns
    -------
    split_distance_min_per_patch: raster map within GRASS GIS
        A map of split distance per patch (see above). Generated only if 'min_per_patch' in included in the
        options.
    split_distance_per_pixel: raster map within GRASS GIS
        A map of split distance per patch (see above). Generated only if 'min_per_patch' in included in the
        options.
    *** Maybe it is a good idea to append a prefix in the beginning of the output map names, in case
    *** habitat split is calculated for different sets of maps/areas/cities...
    '''

    # Set working region
    if resolution is not None:
        # Define region based on resolution defined as input
        grass.run_command('g.region', flags = 'ap', raster = patch_size_map, res = resolution)
    else:
        # Define region based on the resolution of the patch size map
        grass.run_command('g.region', flags = 'ap', raster = patch_size_map)        

    # Calculate distance from rivers
    grass.run_command('r.grow.distance', input = water_map, distance = water_map+'_dist', overwrite = True)

    # Keep distance from rivers only within habitat patches
    grass.mapcalc(water_map+'_dist_patch = if('+patch_size_map+' > 0, '+water_map+'_dist, null())', 
                  overwrite = True)

    # If options include min_per_patch, calculate habitat split as:
    #   min(dist_pixels_of_the_patch_to_nearest_river)/patch_area
    if 'min_per_patch' in options:
        # Calculate distance from each patch to the nearest river
        grass.run_command('r.stats.zonal', base = patch_id_map, cover = water_map+'_dist_patch',
                          method = 'min', output = water_map+'_dist_patch_min')

        # Calculate split distance as the ratio between the above and patch area
        grass.mapcalc('split_distance_min_per_patch = '+water_map+'_dist_patch_min / '+patch_size_map, 
                      overwrite = True)

    # If options include per_pixel, calculate habitat split as:
    #   dist_pixel_to_nearest_river/patch_area
    if 'per_pixel':
        # Calculate split distance per pixel
        grass.mapcalc('split_distance_per_pixel = '+water_map+'_dist_patch / '+patch_size_map, 
                      overwrite = True)


# End of function

# Test using the function
help(calculate_split_distance)

calculate_split_distance(water_map = 'simple_river', patch_size_map = 'patch', 
                         patch_id_map = 'patch_id', 
                         options=['min_per_patch', 'per_pixel'], 
                         resolution=None)


# units
grass.run_command("g.region", flags = "ap", vector = "limit_rc", res = "1000")
grass.run_command("v.mkgrid", flags = "h", map = "limit_rc_hex1000", overwrite = True)
grass.run_command("v.select", ainput = "limit_rc_hex1000", binput = "limit_rc", \
	output = "limit_rc_hex1000_overlap", operator = "overlap", overwrite = True)

grass.run_command("v.rast.stats", map = "limit_rc_hex1000_overlap", \
	raster = "split_distance", column_prefix = "sd_", method = "av,med,st")

grass.run_command("v.rast.stats", map = "limit_rc_hex1000_overlap", \
	raster = "split_distance_in", column_prefix = "sdin_", method = "av,med,st")


