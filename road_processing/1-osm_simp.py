# -*- coding: utf-8 -*-
import arcpy
import pandas as pd

arcpy.env.workspace = r'E:\\citydna\\TOD\\code\\data_review\\road\\road_processing\\osm_road_simp.gdb'
arcpy.env.overwriteOutput = True

# read in osm data of whole country
china_osm2021 = r'E:\\citydna\\TOD\\code\\data_review\\road\\raw_data\\osm2022-original\\gis_osm_roads_free_1.shp'
# read in 38 cities' boundary
clip_root = r'E:\\citydna\\TOD\\code\\data_review\\boundary_city_amap\\shp_data'
# output path
workdir = arcpy.env.workspace + '\\'
roadClasses = ['motorway', 'trunk', 'primary', 'secondary', 'tertiary']


def clip_city_original_osm(city):
    print (city + ' clipping...')
    boundary = clip_root + "\\" + city + '.shp' 
    outpath = workdir + city 
    arcpy.Clip_analysis(china_osm2021, boundary, outpath)


def name_ref(city):
    print (city + ' name_ref ing...')
    fc = workdir + city
    field1 = "name"
    field2 = "ref"
    cursor = arcpy.UpdateCursor(fc)
    for row in cursor:
        if row.getValue(field1).encode('utf-8') == ' ':
            row.setValue(field1, row.getValue(field2))
        cursor.updateRow(row)
    # Delete cursor and row objects
    del cursor, row


def road_select(city):
    print (city + ' road select...')
    city_osm = workdir + city

    for rdclass in roadClasses:
        print (city + ' %s select...' % rdclass)
        arcpy.MakeFeatureLayer_management(city_osm, 'temp')
        expression = "fclass = '%s' " % rdclass
        arcpy.SelectLayerByAttribute_management('temp', 'NEW_SELECTION', expression)
        arcpy.CopyFeatures_management('temp', city + '_' + rdclass)
        arcpy.Delete_management('temp')


