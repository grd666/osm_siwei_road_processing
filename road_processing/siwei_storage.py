# -*- coding: utf-8 -*-
# 将四维路网处理的输出结果集中储存（处理脚本的直接输出路径复杂且分散）

import arcpy
import os
import sys
from arcpy import env

arcpy.env.overwriteOutput = True
# root为两个四维单线化脚本的输出文件夹路径，outgdb为自建的新结果路径
root_1 = r'E:\citydna\TOD\code\data_review\road\road_processing\siwei_road_simp\01_Result_Motorway_Simp'
root_2 = r'E:\citydna\TOD\code\data_review\road\road_processing\siwei_road_simp\01_Result_Road_Simp'
outgdb_1 = r'E:\citydna\TOD\code\data_review\road\road_processing\siwei_motorway_simp.gdb'
outgdb_2 = r'E:\citydna\TOD\code\data_review\road\road_processing\siwei_road_simp.gdb'

citylist = ['wuxi','changzhou','suzhou','wenzhou','jiaxing','shaoxing','wuhu','foshan','dongguan']

for city in citylist:
    print(city)

    # 快速路处理输出结果集中
    env.workspace = root_1 + os.sep + city + '_Motorway_final.gdb'
    arcpy.Merge_management(['rd00_motor_final','rd02_motor_final'], 'temp')
    arcpy.CopyFeatures_management('temp', outgdb_1 + os.sep + city + '_siwei_motor')
    arcpy.Delete_management('temp')

    # 非快速路处理输出结果集中
    env.workspace = root_2 + os.sep + city + os.sep + 'rd_buffer_v2.gdb'
    arcpy.CopyFeatures_management('_f2l_final_result_ungaosu', outgdb_2 + os.sep + city + '_siwei_road')







