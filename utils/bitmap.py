import requests
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
def getRawBitmap():
    url = 'http://api.live.bilibili.com/activity/v1/SummerDraw/bitmap'
    print("[INFO]:Getting bitmap...")
    r = requests.get(url)
    jDate = r.json()
    return jDate['data']['bitmap']



colorlist=[
(0,0,0),
(255,255,255),
(170, 170, 170),
(85, 85, 85),
(254, 211, 199),
(255, 196, 206),
(250, 172, 142),
(255, 139, 131),
(244, 67, 54),
(233, 30, 99),
(226, 102, 158),
(156, 39, 176),
(103, 58, 183),
(63, 81, 181),
(0, 70, 112),
(5, 113, 151),
(33, 150, 243),
(0, 188, 212),
(59, 229, 219),
(151, 253, 220),
(22, 115, 0),
(55, 169, 60),
(137, 230, 66),
(215, 255, 7),
(255, 246, 209),
(248, 203, 140),
(255, 235, 59),
(255, 193, 7),
(255, 152, 0),
(255, 87, 34),
(184, 63, 39),
(121, 85, 72),
]
def getidx(ch):
    if ord(ch)>=ord('A') and ord(ch)<=ord('V'):
        idx=ord(ch)-ord('A')+10
    else:
        idx=ord(ch)-ord('0')
    return idx
def getcolor(pix):
    return colorlist[pix]

bmp=getRawBitmap()
w=1280
h=720
image = Image.new('RGB', (w,h), (255, 255, 255))
draw = ImageDraw.Draw(image)
print("Drawing")
for i in range(w):
    for j in range(h):
        draw.point((i,j), fill=colorlist[getidx(bmp[j*w+i])])

image.save('bitmap.bmp', 'bmp')
                