def road_simp(city):
    print (city + ' road simplify...')

    for rdclass in ['motorway', 'trunk']:
        print (city + ' %s simp...' % rdclass)
        arcpy.MakeFeatureLayer_management(city + '_' + rdclass, 'lyr')
        arcpy.CopyFeatures_management('lyr', city + '_hnl')
        arcpy.Delete_management('lyr')

        # Project to Asia Lambert
        out_coordinate_system = arcpy.SpatialReference(102012)
        arcpy.Project_management(city + "_hnl", city + "_hnlproj", out_coordinate_system)

        arcpy.MakeFeatureLayer_management(city + "_hnlproj", 'lyr')
        arcpy.CopyFeatures_management('lyr', city + '_hnl')
        arcpy.Delete_management('lyr')

        # add merge field = 1
        print (city + '_%s' % rdclass + ' adding field and calculating...')
        arcpy.MultipartToSinglepart_management(city + '_hnl', city + '_hnl_sin')
        arcpy.AddField_management(city + '_hnl_sin', "merge", "SHORT")
        arcpy.CalculateField_management(city + '_hnl_sin', "merge", 1, "PYTHON_9.3")

        # merge divided roads
        print (city + '_%s' % rdclass + ' merging divided roads...')
        arcpy.MergeDividedRoads_cartography(city + '_hnl_sin', "merge", "20 Meters",
                                            city + '_hnl_sin_mer20', "")
        arcpy.MergeDividedRoads_cartography(city + '_hnl_sin_mer20', "merge", "20 Meters",
                                            city + '_hnl_sin_mer20_20', "")
        arcpy.MergeDividedRoads_cartography(city + '_hnl_sin_mer20_20', "merge", "20 Meters",
                                            city + '_hnl_sin_mer20_20_20', "")
        arcpy.MultipartToSinglepart_management(city + '_hnl_sin_mer20_20_20', city + '_hnl_sin_mer20_20_20_sin')
        arcpy.MergeDividedRoads_cartography(city + '_hnl_sin_mer20_20_20_sin', "merge", "50 Meters",
                                            city + '_hnl_sin_mer20_20_20_sin_50', "")
        arcpy.MergeDividedRoads_cartography(city + '_hnl_sin_mer20_20_20_sin_50', "merge", "50 Meters",
                                            city + '_hnl_sin_mer20_20_20_sin_50_50', "")
        arcpy.MergeDividedRoads_cartography(city + '_hnl_sin_mer20_20_20_sin_50_50', "merge", "50 Meters",
                                            city + '_hnl_sin_mer20_20_20_sin_50_50_50', "")
        arcpy.MultipartToSinglepart_management(city + '_hnl_sin_mer20_20_20_sin_50_50_50',
                                               city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin')
        arcpy.MergeDividedRoads_cartography(city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin', "merge", "100 Meters",
                                            city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin_100', "")
        arcpy.MergeDividedRoads_cartography(city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin_100', "merge", "100 Meters",
                                            city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin_100_100', "")
        arcpy.MergeDividedRoads_cartography(city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin_100_100', "merge",
                                            "100 Meters",
                                            city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin_100_100_100', "")
        arcpy.MultipartToSinglepart_management(city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin_100_100_100',
                                               city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin_100_100_100_sin')
        arcpy.MergeDividedRoads_cartography(city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin_100_100_100_sin', "merge",
                                            "150 Meters",
                                            city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin_100_100_100_sin_150', "")
        arcpy.MergeDividedRoads_cartography(city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin_100_100_100_sin_150', "merge",
                                            "150 Meters",
                                            city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin_100_100_100_sin_150_150', "")
        arcpy.MergeDividedRoads_cartography(city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin_100_100_100_sin_150_150',
                                            "merge",
                                            "150 Meters",
                                            city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin_100_100_100_sin_150_150_150',
                                            "")

        # optimize highway
        print (city + '_%s' % rdclass + " optimize...")
        arcpy.CopyFeatures_management(city + '_hnl_sin_mer20_20_20_sin_50_50_50_sin_100_100_100_sin_150_150_150',
                                      city + "_hnl_sin_merge_int")
        arcpy.Integrate_management(city + "_hnl_sin_merge_int", "50 Meters")

        arcpy.CopyFeatures_management(city + "_hnl_sin_merge_int", city + "_hnl_sin_merge_int_deleteid")
        arcpy.DeleteIdentical_management(city + "_hnl_sin_merge_int_deleteid", "shape")

        # Project to WGS84
        out_coordinate_system = arcpy.SpatialReference(4326)
        arcpy.Project_management(city + "_hnl_sin_merge_int_deleteid", city + "_hnlsimpproj", out_coordinate_system)
        # save the final result of highway to a simple name and convenient path
        arcpy.MakeFeatureLayer_management(city + "_hnlsimpproj", 'lyr')
        arcpy.CopyFeatures_management('lyr', city + '_%s' % rdclass + '_simp')
        arcpy.Delete_management('lyr')
        print (city + '_%s' % rdclass + ' Finished!')

    # for rdclass in ['primary', 'secondary', 'tertiary']
    # Project to Asia Lambert
    for rdclass in ['primary', 'secondary', 'tertiary']:
        out_coordinate_system = arcpy.SpatialReference(102012)
        arcpy.Project_management(city + '_' + rdclass, city + '_' + rdclass + '_prj', out_coordinate_system)

        arcpy.MakeFeatureLayer_management(city + '_' + rdclass + '_prj', 'lyr')
        arcpy.CopyFeatures_management('lyr', city + '_' + rdclass)
        arcpy.Delete_management('lyr')

    # export primary way, multitosingle and merge for several times
    print (city + ' dealing with primary roads...')
    arcpy.MakeFeatureLayer_management(city + "_primary", 'temp_lyr')
    arcpy.CopyFeatures_management('temp_lyr', city + '_pr')
    arcpy.Delete_management('temp_lyr')

    arcpy.MultipartToSinglepart_management(city + '_pr', city + '_pr_sin')
    arcpy.AddField_management(city + '_pr_sin', "merge", "SHORT")
    arcpy.CalculateField_management(city + '_pr_sin', "merge", 1, "PYTHON_9.3")
    arcpy.MergeDividedRoads_cartography(city + '_pr_sin', "merge", "50 Meters",
                                        city + '_pr_sin_mer50', "")  # 1st multitosingle and merge
    arcpy.MergeDividedRoads_cartography(city + '_pr_sin_mer50', "merge", "100 Meters",
                                        city + '_pr_sin_mer50_100', "")  # 2nd multitosingle and merge
    arcpy.MergeDividedRoads_cartography(city + '_pr_sin_mer50_100', "merge", "150 Meters",
                                        city + '_pr_sin_mer50_100_150', "")  # 3rd multitosingle and merge
    arcpy.MergeDividedRoads_cartography(city + '_pr_sin_mer50_100_150', "merge", "200 Meters",
                                        city + '_pr_sin_mer50_100_150_200', "")  # 4th multitosingle and merge
    # save the final result of primary roads to a simple name and convenient path
    arcpy.MakeFeatureLayer_management(city + '_pr_sin_mer50_100_150_200', 'lyr')
    arcpy.CopyFeatures_management('lyr', city + '_primary_simp')
    arcpy.Delete_management('lyr')

    # export secondary way, multitosingle and merge for several times
    print (city + ' dealing with secondary roads...')
    arcpy.MakeFeatureLayer_management(city + "_secondary", 'temp_lyr')
    arcpy.CopyFeatures_management('temp_lyr', city + '_sec')
    arcpy.Delete_management('temp_lyr')

    arcpy.MultipartToSinglepart_management(city + '_sec', city + '_sec_sin')
    arcpy.AddField_management(city + '_sec_sin', "merge", "SHORT")
    arcpy.CalculateField_management(city + '_sec_sin', "merge", 1, "PYTHON_9.3")
    arcpy.MergeDividedRoads_cartography(city + '_sec_sin', "merge", "25 Meters",
                                        city + '_sec_sin_mer25', "")  # 1st multitosingle and merge
    arcpy.MergeDividedRoads_cartography(city + '_sec_sin_mer25', "merge", "50 Meters",
                                        city + '_sec_sin_mer25_50', "")  # 2nd multitosingle and merge
    arcpy.MergeDividedRoads_cartography(city + '_sec_sin_mer25_50', "merge", "100 Meters",
                                        city + '_sec_sin_mer25_50_100', "")  # 3rd multitosingle and merge
    arcpy.MergeDividedRoads_cartography(city + '_sec_sin_mer25_50_100', "merge", "150 Meters",
                                        city + '_sec_sin_mer25_50_100_150', "")  # 4th multitosingle and merge
    # save the final result of secondary roads to a simple name and convenient path
    arcpy.MakeFeatureLayer_management(city + '_sec_sin_mer25_50_100_150', 'lyr')
    arcpy.CopyFeatures_management('lyr', city + '_secondary_simp')
    arcpy.Delete_management('lyr')

    # export tertiary way, multitosingle and merge for several times
    print (city + ' dealing with tertiary roads...')
    arcpy.MakeFeatureLayer_management(city + "_tertiary", 'temp_lyr')
    arcpy.SelectLayerByAttribute_management('temp_lyr', "NEW_SELECTION", "\"fclass\" = 'tertiary'")
    arcpy.CopyFeatures_management('temp_lyr', city + '_ter')
    arcpy.Delete_management('temp_lyr')

    arcpy.MultipartToSinglepart_management(city + '_ter', city + '_ter_sin')
    arcpy.AddField_management(city + '_ter_sin', "merge", "SHORT")
    arcpy.CalculateField_management(city + '_ter_sin', "merge", 1, "PYTHON_9.3")
    arcpy.MergeDividedRoads_cartography(city + '_ter_sin', "merge", "50 Meters",
                                        city + '_ter_sin_mer50', "")  # 1st  merge
    arcpy.MergeDividedRoads_cartography(city + '_ter_sin_mer50', "merge", "100 Meters",
                                        city + '_ter_sin_mer50_100', "")  # 2nd  merge
    arcpy.MergeDividedRoads_cartography(city + '_ter_sin_mer50_100', "merge", "150 Meters",
                                        city + '_ter_sin_mer50_100_150', "")  # 3rd  merge
    arcpy.MergeDividedRoads_cartography(city + '_ter_sin_mer50_100_150', "merge", "150 Meters",
                                        city + '_ter_sin_mer50_100_150_150', "")  # 4th  merge
    arcpy.MergeDividedRoads_cartography(city + '_ter_sin_mer50_100_150_150', "merge", "150 Meters",
                                        city + '_ter_sin_mer50_100_150_150_150', "")  # 5th  merge
    # save the final result of tertiary roads to a simple name and convenient path
    arcpy.MakeFeatureLayer_management(city + '_ter_sin_mer50_100_150_150_150', 'lyr')
    arcpy.CopyFeatures_management('lyr', city + '_tertiary_simp')
    arcpy.Delete_management('lyr')

    # Project to WGS84
    for rdclass in ['primary', 'secondary', 'tertiary']:
        out_coordinate_system = arcpy.SpatialReference(4326)
        arcpy.Project_management(city + '_' + rdclass + '_simp', city + '_' + rdclass + '_simp_prj', out_coordinate_system)
        # save the final result of simplified roads to a simple name and convenient path
        arcpy.MakeFeatureLayer_management(city + '_' + rdclass + '_simp_prj', 'lyr')
        arcpy.CopyFeatures_management('lyr', city + '_' + rdclass + '_simp')
        arcpy.Delete_management('lyr')

    print (city + ' simp Finished!!!')


def road_merge(city):
    print (city + ' road merge and simp...')
    # Merge all kind of unhighway roads together (primary, secondary, tertiary, residential and other)
    # and multi to single and merge divided roads
    arcpy.Merge_management([city + '_motorway_simp',
                            city + '_trunk_simp',
                            city + '_primary_simp',
                            city + '_secondary_simp',
                            city + '_tertiary_simp'], city + '_merge_simp')

    # Project to Asia Lambert
    out_coordinate_system = arcpy.SpatialReference(102012)
    arcpy.Project_management(city + '_merge_simp', city + '_merge_simp_prj', out_coordinate_system)

    arcpy.MakeFeatureLayer_management(city + '_merge_simp_prj', 'lyr')
    arcpy.CopyFeatures_management('lyr', city + '_merge_simp')
    arcpy.Delete_management('lyr')

    # simplify merged road
    arcpy.MultipartToSinglepart_management(city + "_merge_simp", city + "_merge_simp_sin")
    arcpy.MergeDividedRoads_cartography(city + "_merge_simp_sin", "merge", "50 Meters",
                                        city + "_merge_simp_sin_mer50", "")
    arcpy.MergeDividedRoads_cartography(city + "_merge_simp_sin_mer50", "merge", "50 Meters",
                                        city + "_merge_simp_sin_mer50_50", "")

    # Project to WGS84
    out_coordinate_system = arcpy.SpatialReference(4326)
    arcpy.Project_management(city + "_merge_simp_sin_mer50_50", city + '_merge_simp_mer_prj', out_coordinate_system)
    # save the final result of simplified roads to a simple name and convenient path
    arcpy.MakeFeatureLayer_management(city + '_merge_simp_mer_prj', 'lyr')
    arcpy.CopyFeatures_management('lyr', city + '_osm')
    arcpy.Delete_management('lyr')

# only keep first 6 fields
def del_field(city):
    print( city + '_osm delete fields...')
    names = arcpy.ListFields(city + "_osm")
    colnum = []
    for i in range(6, len(names) - 1):
        colnum.append(i)
    dropfields = []
    for i in colnum:
        dropfields.append(names[i].name)

    arcpy.MakeFeatureLayer_management(city + "_osm", 'lyr')
    arcpy.CopyFeatures_management('lyr', city + "_osmdel")
    arcpy.Delete_management('lyr')

    arcpy.DeleteField_management(city + "_osmdel", dropfields)
    arcpy.MakeFeatureLayer_management(city + "_osmdel", 'lyr')
    arcpy.CopyFeatures_management('lyr', city + "_osm")
    arcpy.Delete_management('lyr')
    print (city + "_osm delete unused fields finished!")


# =======================================================

citylist = ['wuxi','changzhou','suzhou','wenzhou','jiaxing','shaoxing','wuhu','foshan','dongguan']
keeplist = []
# citylist = ['huhehaote']
# city = 'huhehaote'


for city in citylist[1:]:
    print(city)
    # ---从全国osm路网中裁剪出各个城市范围的osm路网
    clip_city_original_osm(city)

    # ---当name字段为空而ref字段有信息时，将ref信息补充到name
    name_ref(city)

    # ---挑选出所需的五种道路
    road_select(city)

    # ---简化道路
    road_simp(city)

    # ---合并再次简化
    road_merge(city)

    # ---删除多余字段
    del_field(city)

    # ---添加需要保留的文件
    keeplist.append(city + '_osm')

print ('All cities finished!!!')


#-----------------------------------------------------------------------------------------------------------------------
print ('Deleting unused files...')
files = arcpy.ListFeatureClasses()
for fl in files:
    if fl not in keeplist:
        print (fl)
        arcpy.Delete_management(fl)
print ("delete files Finished!")

