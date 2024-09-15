from qgis.core import *
import processing

import os 

path = r'D:\Project\pan_qaidam_yardang\result'
grid_ids = os.listdir(path)
print(grid_ids)



for i in grid_ids:
    inputname = path + '\\' + str(i) + '\\result\\' + 'point_' + str(i) + '.shp'
    joinname = path + '\\' + str(i) + '\\result\\' + 'bounding_' + str(i) + '.shp'
    outputname = path + '\\' + str(i) + '\\result\\' + 'join_' + str(i) + '.shp'
    
    if not os.path.exists(inputname) or not os.path.exists(joinname):
        print(i,"Check files")
        break
    else:
        
        if os.path.exists(outputname):
            print(i,'generated already')
            continue
        else:
            processing.run("native:joinattributesbylocation", {'INPUT':inputname,'PREDICATE':[2,5],
            'JOIN':joinname,'JOIN_FIELDS':['width','height','angle','area_1','perimeter','ratio'],
            'METHOD':2,'DISCARD_NONMATCHING':False,'PREFIX':'','OUTPUT':outputname})
            print(i,'finished')