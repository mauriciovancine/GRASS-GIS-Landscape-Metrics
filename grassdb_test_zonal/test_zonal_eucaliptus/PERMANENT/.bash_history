exit
r.info map=BR_2001_euca_9@PERMANENT
v.db.dropcolumn map=mun_teste_wgs84@PERMANENT columns=dist
r.info map=BR_2001_euca_9@PERMANENT
r.category map=BR_2001_euca_9
r.stats -c input=BR_2001_euca_9
r.info map=BR_2001_euca_9@PERMANENT
r.colors map=BR_2001_euca_9@PERMANENT rules=/home/leecb/Github/GRASS-GIS-Landscape-Metrics/grassdb_test_zonal/test_zonal_eucaliptus/PERMANENT/.tmp/leecb/6630.0
r.info map=temp_rast@PERMANENT
r.info map=MASK@PERMANENT
v.db.dropcolumn map=mun_teste_wgs84 col=proportion_euca
r.info map=MASK@PERMANENT
g.region -p
v.colors map=mun_teste_wgs84@PERMANENT use=z column=proportion_euca_2001 color=byr
r.info map=MASK@PERMANENT
v.db.dropcolumn map=mun_teste_wgs84 col=proportion_euca
v.db.dropcolumn map=mun_teste_wgs84 col=proportion_euca_2001
v.out.ogr --overwrite input=mun_teste_wgs84@PERMANENT output=teste format=ESRI_Shapefile
v.db.dropcolumn map=mun_teste_wgs84 col=proportion_euca_2001
v.info map=mun_teste_wgs84@PERMANENT
v.db.dropcolumn map=mun_teste_wgs84@PERMANENT columns=p_eu_2001
v.db.dropcolumn map=mun_teste_wgs84@PERMANENT columns=np_2001
g.list rast
g.list vect
exit
