import cv2
import numpy as np
import random
import math
import copy
import os
import fnmatch
s = open("s.txt", 'r', encoding='UTF-8')
lines = s.readlines()
l = {}
img1 = cv2.imread('img.png', cv2.IMREAD_COLOR)
for line in lines:
    l[line.strip().split(":")[0]] = line.strip().split(":")[1]
s.close()
imgs0 = []
for file in os.listdir('img'):
    if fnmatch.fnmatch(file, '*.png'):
        imgs0.append(cv2.imread('img/'+file, cv2.IMREAD_UNCHANGED))
imgx = l.get('크기', 'a-a').split('-')[0]
imgy = l.get('크기', 'a-a').split('-')[1]
height, width, channel = img1.shape
if imgx == 'a':
    imgx = width
if imgy == 'a':
    imgy = height
bg = cv2.mean(img1)
bgr = l.get('바탕', 'a-a-a').split('-')[0]
bgg = l.get('바탕', 'a-a-a').split('-')[1]
bgb = l.get('바탕', 'a-a-a').split('-')[2]
if bgr == 'a':
    bgr = bg[0]
if bgg == 'a':
    bgg = bg[1]
if bgb == 'a':
    bgb = bg[2]
img0 = np.full((int(imgx), int(imgy), 4), (int(bgr), int(bgg), int(bgb), 255), dtype=np.uint8)
img1 = cv2.resize(img1, dsize=(int(imgy), int(imgx)), interpolation=cv2.INTER_LINEAR)
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2BGRA)
a = int((float(imgx) + float(imgy)) * 0.01)
def xs(im0, im1):
    im02 = copy.deepcopy(im0)
    mask = im1[:, :, 3]
    cv2.copyTo(im1, mask, im02)
    return im02
def sc(b0, b1):
    img001 = cv2.absdiff(b0, b1)
    img001 = cv2.cvtColor(img001, cv2.COLOR_BGRA2GRAY)
    return cv2.mean(img001)[0]
def aa01():
    global o
    for k0 in range(len(o)):
        i = o[k0]
        for j in range(int(l.get('자식', 8))):
            o0 = {}
            o0["posX"] = i["posX"] + int(random.randrange(int(l.get('오차', 12)) * -1, int(l.get('오차', 12)) + 1) / 100 * int(imgx))
            o0["posY"] = i["posY"] + int(random.randrange(int(l.get('오차', 12)) * -1, int(l.get('오차', 12)) + 1) / 100 * int(imgy))
            o0["sizeX"] = i["sizeX"] + int(random.randrange(int(l.get('오차', 12)) * -1, int(l.get('오차', 12)) + 1) / 100 * int(imgx))
            o0["sizeY"] = i["sizeY"] + int(random.randrange(int(l.get('오차', 12)) * -1, int(l.get('오차', 12)) + 1) / 100 * int(imgy))
            o0["rot"] = i["rot"] + int(random.randrange(int(l.get('오차', 12)) * -1, int(l.get('오차', 12)) + 1) * 3.59)
            o0["color"] = i["color"]
            o0["img"] = i["img"]
            t_img = cv2.resize(imgs0[o0["img"]], dsize=(int(imgx), int(imgy)), interpolation=cv2.INTER_LINEAR)
            m00 = cv2.getRotationMatrix2D((o0["posX"], o0["posY"]), o0["rot"], 1)
            m01 = np.float32([[o0["sizeX"] / int(imgx), 0, 0],[0, o0["sizeY"] / int(imgy),0]])
            m02 = np.float32([[1, 0, o0["posX"] - (o0["sizeX"]/2)],[0, 1, o0["posY"] - (o0["sizeY"]/2)]])
            re0 = cv2.warpAffine(t_img, m01, (int(imgx), int(imgy)))
            re0 = cv2.warpAffine(re0, m02, (int(imgx), int(imgy)))
            re0 = cv2.warpAffine(re0, m00, (int(imgx), int(imgy)))
            mask1 = cv2.inRange(re0, np.array([128, 128, 128, 128], dtype=np.int16), np.array([255, 255, 255, 255], dtype=np.int16))
            re0[mask1 > 0] = o0["color"]
            o0["sc"] = sc(img1, xs(img0, re0))
            o.append(o0)
    o = sorted(o, key=lambda k: k['sc'])[0:int(l.get('순위', 128))]
