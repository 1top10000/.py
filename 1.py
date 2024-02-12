import cv2
import numpy as np
import random
import math
s = open("s.txt", 'r', encoding='UTF-8')
lines = s.readlines()
l = {}
img1 = cv2.imread('img.png', cv2.IMREAD_COLOR)
for line in lines:
    l[line.strip().split(":")[0]] = line.strip().split(":")[1]
s.close()
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
img0 = np.full((int(imgx), int(imgy), 4), (int(bgr), int(bgg), int(bgb), 1), dtype=np.uint8)
img1 = cv2.resize(img1, dsize=(int(imgx), int(imgy)), interpolation=cv2.INTER_LINEAR)
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2BGRA)
def sc(a0, b0):
    c0 = []
    for i0 in range(a0.shape[0]):
        for j0 in range(a0.shape[1]):
            c0.append((abs(a0[i0, j0][0] - b0[i0, j0][0]) + abs(a0[i0, j0][1] - b0[i0, j0][1]) + abs(a0[i0, j0][2] - b0[i0, j0][2]))/3)
    return np.mean(c0)
'''
o = []
for i in range(int(l.get('순위', 128)) * int(l.get('자식', 8))):
    o.append({})
    o[i]["posX"] = random.randrange(1,int(imgx) + 1)
    o[i]["posY"] = random.randrange(1,int(imgy) + 1)
    o[i]["sizeX"] = random.randrange(1,int(imgx) + 1)
    o[i]["sizeY"] = random.randrange(1,int(imgy) + 1)
    o[i]["color"] = (random.randrange(1, 256), random.randrange(1, 256), random.randrange(1, 256), 1)
    o[i]["rot"] = random.randrange(1, 360)
    o[i]["tr"] = random.randrange(100 - int(l.get("투명", 80)), 101)/100
    t_img = np.full((int(imgx), int(imgy), 4), (0, 0, 0, 0), dtype=np.uint8)
    cv2.rectangle(t_img, (o[i]["posX"] - math.ceil(o[i]["sizeX"]/2), o[i]["posY"] + math.ceil(o[i]["sizeY"]/2)), (o[i]["posX"] + math.ceil(o[i]["sizeX"]/2), o[i]["posY"] - math.ceil(o[i]["sizeY"]/2)), o[i]["color"], -1)
    m00 = cv2.getRotationMatrix2D((o[i]["posX"], o[i]["posY"]), o[i]["rot"], 1)
    re0 = cv2.warpAffine(t_img, m00, (int(imgx), int(imgy)))
    o[i]["sc"] = sc(img0, cv2.addWeighted(img1, 1, re0, o[i]["tr"], 0))
'''
for i in range(int(l.get('반복', 4))):
    print(0)
cv2.imshow('a', img0)
cv2.waitKey()
cv2.destroyAllWindows()
test0 = np.full((50, 50, 3), (32, 65, 152), dtype=np.uint8)
test1 = np.full((50, 50, 3), (43, 53, 98), dtype=np.uint8)
print(sc(test0, test1))
