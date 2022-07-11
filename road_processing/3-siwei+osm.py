import arcpy
import pandas as pd
import os

arcpy.env.workspace = r'E:\01_CityDiagnosis2021\01_Data\04_road\00road_osm_siwei.gdb'
arcpy.env.overwriteOutput = True

# simplified road data (simp_path should be same as 'arcpy.env.workspace' in osm_siwei_simplify_highway_road.py)
# simp_path = r'D:\CityDNA\Data\changzhou0721\city_boundary\changzhou.gdb'


# canceloverlap and merge
def CancelOverlapRoads(basemap, cancelmap):
    print (basemap + ' cancel overlap roads... ')
    # project to "Asia Alberts Lambert"
    out_coordinate_system = arcpy.SpatialReference(102012)
    arcpy.Project_management(os.path.join(cancelmapRoot, cancelmap), cancelmap + "proj", out_coordinate_system)

    # create 20m buffer of basemap
    print (basemap + ' create 50 meters buffer...')
    arcpy.Buffer_analysis(os.path.join(basemapRoot, basemap), basemap + "50", "50 Meters")

    # cancelmapproj INTERSECT basemap20
    print (basemap + ' intersect...')
    arcpy.Intersect_analysis([basemap + '50', cancelmap + 'proj'], cancelmap + 'inter')

    # dissolve same FID !!!!NAME
    print (basemap + ' dissolve field...')
    dissolve_field = "FID_" + cancelmap + 'proj'
    arcpy.Dissolve_management(cancelmap + 'inter', cancelmap + 'interdis', dissolve_field)

    # add field
    print (basemap + ' add field...')
    arcpy.AddField_management(cancelmap + "proj", "LengthAll", "DOUBLE")
    arcpy.AddField_management(cancelmap + 'interdis', "LengthPart", "DOUBLE")

    # calculate geometry
    print (basemap + ' calculate geometry...')
    arcpy.CalculateField_management(cancelmap + "proj", "LengthAll", "!shape.length@meters!", "PYTHON_9.3")
    arcpy.CalculateField_management(cancelmap + 'interdis', "LengthPart", "!shape.length@meters!", "PYTHON_9.3")

    # before join table, create new field, add index
    print (basemap + ' create new field, add index...')
    arcpy.AddField_management(cancelmap + "proj", "FIDid", "LONG")
    # add cursor
    fc = cancelmap + "proj"
    field1 = "OBJECTID"
    field2 = "FIDid"
    cursor = arcpy.UpdateCursor(fc)
    for row in cursor:
        # field2(FIDid) will be equal to field1(FID)
        row.setValue(field2, row.getValue(field1))
        cursor.updateRow(row)
    del row
    del cursor
    # make index
    arcpy.AddIndex_management(cancelmap + "proj", "FIDid", "index", "UNIQUE", "ASCENDING")

    # join table and export the result as addonmap+join.shp
    print (basemap + ' join table...')
    arcpy.MakeFeatureLayer_management(cancelmap + "proj", "tempLayer")
    arcpy.AddJoin_management("tempLayer", "FIDid", cancelmap + 'interdis', dissolve_field, "KEEP_COMMON")
    arcpy.CopyFeatures_management("tempLayer", cancelmap + "join")
    arcpy.Delete_management('tempLayer')

    # calculate the percent
    print (basemap + " addfield...")
    arcpy.AddField_management(cancelmap + "join", "percent", "DOUBLE")

    print (basemap + ' calculate percent...')
    fc2 = cancelmap + "join"
    fieldAll = cancelmap + "proj_LengthAll"
    fieldPart = cancelmap + "interdis_LengthPart"
    target = "percent"
    cursor = arcpy.UpdateCursor(fc2)
    for row in cursor:
        # calculate percent field
        row.setValue(target, row.getValue(fieldPart) / row.getValue(fieldAll))
        cursor.updateRow(row)
    del row
    del cursor

    # extract Threshold value
    arcpy.MakeFeatureLayer_management(cancelmap + "join", 'lyr')
    arcpy.SelectLayerByAttribute_management('lyr', 'NEW_SELECTION', '"percent" > 0.3')
    arcpy.CopyFeatures_management('lyr', cancelmap + "_add")
    arcpy.Delete_management('lyr')

    # in "percent" > 0.3, record 'beijing_road_addoninterdis_FID_beijing_road_addonproj' and delete from '_road' file
    print (cancelmap + " record FID...")
    fc = cancelmap + "_add"
    field1 = city + "_osminterdis_FID_" + city + "_osmproj"
    fid = []
    cursor = arcpy.UpdateCursor(fc)
    for row in cursor:
        fid.append(row.getValue(field1))
        cursor.updateRow(row)
    # Delete cursor and row objects
    del cursor, row
    print (cancelmap + " record FID finished!")

    # delete the fid records in cancelmap
    arcpy.MakeFeatureLayer_management(os.path.join(cancelmapRoot, cancelmap), 'lyr')
    arcpy.CopyFeatures_management('lyr', cancelmap + "_deloverlap")
    arcpy.Delete_management('lyr')
    print (cancelmap + " deleteRow OBJECTID...")
    fc = cancelmap + "_deloverlap"
    field1 = "OBJECTID"
    with arcpy.da.UpdateCursor(fc, field1) as cursor:
        for row in cursor:
            if row[0] in fid:
                cursor.deleteRow()
    del cursor, row
    print (cancelmap + " deleteRow OBJECTID finished!")

    # Merge basemap and cancelmap
    print (basemap + ' merge...')
    arcpy.Merge_management([os.path.join(basemapRoot, basemap), cancelmap + "_deloverlap"], city + "_osm2siwei")

    # Project to WGS84
    out_coordinate_system = arcpy.SpatialReference(4326)
    arcpy.Project_management(city + "_osm2siwei", city + "_osm2siwei_proj", out_coordinate_system)
    # save the final result of highway to a simple name and convenient path
    arcpy.MakeFeatureLayer_management(city + "_osm2siwei_proj", 'lyr')
    arcpy.CopyFeatures_management('lyr', city + "_osm2siwei")
    arcpy.Delete_management('lyr')
    print (basemap + ' finished!')


