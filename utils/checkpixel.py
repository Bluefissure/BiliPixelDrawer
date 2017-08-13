import random
import sys
import os
import urllib
import base64
sys.path.append('/root/IMS/')
os.environ['DJANGO_SETTINGS_MODULE'] ='IMS.settings'
from IMS import settings
import django
from django.db import connection, connections
django.setup()
from pixelapp.models import *
import time
import json
import codecs
import requests
def getRawBitmap():
    url = 'http://api.live.bilibili.com/activity/v1/SummerDraw/bitmap'
    print("Getting bitmap...")
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

def addpixel(projname):
    proj=Project.objects.filter(name=projname)[0]
    for p in proj.pixel.all():
        p.delete()
    with codecs.open('input.txt','r', 'utf8') as of:
      for s in of.readlines():
        ss = s.split()
        pix=Pixel()
        pix.x=ss[0]
        pix.y=ss[1]
        pix.color=ss[2]
        pix.project=proj
        pix.finuser=User.objects.filter(id="Anonymous")[0]
        pix.save()
        print(pix)

def checkpixel(projname):
    proj=Project.objects.filter(name=projname)[0]
    w=1280
    h=720
    bmp=getRawBitmap()
    change_cnt=0
    finbyother_cnt=0
    ano=User.objects.filter(id="Anonymous")[0]
    fin=User.objects.filter(id="FinishedbyOther")[0]
    for p in proj.pixel.all():
        if getidx(bmp[p.y*w+p.x])!=p.color:
            if p.finuser!=ano:
                p.finuser=ano
                p.save()
                change_cnt+=1
        elif p.finuser==ano:
            p.finuser=fin
            finbyother_cnt+=1
            p.save()
    print("Changed pixels:"+str(change_cnt))
    print("Finished-by-other pixels:"+str(finbyother_cnt))
checkpixel("Ingress")