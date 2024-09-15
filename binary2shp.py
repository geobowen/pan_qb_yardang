import cv2
from osgeo import gdal, ogr, osr
import os

def raster2shp(mask_path, image_path, strVectorFile):

    img0 = cv2.imread(mask_path)
    img1 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    ret, img2 = cv2.threshold(img1, 200, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    if not contours:
        print("No target founded")
        return None,None
    else:
        inimg = gdal.Open(image_path)
        prj = osr.SpatialReference()
        prj.ImportFromWkt(inimg.GetProjection())
        Geoimg = inimg.GetGeoTransform()

        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")  # 支持中文路径
        gdal.SetConfigOption("SHAPE_ENCODING", "CP936")      # 属性表字段支持中文

        #strVectorFile = "E:/qgsgoogle.shp"

        ogr.RegisterAll()   #注册所有驱动
        strDriverName = "ESRI Shapefile"
        oDriver = ogr.GetDriverByName(strDriverName)
        if oDriver == None:
            print("驱动不可用！")

        oDS = oDriver.CreateDataSource(strVectorFile)   #创建数据源
        if oDS == None:
            print("创建文件失败！")

        srs = osr.SpatialReference()  #创建空间参考
        srs.ImportFromEPSG(3857)
        papszLCO = []

        #创建多边形图层，"TestPolygon"->属性表名
        oLayer = oDS.CreateLayer("TestPolygon", srs, ogr.wkbPolygon, papszLCO)
        if oLayer == None:
            print("图层创建失败！")



        '''下面添加矢量数据，属性表数据、矢量数据坐标'''    
        oFieldID = ogr.FieldDefn("FieldID", ogr.OFTInteger)  # 创建一个叫FieldID的整型属性
        oLayer.CreateField(oFieldID, 1)

        oDefn = oLayer.GetLayerDefn()   #定义要素
        gardens = ogr.Geometry(ogr.wkbMultiPolygon)  # 定义总的多边形集
        i = 0
        for contour in contours:
        #area = cv2.contourArea(contour)
        #if area > 100:  # 面积大于n才保存

            box1 = ogr.Geometry(ogr.wkbLinearRing)
            i += 1
            for point in contour:
                #将像素坐标转地理坐标
                x_col = Geoimg[0] + Geoimg[1] * (float(point[0, 0])) + (float(point[0, 1])) * Geoimg[2]
                y_row = Geoimg[3] + Geoimg[4] * (float(point[0, 0])) + (float(point[0, 1])) * Geoimg[5]
                
                
                box1.AddPoint(x_col, y_row)   #注意！！！顺序
            oFeatureTriangle = ogr.Feature(oDefn)
            oFeatureTriangle.SetField(0, i)
            garden1 = ogr.Geometry(ogr.wkbPolygon)
            garden1.AddGeometry(box1)
            gardens.AddGeometry(garden1)
        gardens.CloseRings()

        geomTriangle = ogr.CreateGeometryFromWkt(str(gardens))
        oFeatureTriangle.SetGeometry(geomTriangle)
        oLayer.CreateFeature(oFeatureTriangle)
        oDS.Destroy()

        xpixel = Geoimg[1]
        ypixel = Geoimg[5]

        return xpixel,ypixel

def shp2area(strShpFile,xpixel,ypixel):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(strShpFile, 1)
    layer = dataSource.GetLayer()
    
    src_srs = layer.GetSpatialRef()
    tgt_srs = osr.SpatialReference()
    tgt_srs.ImportFromEPSG(3857)
    transform = osr.CoordinateTransformation(src_srs, tgt_srs)
    
    new_field = ogr.FieldDefn("Area", ogr.OFTReal)
    new_field.SetWidth(32)
    new_field.SetPrecision(2)
    layer.CreateField(new_field)
    for feature in layer:
        geom = feature.GetGeometryRef()
        geom2 = geom.Clone()
        geom2.Transform(transform)
        #area = geom.GetArea()
        area = geom2.GetArea()
        # 矢量面积
        #feature.SetField("Area", abs(area/xpixel/ypixel))
        feature.SetField("Area", area)
        #feature.SetField("Area2", area2)
        layer.SetFeature(feature)
    print("Done!")

dataset_root_path = "E:/data/629/18/"
img_folder = dataset_root_path + "629"
mask_folder = dataset_root_path + "binary"

strVectorFile_folder = dataset_root_path + "vec"
strShpFile_folder = dataset_root_path + "shp"

if not os.path.exists(strVectorFile_folder):
    os.mkdir(strVectorFile_folder)
    print("strVectorFilePath created")

if not os.path.exists(strShpFile_folder):
    os.mkdir(strShpFile_folder)
    print("strShpFilePath created")

imglist = os.listdir(img_folder)

for i in range(0, len(imglist)):
    path = os.path.join(img_folder, imglist[i])
    if os.path.isfile(path):
        _ = next(os.walk(img_folder))
        filestr = imglist[i].split(".")[0]
        image_path = os.path.join(img_folder, imglist[i])
        maskname = filestr + ".png"
        mask_path = os.path.join(mask_folder, maskname)
        vecname = filestr + ".shp"
        strVectorFile = os.path.join(strVectorFile_folder, vecname)
        xpixel, ypixel = raster2shp(mask_path, image_path, strVectorFile)
        if xpixel:
            strShpFile = os.path.join(strShpFile_folder, vecname)
            strTemp = "ogr2ogr -f \"ESRI Shapefile\" -explodecollections " + strShpFile + " " + strVectorFile
            print(strTemp)
            os.system(strTemp)
            shp2area(strShpFile, xpixel, ypixel)
            print("Number %i is Done" %i)
        else:
            continue



#image_path = "E:/binary/test.tif"# 原始有地理坐标的图片
#mask_path = "E:/binary/test.png"# 分割结果图
#strShpFile = "E:/binary/1228explode.shp"# 分割结果图转为包含每个矢量的面积的矢量文件

#strVectorFile = "E:/1230.shp"# 分割结果图转矢量文件

#xpixel, ypixel = raster2shp(mask_path, image_path, strVectorFile)

#矢量炸开
#strTemp = "ogr2ogr -f \"ESRI Shapefile\" -explodecollections " + strShpFile + " " + strVectorFile
#print(strTemp)
#os.system(strTemp)
#shp2area(strShpFile, xpixel, ypixel)