# ===================================
'''
函数定义部分结束，以下为循环运行部分
'''
citylist = ['beijing', 'tianjin', 'shanghai', 'chongqing', 'shijiazhuang', 'tangshan', 'taiyuan', 'jincheng',
            'huhehaote', 'baotou', 'haerbin', 'daqing', 'changchun', 'siping', 'shenyang', 'dalian', 'jinan', 'qingdao',
            'dongying', 'nanjing', 'xuzhou', 'hefei', 'bozhou', 'hangzhou', 'ningbo', 'quzhou', 'fuzhou', 'xiamen',
            'nanchang', 'jingdezhen', 'ganzhou', 'zhengzhou', 'luoyang', 'wuhan', 'huangshi', 'changsha', 'changde',
            'guangzhou', 'shenzhen', 'haikou', 'sanya', 'nanning', 'liuzhou', 'kunming', 'lincang', 'guiyang', 'anshun',
            'chengdu', 'suining', 'xian', 'yanan', 'lanzhou', 'baiyin', 'yinchuan', 'wuzhong', 'wulumuqi', 'kelamayi',
            'xining', 'lasa']
keeplist = []

# city = 'fuzhou'
# city = 'tianjin'
# citylist = ['tianjin', 'fuzhou']

for city in citylist[:1]:
    basemapRoot = r'E:\01_CityDiagnosis2021\01_Data\04_road\02road_siwei_single.gdb'
    cancelmapRoot = r'E:\01_CityDiagnosis2021\01_Data\04_road\01road_osm_single.gdb'
    basemap = city
    cancelmap = city + "_osm"
    CancelOverlapRoads(basemap, cancelmap)
    print (city + ' finished!!!')

keeplist = []
# complete keeplist and delete unused files
for city in citylist:
    keeplist.append(city + "_osm2siwei")


files = arcpy.ListFeatureClasses()
for fl in files:
    if fl not in keeplist:
        print ("Delelting " + fl)
        arcpy.Delete_management(fl)
print( "Finish delete files!!!")