for l01 in range(int(l.get('최대', 800))):
    o = []
    for i in range(int(l.get('순위', 128)) * int(l.get('자식', 8))):
        o.append({})
        o[i]["posX"] = random.randrange(a,int(imgx) + 1)
        o[i]["posY"] = random.randrange(a,int(imgy) + 1)
        o[i]["sizeX"] = random.randrange(a,int(imgx) + 1)
        o[i]["sizeY"] = random.randrange(a,int(imgy) + 1)
        o[i]["rot"] = random.randrange(1, 360)
        o[i]["img"] = random.randrange(0, len(imgs0))
        t_img = cv2.resize(imgs0[o[i]["img"]], dsize=(int(imgx), int(imgy)), interpolation=cv2.INTER_LINEAR)
        m00 = cv2.getRotationMatrix2D((o[i]["posX"], o[i]["posY"]), o[i]["rot"], 1)
        m01 = np.float32([[o[i]["sizeX"] / int(imgx), 0, 0],[0, o[i]["sizeY"] / int(imgy),0]])
        m02 = np.float32([[1, 0, o[i]["posX"] - (o[i]["sizeX"]/2)],[0, 1, o[i]["posY"] - (o[i]["sizeY"]/2)]])
        re0 = cv2.warpAffine(t_img, m01, (int(imgx), int(imgy)))
        re0 = cv2.warpAffine(re0, m02, (int(imgx), int(imgy)))
        re0 = cv2.warpAffine(re0, m00, (int(imgx), int(imgy)))
        size0 = (o[i]["sizeX"]/100) * (o[i]["sizeY"]/100)
        r1 = size0 / ((float(imgx)/100) * (float(imgy)/100))
        mask9 = re0[:, :, 3]
        img2 = copy.deepcopy(img1)
        img2[mask9 == 0] = 0
        img2[:, :, 3] = 255
        c = cv2.mean(img2)
        o[i]["color"] = (c[0] / r1, c[1] / r1, c[2] / r1, c[3])
        mask1 = cv2.inRange(re0, np.array([128, 128, 128, 128], dtype=np.int16), np.array([255, 255, 255, 255], dtype=np.int16))
        re0[mask1 > 0] = o[i]["color"]
        o[i]["sc"] = sc(img1, xs(img0, re0))
    o = sorted(o, key=lambda k: k['sc'])[0:int(l.get('순위', 128))]
    for i in range(int(l.get('반복', 4))):
        aa01()
    o00 = o[0]
    tmp_img = cv2.resize(imgs0[o00["img"]], dsize=(int(imgx), int(imgy)), interpolation=cv2.INTER_LINEAR)
    m00 = cv2.getRotationMatrix2D((o00["posX"], o00["posY"]), o00["rot"], 1)
    m01 = np.float32([[o00["sizeX"] / int(imgx), 0, 0],[0, o00["sizeY"] / int(imgy),0]])
    m02 = np.float32([[1, 0, o00["posX"] - (o00["sizeX"]/2)],[0, 1, o00["posY"] - (o00["sizeY"]/2)]])
    re0 = cv2.warpAffine(tmp_img, m01, (int(imgx), int(imgy)))
    re0 = cv2.warpAffine(re0, m02, (int(imgx), int(imgy)))
    re0 = cv2.warpAffine(re0, m00, (int(imgx), int(imgy)))
    mask2 = cv2.inRange(re0, np.array([128, 128, 128, 128], dtype=np.int16), np.array([255, 255, 255, 255], dtype=np.int16))
    re0[mask2 > 0] = o00["color"]
    img0 = xs(img0, re0)
    print(o00)
    cv2.imwrite("img0.png", img0)
