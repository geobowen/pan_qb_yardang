from qgis.core import *
import processing

import os 

path = r'D:\Project\pan_qaidam_yardang\result'
grid_ids = os.listdir(path)
print(grid_ids)



for i in grid_ids:
    inputname = path + '\\' + str(i) + '\\result\\' + 'merge_' + str(i) + '.shp'
    outputname = path + '\\' + str(i) + '\\result\\' + 'point_' + str(i) + '.shp'
    if os.path.exists(outputname):
        print(i,'generated already')
        continue
    else:
        processing.run("native:pointonsurface", {'INPUT':inputname,'ALL_PARTS':True,'OUTPUT':outputname})
        print(i,'finished')