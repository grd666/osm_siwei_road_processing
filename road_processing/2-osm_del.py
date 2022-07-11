import arcpy
import pandas as pd

arcpy.env.workspace = r'E:\\citydna\\TOD\\code\\data_review\\road\\road_processing\\osm_road_del.gdb'
arcpy.env.overwriteOutput = True

# canceloverlap and merge
def CancelOverlapRoads(basemap, cancelmap):
    print (basemap + ' cancel overlap roads... ')
    # project to "Asia Alberts Lambert"
    out_coordinate_system = arcpy.SpatialReference(102012)
    arcpy.Project_management(cancelmap, cancelmap + "proj", out_coordinate_system)

    # create 20m buffer of basemap
    print (basemap + ' create 50 meters buffer...')
    arcpy.Buffer_analysis(basemap, basemap + "50", "50 Meters")

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
    field1 = city + "_roadinterdis_FID_" + city + "_roadproj"
    fid = []
    cursor = arcpy.UpdateCursor(fc)
    for row in cursor:
        # print row.getValue(field1)
        fid.append(row.getValue(field1))
        cursor.updateRow(row)
    # Delete cursor and row objects
    del cursor, row
    print (cancelmap + " record FID finished!")

    # delete the fid records in cancelmap
    arcpy.MakeFeatureLayer_management(cancelmap, 'lyr')
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
    arcpy.Merge_management([basemap, cancelmap + "_deloverlap"], city + "_highway_add_road")

    # Project to WGS84
    out_coordinate_system = arcpy.SpatialReference(4326)
    arcpy.Project_management(city + "_highway_add_road", city + "_highway_add_road_proj", out_coordinate_system)
    # save the final result of highway to a simple name and convenient path
    arcpy.MakeFeatureLayer_management(city + "_highway_add_road_proj", 'lyr')
    arcpy.CopyFeatures_management('lyr', city + "_osmdel")
    arcpy.Delete_management('lyr')
    print (basemap + ' finished!')


# ==========================================================================
citylist = ['wuxi','changzhou','suzhou','wenzhou','jiaxing','shaoxing','wuhu','foshan','dongguan']
keeplist = []


for city in citylist[1:]:
    arcpy.MakeFeatureLayer_management(r'E:\\citydna\\TOD\\code\\data_review\\road\\road_processing\\osm_road_simp.gdb\\' + city + "_osm", 'temp')
    expression = "fclass in ('motorway', 'trunk') "
    arcpy.SelectLayerByAttribute_management('temp', 'NEW_SELECTION', expression)
    arcpy.CopyFeatures_management('temp', city + '_highway')
    arcpy.Delete_management('temp')

    arcpy.MakeFeatureLayer_management(r'E:\\citydna\\TOD\\code\\data_review\\road\\road_processing\\osm_road_simp.gdb\\' + city + "_osm", 'temp')
    expression = "fclass in ('primary', 'secondary', 'tertiary') "
    arcpy.SelectLayerByAttribute_management('temp', 'NEW_SELECTION', expression)
    arcpy.CopyFeatures_management('temp', city + '_road')
    arcpy.Delete_management('temp')

    basemap = city + "_highway"
    cancelmap = city + "_road"

    CancelOverlapRoads(basemap, cancelmap)

    keeplist.append(city + "_osmdel")

    print (city + ' finished!!!')


# delete unused files
files = arcpy.ListFeatureClasses()
for fl in files:
    if fl not in keeplist:
        print (fl)
        arcpy.Delete_management(fl)
print ("Finish delete files!!!")








