# Date: 2019/04/15
# Author: ZQY
# Content: Extract ungaosu road and simplify the road
# Email: qingyuanzhang@citydnatech.com

import arcpy
import os
import sys
from arcpy import env
import time

arcpy.env.overwriteOutput = True

reload(sys)
sys.setdefaultencoding('utf8')

# city = 'beijing'

rawDir = r'G:\00_BaseData\03_RoadSimp'
arcpy.SpatialReference(4326)
arcpy.env.overwriteOutput = True
citylist = ['laibin']

for city in citylist:
    print(city)
    # <---------------------------------------------- STEP 1 -------------------------------------------------------------->
    inputGDB = r'G:\00_BaseData\03_RoadSimp\01_RoadSiWei' #change to where you save for siwei
    outputGDB = rawDir + os.sep + city + '_shapes.gdb'

    rd_class = ['高速公路', '国道', '都市高速路', '省道', '县道', '乡镇道路', '九级路', '行人道路']
    rd_class_EN = ['rd00', 'rd01', 'rd02', 'rd03', 'rd04', 'rd05', 'rd06', 'rd07']

    arcpy.CreateFileGDB_management(rawDir, city + "_shapes.gdb", "10.0")
    env.workspace = rawDir + os.sep + city + r'_shapes.gdb'

    # Local variables:
    arcpy.CopyFeatures_management(r'G:\00_BaseData\03_RoadSimp\01_CityBoundary\\' + city + '.shp', outputGDB + os.sep + 'boundary')
    parcel = "boundary"


    start = time.clock()
    for index, feature in enumerate(rd_class):
        print(index, feature)
        arcpy.Clip_analysis(inputGDB+os.sep+feature+'.shp', parcel, rd_class_EN[index])
        # arcpy.AddField_management(rd_class_EN[index],"rdClass","TEXT")
        # arcpy.CalculateField_management(rd_class_EN[index],"rdClass",rd_class[index],"PYTHON_9.3")
        arcpy.AddField_management(rd_class_EN[index],"rdClass","TEXT")
        arcpy.CalculateField_management(rd_class_EN[index],"rdClass",'\"'+rd_class_EN[index]+'\"',"PYTHON_9.3")
    elapsed = (time.clock() - start)
    print("Step 1 Time used:", elapsed, ' finished!')
    # <---------------------------------------------- STEP 2 -------------------------------------------------------------->
    inputGDB = rawDir + os.sep + city + '_shapes.gdb'
    outputGDB = rawDir + os.sep + city + '_road_simp_result.gdb'

    rd_class = ['高速公路', '国道', '都市高速路', '省道', '县道', '乡镇道路', '九级路', '行人道路']
    rd_class_EN = ['rd00', 'rd01', 'rd02', 'rd03', 'rd04', 'rd05', 'rd06', 'rd07']

    # create a dictionary containing sql to extract road element by kind
    arcpy.env.workspace = rawDir + os.sep + "test_0217.gdb"

    sql_dict_by_kind = {
        "rd00": "Kind = '0002|0005|000c' Or Kind = '0002|0008|000c' Or Kind = '0002|000c' Or Kind = '0002|000c|000f' Or Kind = '0004|0005|000b' Or Kind = '0005|000c' Or Kind = '000b|000c' Or Kind = '000c'",
        "rd01": "Kind <> '020a' And Kind <> '0204' And Kind <> '0204|0216' And Kind <> '0202|0204' And Kind <> '020b' And Kind <> '020a|0217' And Kind <> '0212' And Kind <> '0204|020a' And Kind <> '0204|020a|0217' And Kind <> '020a|0212|0217'",
        "rd02": "Kind <> '0105|010b|0117' And Kind <> '0105|010b' And Kind <> '0103|010b|010c' And Kind <> '0105|0108|010b' And Kind <> '0103|0108|010b|010c'",
        "rd03": "Kind = '0300' Or Kind = '0301' Or Kind = '0302' Or Kind = '0302|0308' Or Kind = '0302|030f' Or Kind = '0304' Or Kind = '0304|0308|030a' Or Kind = '0308' Or Kind = '0308|030a' Or Kind = '030a' Or Kind = '030b' and PathName NOT LIKE '%立交%'",
        "rd04": "Kind <> '0400' And Kind <> '0404' And Kind <> '0404|040a' And Kind <> '0404|040a|0417' And Kind <> '0404|0415' And Kind <> '0404|0416' And Kind <> '040a' And Kind <> '040a|0412' And Kind <> '040a|0417' And Kind <> '040b' And Kind <> '040b|0416' And Kind <> '040f' And Kind <> '0412' And Kind <> '0416'",
        "rd05": "Kind <> '0600' And Kind <> '0604' And Kind <> '0604|060a' And Kind <> '0604|060a|0616' And Kind <> '0604|060a|0617' And Kind <> '0604|060b|0616' And Kind <> '0604|0613' And Kind <> '0604|0613|0616' And Kind <> '0604|0614|0616' And Kind <> '0604|0615' And Kind <> '0604|0615|0616' And Kind <> '0604|0616' And Kind <> '0604|0617' And Kind <> '060a|0612' And Kind <> '060a|0612|0617' And Kind <> '060a|0617' And Kind <> '060b' And Kind <> '0612' And Kind <> '0615' And Kind <> '0616'"
    }

    replace_dict_by_kind = {
        "0401": "0401",
        "0402": "0402",
        "0404": "0404",
        "0408": "0408",
        "0402|0408": "0402",
        "0402|040f": "0402"
    }

    replace_dict_by_kind_2 = {
        "0600": "0600",
        "0601": "0601",
        "0602": "0602",
        "0602|0604": "0602",
        "0602|0608": "0602",
        "0602|060f": "0602",
        "0602|0613": "0602|0613",
        "0602|0614": "0602",
        "0604": "0604",
        "0604|060a": "0604|060a",
        "0604|060a|0616": "0604|060a|0616",
        "0604|060a|0617": "0604|060a|0617",
        "0604|060b|0616": "0604|060b|0616",
        "0604|0613": "0604|0613",
        "0604|0613|0616": "0604|0613|0616",
        "0604|0614": "0601",
        "0604|0614|0616": "0604|0614|0616",
        "0604|0615": "0604|0615",
        "0604|0615|0616": "0604|0615|0616",
        "0604|0616": "0604|0616",
        "0604|0617": "0604|0617",
        "0608": "0601",
        "0608|060a": "060a",
        "0608|0615": "0608|0615",
        "0609": "0601",
        "060a": "060a",
        "060a|0612": "060a|0612",
        "060a|0612|0617": "060a|0612|0617",
        "060a|0617": "060a|0617",
        "060b": "060b",
        "060e": "060e",
        "060f": "0601",
        "0612": "0612",
        "0613": "0613",
        "0614": "0601",
        "0615": "0615",
        "0616": "0616"
    }

    config_by_kind = {
        'rd00': {'merge_distance': 60, 'select_area': 10000},
        'rd01': {'merge_distance': 60, 'select_area': 10000},
        'rd02': {'merge_distance': 60, 'select_area': 10000},
        'rd03': {'merge_distance': 30, 'select_area': 10000},
        'rd04': {'merge_distance': 60, 'select_area': 10000},
        'rd05': {'merge_distance': 60, 'select_area': 10000}
    }


    # sub functions extends from pangding's ori codes

    def subfunc(roadClassList, mergeDistance):
        if len(roadClassList) == 1:
            print 'case one'
            roadClass = roadClassList[0]
            arcpy.CopyFeatures_management(inputGDB + os.sep + roadClass, roadClass)
            arcpy.Select_analysis(roadClass, '_temp', sql_dict_by_kind.get(roadClass))
        else:
            print 'case two'
            mergelist = []
            roadClass = ''
            for i in roadClassList:
                print(i)
                arcpy.CopyFeatures_management(inputGDB + os.sep + i, i)
                arcpy.Select_analysis(i, '_temp' + i, sql_dict_by_kind.get(i))
                mergelist.append('_temp' + i)
                roadClass += i
            arcpy.Merge_management(mergelist, '_temp' + roadClass)
            arcpy.CopyFeatures_management('_temp' + roadClass, '_temp')

            # optimize by kind field
        if roadClass == "rd04":
            with arcpy.da.UpdateCursor('_temp', ['Kind']) as cursor:
                # For each row, evaluate the WELL_YIELD value (index position
                # of 0), and update WELL_CLASS (index position of 1)
                for row in cursor:
                    row[0] = replace_dict_by_kind.get(row[0])
                    # Update the cursor with the updated list
                    cursor.updateRow(row)
                del row, cursor
        elif roadClass == "rd05":
            with arcpy.da.UpdateCursor('_temp', ['Kind']) as cursor:
                # For each row, evaluate the WELL_YIELD value (index position
                # of 0), and update WELL_CLASS (index position of 1)
                for row in cursor:
                    row[0] = replace_dict_by_kind.get(row[0])
                    # Update the cursor with the updated list
                    cursor.updateRow(row)
                del row, cursor

        # dissolve by key fields: kind, rdClass, lanenum and pathname
        # not all roads have pathname so we treat them separately

        arcpy.Select_analysis('_temp', '_temp_1', "PathName <> ''")
        arcpy.Dissolve_management(('_temp_1'), 'dissolve_1', ["Kind", "LaneNum", "rdClass", "PathName"])
        arcpy.Select_analysis('_temp', '_temp_2', "PathName = ''")
        arcpy.Dissolve_management(('_temp_2'), 'dissolve_2', ["Kind", "LaneNum", "rdClass"])
        arcpy.Merge_management(['dissolve_1', 'dissolve_2'], 'dissolve')
        arcpy.DeleteField_management('dissolve', 'merge')
        arcpy.AddField_management('dissolve', 'merge', "SHORT")

        arcpy.CalculateField_management('dissolve', 'merge', 1, "PYTHON_9.3")
        arcpy.MultipartToSinglepart_management('dissolve','dissolve_multi')
        arcpy.FeatureToLine_management('dissolve_multi', '_multi')

        # we should test and apply different merge distance for different roadClass,
        # but currently we use 60 meters for all of them
        arcpy.MergeDividedRoads_cartography('_multi', 'merge', str(mergeDistance) + ' meters', '_merged')

        # alter merging, there are a bunch of short roads being genereated, so we have to dissolve one more time
        arcpy.Dissolve_management(('_merged'), '_merged_dissolve_1', ["LaneNum", "rdClass", "PathName"])

        # save two return features
        arcpy.CopyFeatures_management('_multi', '_multi_' + roadClass)
        # in next step this feature will be used to provide full sectional info for each road link
        arcpy.CopyFeatures_management('_multi', outputGDB + os.sep + '_multi' + roadClass)

        arcpy.CopyFeatures_management('_merged_dissolve_1', '_merged_' + roadClass)
        # in next step this feature will be treated as base to extract the true center line
        arcpy.CopyFeatures_management('_merged_dissolve_1', outputGDB + os.sep + '_merged_' + roadClass)

        # then we try to link spatial relationship to merged links by merged distance

        arcpy.Delete_management('_temp')
        arcpy.Delete_management('_temp_1')
        arcpy.Delete_management('_temp_2')
        arcpy.Delete_management('dissolve_1')
        arcpy.Delete_management('dissolve_2')
        arcpy.Delete_management('dissolve')
        arcpy.Delete_management('_multi')
        arcpy.Delete_management('_merged')
        arcpy.Delete_management('_merged_dissolve_1')
        arcpy.Delete_management('dissolve_multi')


    def small_triangle_optimize(roadClass, selectarea):
        # function designed to capture outer bound lines

        if roadClass not in rd_class_EN:
            inputfile = roadClass
            outputfile = roadClass
        else:
            inputfile = '_merged_' + roadClass
            outputfile = '_merged_ct' + roadClass

        # arcpy.ExtendLine_edit(road_class,"5 meters","FEATURE")
        arcpy.FeatureToLine_management(inputfile, '_merged_f2l')

        arcpy.FeatureVerticesToPoints_management('_merged_f2l', '_bothpt', 'BOTH_ENDS')
        arcpy.DeleteIdentical_management('_bothpt', ["Shape"])

        arcpy.FeatureToPolygon_management('_merged_f2l', '_toPgon')
        arcpy.AddField_management('_toPgon', "area", "FLOAT")
        arcpy.CalculateField_management('_toPgon', "area", "!shape.area@meters!", "PYTHON_9.3")
        arcpy.Select_analysis('_toPgon', '_toPgon_sm_60', 'area<' + selectarea)

        arcpy.SpatialJoin_analysis('_merged_f2l', '_toPgon_sm_60', '_sj', 'JOIN_ONE_TO_ONE', '', '',
                                   'SHARE_A_LINE_SEGMENT_WITH')
        arcpy.Select_analysis('_sj', '_sj1', 'Join_Count=1')
        arcpy.Select_analysis('_sj', '_sj2', 'Join_Count=2')
        arcpy.SpatialJoin_analysis('_sj1', '_sj2', '_sjed', 'JOIN_ONE_TO_ONE', '', '', 'INTERSECT')
        arcpy.Select_analysis('_sjed', '_to_be_del', 'Join_Count_1>0')

        arcpy.AddField_management('_to_be_del', "tag", "SHORT")
        arcpy.CalculateField_management('_to_be_del', "tag", "1", "PYTHON_9.3")

        # join the tag to delete all need to be deleted
        arcpy.JoinField_management('_merged_f2l', "OBJECTID", '_to_be_del', "TARGET_FID", ['tag'])
        arcpy.Select_analysis('_merged_f2l', '_merged_ct', 'tag IS NULL')

        # select out by tag and copy to outputGDB
        arcpy.CopyFeatures_management('_merged_ct', outputGDB + os.sep + outputfile)

        ### things need to be done
        # 1) del all temp features
        # 2) join by a certain combination of layers to create other small areas and repeat this func

        arcpy.Delete_management('_sj')
        arcpy.Delete_management('_sj1')
        arcpy.Delete_management('_sj2')
        arcpy.Delete_management('_sjed')
        arcpy.Delete_management('_to_be_del')


    ## 弧度比值优化去掉匝道等路
    ## 345 几乎是同个级别，可以通过merge之后再形成小的边块进行计算

    def main_all_but_separate():
        arcpy.CreateFileGDB_management(rawDir, city + "_road_simp_result.gdb", "10.0")
        # for road in rd_class_EN[:6]:
        # for road in rd_class_EN[3:6]:
        for road in ['rd01','rd03', 'rd04', 'rd05']:
            print(road)
            arcpy.CreateFileGDB_management(rawDir, "test_0217" + road + ".gdb", "10.0")
            arcpy.env.workspace = rawDir + os.sep + "test_0217" + road + ".gdb"
            v_record1 = arcpy.GetCount_management(inputGDB + os.sep + road)
            if int(v_record1.getOutput(0)) != 0:
                print(road, int(v_record1.getOutput(0)))
                subfunc([road], 60)
                # attach_sublane_attr(road)
                small_triangle_optimize(road, str(config_by_kind[road]['select_area']))


    def main_test_with_one_class(classnum):
        road = rd_class_EN[classnum]
        arcpy.CreateFileGDB_management(rawDir, "test_0217" + road + ".gdb", "10.0")
        arcpy.env.workspace = rawDir + os.sep + "test_0217" + road + ".gdb"
        subfunc(road)


    def main_merging_some(roadClassList):
        roadClassList = ['rd00', 'rd01', 'rd03']
        roadClass = ''
        for i in roadClassList:
            roadClass += i
        arcpy.CreateFileGDB_management(rawDir, city + "_road_simp_result" + roadClass + ".gdb", "10.0")
        arcpy.env.workspace = rawDir + os.sep + city + "_road_simp_result" + roadClass + ".gdb"

        subfunc(roadClassList, 100)

        arcpy.ExtendLine_edit('_merged' + roadClass, "50 meters", "FEATURE")

        arcpy.CopyFeatures_management('_merged_' + roadClass, '_merged_ori')
        small_triangle_optimize('_merged_ori', '10000')


    start = time.clock()
    ### fill in the function we want to execute
    main_all_but_separate()
    elapsed = (time.clock() - start)
    print("Step 2 Time used:", elapsed, ' finished!')

    # <---------------------------------------------- STEP 3 -------------------------------------------------------------->
    inputGDB = rawDir + os.sep + city + '_road_simptest.gdb'
    outputGDB = rawDir + os.sep + city + '_road_simp_result.gdb'
    bufferGDB = rawDir + os.sep + city + '_rd_buffer.gdb'

    rd_class = ['高速公路', '国道', '都市高速路', '省道', '县道', '乡镇道路', '九级路', '行人道路']
    rd_class_EN = ['rd00', 'rd01', 'rd02', 'rd03', 'rd04', 'rd05', 'rd06', 'rd07']

    arcpy.CreateFileGDB_management(rawDir,  city + "_rd_buffer.gdb", "10.0")

    def unique_values(table, field):
        with arcpy.da.SearchCursor(table, [field]) as cursor:
            return sorted({row[0] for row in cursor})

    # 根据道路等级设置buffer,选择在buffer内的路,最后一步是merge了buffer road
    def create_buffer_rdclass():
        # create buffer based on road class
        merge_list = []

        # for i in rd_class_EN[3:-2]:
        for i in ['rd01','rd03', 'rd04', 'rd05']:
            # i = 'rd03'
            if (arcpy.Exists(outputGDB + os.sep + '_merged_ct' + i)) is True:
                print(outputGDB + os.sep + '_merged_ct' + i)
                i_index = rd_class_EN[:-2].index(i)
                buffer_feature = outputGDB + os.sep + '_merged_ct' + i
                output_buffer = bufferGDB + os.sep + 'buffer_' + i
                arcpy.Buffer_analysis(buffer_feature, output_buffer, "60 Meters", "", "", "ALL")
                for j in rd_class_EN[i_index + 1: -2]:
                    if (arcpy.Exists(outputGDB + os.sep + '_merged_ct' + j)) is True:
                        print(j)
                        arcpy.MakeFeatureLayer_management(outputGDB + os.sep + '_merged_ct' + j, "temp")
                        arcpy.SelectLayerByLocation_management("temp", "within", output_buffer, '', 'NEW_SELECTION')
                        arcpy.CopyFeatures_management("temp", bufferGDB + os.sep + j + '_inbuffer_' + i)
                        arcpy.Delete_management('temp', 'lyr')
                        merge_list.append(bufferGDB + os.sep + j + '_inbuffer_' + i)

        arcpy.Merge_management(merge_list, bufferGDB + os.sep + 'buffer_road')


    def remove_in_buffer_feature(rdlevel_list,rdlevel):
        merge_list1 = []
        merge_list1.extend([outputGDB + os.sep + '_merged_ct' + i for i in rdlevel_list])
        arcpy.Merge_management(merge_list1, bufferGDB + os.sep + 'merge_road' + rdlevel)
        arcpy.MakeFeatureLayer_management(bufferGDB + os.sep + 'merge_road' + rdlevel, 'temp')

        arcpy.SelectLayerByLocation_management('temp', 'ARE_IDENTICAL_TO', bufferGDB + os.sep + 'buffer_road')
        arcpy.SelectLayerByAttribute_management('temp', "SWITCH_SELECTION")

        arcpy.CopyFeatures_management('temp', bufferGDB + os.sep + 'merge_road_v2' + rdlevel)
        arcpy.Delete_management('temp')


    def select_rd_class(rd_list,rdlevel):

        bufferGDB_v2 = rawDir + os.sep + "rd_buffer_v2.gdb"
        arcpy.MakeFeatureLayer_management(bufferGDB + os.sep + 'merge_road_v2' + rdlevel, 'temp')
        # rd_list = ['rd00', 'rd01', 'rd02', 'rd03', 'rd04', 'rd05']
        for rd in rd_list:
            print(rd)
            arcpy.SelectLayerByAttribute_management('temp', "NEW_SELECTION", "rdClass = '" + rd + "'")
            # arcpy.CopyFeatures_management('temp', bufferGDB_v2 + os.sep + 'v2_rd0' + str(rd_list.index(rd)) + rdlevel)
            arcpy.CopyFeatures_management('temp', bufferGDB_v2 + os.sep + 'v2_' + rd + rdlevel)
            arcpy.Buffer_analysis(bufferGDB_v2 + os.sep + 'v2_' + rd + rdlevel, \
                                  bufferGDB_v2 + os.sep + 'v2_' + rd + '_buffer' + rdlevel, '30 Meters')

        arcpy.Delete_management('temp')


    def create_rdclass_buffer_v2(rd_list,rdlevel):
        # rd_list = ['rd00', 'rd01', 'rd02', 'rd03', 'rd04', 'rd05']
        for rd in rd_list:
            print(rd)
            rd_path = rawDir + os.sep + "rd_buffer_v2.gdb" + os.sep + 'v2_' + rd + rdlevel
            output_dissolve_path = rawDir + os.sep + "rd_buffer_v2.gdb" + os.sep + 'v2_' + rd + '_dissolve' + rdlevel
            output_buffer_path = rawDir + os.sep + "rd_buffer_v2.gdb" + os.sep + 'v2_' + rd + '_buffer' + rdlevel
            output_sj_path = rawDir + os.sep + "rd_buffer_v2.gdb" + os.sep + 'v2_' + rd + '_sj' + rdlevel
            output_select_sj_path = rawDir + os.sep + "rd_buffer_v2.gdb" + os.sep + 'v2_' + rd + '_sj_select' + rdlevel
            output_final = rawDir + os.sep + "rd_buffer_v2.gdb" + os.sep + 'v2_' + rd + '_final' + rdlevel
            arcpy.MakeFeatureLayer_management(rd_path, 'temp')
            arcpy.Dissolve_management('temp', output_dissolve_path, ['rdClass', 'PathName'], "", "SINGLE_PART", '')
            arcpy.Buffer_analysis(output_dissolve_path, output_buffer_path, '30 Meters')

            arcpy.SpatialJoin_analysis(output_buffer_path, output_dissolve_path, output_sj_path, '', "", "", "CONTAINS")
            arcpy.MakeFeatureLayer_management(output_sj_path, 'temp2')
            arcpy.SelectLayerByAttribute_management('temp2', "NEW_SELECTION", "Join_Count > 2")
            arcpy.CopyFeatures_management('temp2', output_select_sj_path)
            arcpy.Delete_management('temp2')

            unique_rd_id = unique_values(output_select_sj_path, 'TARGET_FID')
            if unique_rd_id:
                print('unique_rd_id exists')
                arcpy.MakeFeatureLayer_management(output_dissolve_path, 'temp3')
                arcpy.SelectLayerByLocation_management('temp3', 'WITHIN', output_select_sj_path)
                arcpy.SelectLayerByAttribute_management('temp3', "REMOVE_FROM_SELECTION", "OBJECTID IN (" + str(unique_rd_id)[1:-1] + ')')
                arcpy.SelectLayerByAttribute_management('temp3', "SWITCH_SELECTION")
                arcpy.CopyFeatures_management('temp3', output_final)
                arcpy.Delete_management('temp3')
            else:
                print('unique_rd_id not exists')
                arcpy.CopyFeatures_management(output_dissolve_path, output_final)


    def merge_final(rd_list,rdlevel):
        merge_list = []
        gdbDir = rawDir + os.sep + "rd_buffer_v2.gdb"
        # merge_list.extend([gdbDir + os.sep + 'v2_rd0' + str(i) + '_final' for i in range(6)])
        merge_list.extend([gdbDir + os.sep + 'v2_' + str(i) + '_final' + rdlevel for i in rd_list])
        arcpy.Merge_management(merge_list, gdbDir + os.sep + 'merge_road_v3' + rdlevel)

    ### execute by order


    start = time.clock()
    ### fill in the function we want to execute
    create_buffer_rdclass()
    # remove_in_buffer_feature(['rd00', 'rd02'],'_gaosu')
    remove_in_buffer_feature(['rd01','rd03', 'rd04', 'rd05'],'_ungaosu')
    arcpy.CreateFileGDB_management(rawDir, "rd_buffer_v2.gdb", "10.0")
    # select_rd_class(['rd00', 'rd02'],'_gaosu')
    select_rd_class(['rd01','rd03', 'rd04', 'rd05'],'_ungaosu')
    # create_rdclass_buffer_v2(['rd00', 'rd02'],'_gaosu')
    create_rdclass_buffer_v2(['rd01','rd03', 'rd04', 'rd05'],'_ungaosu')
    # merge_final(['rd00', 'rd02'],'_gaosu')
    merge_final(['rd01','rd03', 'rd04', 'rd05'],'_ungaosu')
    elapsed = (time.clock() - start)
    print("Step 3 Time used:", elapsed, ' finished!')

    # <---------------------------------------------- STEP 4 -------------------------------------------------------------->
    bufferResultGDB = rawDir + os.sep + r"rd_buffer_v2.gdb"
    simpResultGDB = rawDir + os.sep + city + r'_road_simp_result.gdb'

    rd_class = ['高速公路', '国道', '都市高速路', '省道', '县道', '乡镇道路', '九级路', '行人道路']
    rd_class_EN = ['rd00', 'rd01', 'rd02', 'rd03', 'rd04', 'rd05', 'rd06', 'rd07']
    arcpy.env.workspace = rawDir + os.sep + r"rd_buffer_v2.gdb"


    def merge_multi(rd_list, rdlevel):
        merge_list = []
        gdbDir = simpResultGDB
        merge_list.extend([gdbDir + os.sep + '_multi' + str(i) for i in rd_list])
        # merge_list.extend([gdbDir + os.sep + '_multird0' + str(i) for i in range(6)])
        arcpy.Merge_management(merge_list, gdbDir + os.sep + '_multi_merged' + rdlevel)
        arcpy.env.workspace = rawDir + os.sep + r"rd_buffer_v2.gdb"
        arcpy.CopyFeatures_management(gdbDir + os.sep + '_multi_merged' + rdlevel, '_multi_merged' + rdlevel)


    def treat_the_line(rdlevel):
        arcpy.ExtendLine_edit('_multi_merged' + rdlevel, "50 meters", "FEATURE")
        arcpy.FeatureToLine_management('merge_road_v3' + rdlevel, 'merge_road_treated' + rdlevel)


    def attach_sublane_attr(rdlevel):
        # treat the multiparts roads first
        arcpy.CopyFeatures_management('_multi_merged' + rdlevel, '_multi_f2l_orgrd' + rdlevel)
        arcpy.FeatureToLine_management('_multi_f2l_orgrd' + rdlevel, '_f2l_orgrd' + rdlevel)
        arcpy.DeleteField_management('_f2l_orgrd' + rdlevel, "length")
        arcpy.AddField_management('_f2l_orgrd' + rdlevel, "length", "FLOAT")
        arcpy.CalculateField_management('_f2l_orgrd' + rdlevel, "length", "!shape.length@meters!", "PYTHON_9.3")
        arcpy.Select_analysis('_f2l_orgrd' + rdlevel, '_f2l_orgrd2' + rdlevel, 'length>=25')

        # treat center line
        arcpy.CopyFeatures_management('merge_road_treated' + rdlevel, '_merged_f2l' + rdlevel)
        arcpy.FeatureToLine_management('_merged_f2l' + rdlevel, '_f2l' + rdlevel)
        arcpy.DeleteField_management('_f2l' + rdlevel, "uniqueID")
        arcpy.AddField_management('_f2l' + rdlevel, "uniqueID", "INTEGER")
        arcpy.CalculateField_management('_f2l' + rdlevel, "uniqueID", '!OBJECTID!', "PYTHON_9.3")

        # create the center point to create buffer and then capture multi part attr
        arcpy.FeatureVerticesToPoints_management('_f2l' + rdlevel, '_midpt' + rdlevel, 'MID')
        arcpy.Buffer_analysis('_midpt' + rdlevel, '_midptBuff30' + rdlevel, '30 Meters')

        # 怎么感觉像是多余的操作？
        arcpy.DeleteField_management('_f2l_orgrd2' + rdlevel, "CarNum")
        arcpy.AddField_management('_f2l_orgrd2' + rdlevel, "CarNum", "INTEGER")
        arcpy.CalculateField_management('_f2l_orgrd2' + rdlevel, "CarNum", '!LaneNum!', "PYTHON_9.3")

        # spatial join
        fieldmappings = arcpy.FieldMappings()
        fieldmappings.addTable('_midptBuff30' + rdlevel)
        fieldmappings.addTable('_f2l_orgrd2' + rdlevel)
        pop1990FieldIndex = fieldmappings.findFieldMapIndex("CarNum")
        fieldmap = fieldmappings.getFieldMap(pop1990FieldIndex)
        field = fieldmap.outputField
        field.name = "CarNum"
        field.aliasName = "CarNum"
        fieldmap.outputField = field
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(pop1990FieldIndex, fieldmap)
        arcpy.SpatialJoin_analysis('_midptBuff30' + rdlevel, '_f2l_orgrd2' + rdlevel, '_sj1' + rdlevel, 'JOIN_ONE_TO_ONE',
                                   '', fieldmappings, 'INTERSECTS')
        arcpy.JoinField_management('_f2l' + rdlevel, "uniqueID", '_sj1' + rdlevel, "uniqueID", ['CarNum'])

        # estimate width with carNum
        arcpy.DeleteField_management('_f2l' + rdlevel, "RdWid")
        arcpy.AddField_management('_f2l' + rdlevel, "RdWid", "FLOAT")
        arcpy.CalculateField_management('_f2l' + rdlevel, "RdWid", '!CarNum!*3.5/2+25', "PYTHON_9.3")
        arcpy.CopyFeatures_management('_f2l' + rdlevel, '_f2l_final_result' + rdlevel)


    # 如果对所有路段进行dissolve

    start = time.clock()
    ### fill in the function we want to execute
    # merge_multi(['rd00', 'rd02'], '_gaosu')
    merge_multi(['rd03', 'rd04', 'rd05'], '_ungaosu')
    # treat_the_line('_gaosu')
    treat_the_line('_ungaosu')
    # attach_sublane_attr('_gaosu')
    attach_sublane_attr('_ungaosu')
    elapsed = (time.clock() - start)
    print("Step 4 Time used:", elapsed, ' finished!')


    # <---------------------------------------------- STEP 5 -------------------------------------------------------------->
    # Copy result to a new directory which named by city
    # Create target Directory if don't exist
    dirName = r'G:\00_BaseData\03_RoadSimp\01_Result_Road_Simp\\' + city
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:
        print("Directory " , dirName ,  " already exists")

    arcpy.Copy_management(rawDir + os.sep + r"rd_buffer_v2.gdb", dirName + os.sep + r"rd_buffer_v2.gdb")
    env.workspace = dirName + os.sep + r"rd_buffer_v2.gdb"
    fclist = arcpy.ListFeatureClasses()
    for fc in fclist:
        if fc == '_f2l_final_result_ungaosu':
            fclist.remove(fc)
    for i in fclist:
        print('Delete feature class: ' + str(i))
        arcpy.Delete_management(i)
