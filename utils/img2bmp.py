from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys
import codecs,os

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
(121, 85, 72)
]
def getidx(ch):
    if ord(ch)>=ord('A') and ord(ch)<=ord('V'):
        idx=ord(ch)-ord('A')+10
    else:
        idx=ord(ch)-ord('0')
    return idx
def getcolor(color):
    min_diff = 255*3
    min_i = 0
    result = (0,0,0)
    for i in range(32):
        c=colorlist[i]
        sum_diff = abs(color[0]-c[0])+abs(color[1]-c[1])+abs(color[2]-c[2])
        if sum_diff<min_diff:
            min_diff=sum_diff
            result=c
            min_i=i
    return (result,i)
def img2pix(filename):
    im = Image.open(filename)
    w, h = im.size
    print('Image size: %sx%s' % (w, h))
    seq=im.getdata()
    image = Image.new('RGB', (w,h), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    with codecs.open(filename+'.dat', 'w', 'utf8') as of:
        for i in range(w):
            for j in range(h):
                try:
                    if seq[j*w+i]!=(255, 255, 255) and seq[j*w+i]!=(0,0,0): #in range
                        pir = getcolor(seq[j*w+i])
                        of.write("%d %d %d\n"%(i,j,pir[1]))
                        draw.point((i,j), fill=pir[0])
                except:
                    print("%d %d"%(i,j))
    image.save('pix_'+filename+'.bmp', 'bmp')

def data2pix(datafile):
    w=1280
    h=720	
    image = Image.new('RGB', (w,h), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    with codecs.open(datafile,'r', 'utf8') as of:
      for s in of.readlines():
        ss = s.split()
        color=colorlist[int(ss[2])]
        print(color)
        draw.point((int(ss[0]),int(ss[1])), fill=color)
    image.save('data.bmp', 'bmp')


img2pix("a.jpg")
data2pix("a.jpg.dat")