# coding:utf-8
from PIL import Image
import random
import os
import configparser
import json

def getImageObj(file):
    im = Image.open(file)
    if im.mode != "RGBA" and im.mode != "RGB":
        print("error:不是RGB/RGBA图片", im.mode, file)
        return None
    pix = im.load()
    pixel = pix[0, 0]
    #  主要有三种类型，rgb／rgba／colormap
    if type(pixel) is not tuple:
        print("error:无法获取RGB值", pixel, file)
        return None
    else:
        return im

def randomCoordinate(w,h):
    x = random.randint(0, w - 1)
    y = random.randint(0, h - 1)
    return (x,y)

def randomCoordinateNum(w,h,num):
    if w*h<num:
        print("error:不合法的输入")
        return None
    arr = []
    while(True):
        x, y = randomCoordinate(w, h)
        if (x, y) not in arr:
            arr.append((x, y))
            if len(arr) == num:
                return arr
    return None

def restore(file,im,pixs):
    oldArr = getRecordJSON(file)
    if oldArr == None or len(oldArr) == 0:
        return
    for old in oldArr:
        x,y = old["x"],old["y"]
        rbgIndex = old["rgb"]
        value = old["value"]
        pixellist = list(pixs[x, y])
        pixellist[rbgIndex] = pixellist[rbgIndex] - value
        im.putpixel([x,y],tuple(pixellist))
    setRecordJSON(file, None)

def modify(file,im,pixs):
    width = im.size[0]
    height = im.size[1]
    xyArr = randomCoordinateNum(width,height,modifyNum)
    json=[]
    for x,y in xyArr:
        pixellist = list(pixs[x,y])
        rbgIndex = random.randint(0,2)
        pixelvalue = pixellist[rbgIndex]
        value = 1
        if pixelvalue > 125:
            value = -1
        pixellist[rbgIndex] = pixelvalue + value
        im.putpixel([x, y],tuple(pixellist))
        json.append({"x":x,"y":y,"rgb":rbgIndex,"value":value})
    setRecordJSON(file,json)

def handleFile(file):
    im = getImageObj(file)
    if im == None:
        return
    pixs = im.load()
    restore(file,im,pixs)
    if restoreAndModify == 1:
        modify(file,im,pixs)
    im.save(file, im.format)
    im.close()
    return

def scanningdir(dir):
    files = []
    for parent, dirnames, filenames in os.walk(dir):
        for file in filenames:
            path = parent + "/" + file
            houzhui = path[-4:]
            if houzhui == ".png" or houzhui == ".jpg":
                files.append(path)
    filesCNT = len(files)
    for i in range(0,filesCNT):
        print("正在处理%s/%s    %s"%(i+1,filesCNT,files[i]))
        handleFile(files[i])

def getRecordJSON(key):
    if config.has_option(sectionName,key):
        obj = config.get(sectionName, key)
        jsonData = json.loads(obj)
        # print("读取json文件:", jsonData)
        return jsonData

def setRecordJSON(key,jsonData):
    if jsonData == None:
        config.remove_option(sectionName, key)
        with open(recordPath, 'w') as f:
            config.write(f)
    else:
        str = json.dumps(jsonData)
        config.set(sectionName, key, str)
        with open(recordPath, 'w') as f:
            config.write(f)
    # print("写入json文件:", str)

def getRecordTxt():
    pyscriptPath = os.path.abspath(__file__)
    pyscriptname = pyscriptPath.split("/")[-1]
    pyscriptDir = os.path.dirname(pyscriptPath)
    recordPath = pyscriptDir + "/" + pyscriptname.split(".")[0] + "_record.ini"
    if os.path.exists(recordPath) == False:
        with open(recordPath, 'w') as f:
            config.read(recordPath)
            config.add_section(sectionName)
            config.write(f)
            return recordPath
    else:
        config.read(recordPath)
    return recordPath


# 1：恢复之前的像素值，并修改   0：只恢复
restoreAndModify = 1
# 要修改的目录／文件
imgPath = "/Users/apple/Desktop/修改像素/changeImagePixel/Assets.xcassets"
# 修改多少个像素点
modifyNum = 5

if __name__ == '__main__':
    config = configparser.ConfigParser()
    sectionName = "record"
    recordPath = getRecordTxt()
    if os.path.isdir(imgPath):
        scanningdir(imgPath)
    elif os.path.isfile(imgPath):
        handleFile(imgPath)