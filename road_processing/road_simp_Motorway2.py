# Date: 2019/04/15
# Author: ZQY
# Content: Simplify motorway
# Email: qingyuanzhang@citydnatech.com

import arcpy
import os
from arcpy import env
import time

env.overwriteOutput = True

# citylist = [u'beijing', u'changchun', u'changsha',u'chengdu', u'chongqing', u'dalian', u'dongguan', u'foshan', u'fuzhou', u'guangzhou', u'guiyang', u'hangzhou', u'harbin', u'hefei', u'kunming', u'nanchang', u'nanjing', u'nanning', u'ningbo', u'qingdao', u'shanghai', u'shenyang', u'shenzhen', u'shijiazhuang', u'suzhou', u'tianjin', u'wuhan', u'wuxi', u'xiamen', u'xian', u'zhengzhou']
citylist = ['tianjin', 'shanghai', 'chongqing', 'shijiazhuang', 'tangshan', 'taiyuan', 'huhehaote', 'haerbin',
            'changchun', 'shenyang', 'dalian', 'jinan', 'qingdao', 'nanjing', 'xuzhou', 'hefei', 'hangzhou', 'ningbo',
            'quzhou', 'fuzhou', 'xiamen', 'nanchang', 'ganzhou', 'zhengzhou', 'luoyang', 'wuhan', 'huangshi',
            'changsha', 'guangzhou', 'shenzhen', 'nanning', 'kunming', 'guiyang', 'chengdu', 'xian', 'lanzhou',
            'yinchuan', 'wulumuqi']

citylist = ['eerduosi', 'chifeng', 'tongliao']

for city in citylist:
    print(city)
    env.workspace = r'G:\00_BaseData\03_RoadSimp\\' + city + '_shapes.gdb'
    fc_inpath = r'G:\00_BaseData\03_RoadSimp\\' + city + '_shapes.gdb'
    arcpy.CreateFileGDB_management(r'G:\00_BaseData\03_RoadSimp\01_Result_Motorway_Simp', city + '_motorway.gdb', '10.0')
    outgdb = r'G:\00_BaseData\03_RoadSimp\01_Result_Motorway_Simp\\' + city + '_motorway.gdb'
    fclist = [u'rd00', u'rd02']
    for fc in fclist:
        if "inter" not in fc:
            print fc
            arcpy.Select_analysis(fc,outgdb + os.sep + fc,"rdClass = 'rd00' OR rdClass = 'rd02'")
            tempfc = outgdb + os.sep + fc
            arcpy.DeleteField_management(tempfc, "merge")
            arcpy.AddField_management(tempfc, "merge", "INTEGER")
            arcpy.CalculateField_management(tempfc, "merge", 1, "PYTHON_9.3")
            arcpy.MakeFeatureLayer_management(tempfc, "temp_remove")
            arcpy.MultipartToSinglepart_management("temp_remove", "temp_remove_singlepart")
            arcpy.MergeDividedRoads_cartography("temp_remove_singlepart", 'merge', '30 meters', outgdb + os.sep + fc + '_motor')
            arcpy.Delete_management("temp_remove")
            arcpy.Delete_management("temp_remove_singlepart")

    env.workspace = r'G:\00_BaseData\03_RoadSimp\01_Result_Motorway_Simp\\' + city + '_motorway.gdb'
    fclist = arcpy.ListFeatureClasses()
    arcpy.CreateFileGDB_management(r'G:\00_BaseData\03_RoadSimp\01_Result_Motorway_Simp', city + '_Motorway_final.gdb', '10.0')
    outgdb = r'G:\00_BaseData\03_RoadSimp\01_Result_Motorway_Simp\\' + city + '_Motorway_final.gdb'
    for fc in fclist:
        if 'motor' in fc:
            print fc
            arcpy.Select_analysis(fc,outgdb + os.sep + fc + '_select',"Kind = '0002|000c' OR Kind = '0102|010c' OR Kind = '0002|0008|000c' OR Kind = '0102|0108|010c' OR Kind = '010c' OR Kind = '000c' OR Kind = '000c|000f' OR Kind = '0102|0103|010c' OR Kind = '0102|010c|010f' OR Kind = '0002|0003|000c' OR Kind = '0002|000c|000f'")
            tempfc = outgdb + os.sep + fc + '_select'
            arcpy.ExtendLine_edit(tempfc, '500 Meters')
            arcpy.DeleteField_management(tempfc, "merge")
            arcpy.AddField_management(tempfc, "merge", "INTEGER")
            arcpy.CalculateField_management(tempfc, "merge", 1, "PYTHON_9.3")
            arcpy.MultipartToSinglepart_management(tempfc, outgdb + os.sep + fc + '_single')
            arcpy.MakeFeatureLayer_management(outgdb + os.sep + fc + '_single', "temp_remove")
            arcpy.MergeDividedRoads_cartography("temp_remove", 'merge', '30 meters', outgdb + os.sep + fc + '_final')
            arcpy.Delete_management("temp_remove")
