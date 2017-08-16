# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, Http404, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from django.core.files.base import ContentFile
from django.utils import timezone
from collections import OrderedDict
import datetime
import pytz
import random,string
import re
import json
from pixelapp.models import *
# Create your views here.

def ren2res(template, req, dict={}):
    if req:
        return render_to_response(template, dict, context_instance=RequestContext(req))
    else:
        return render_to_response(template, dict)

def pixelhome(req):
    dict={}
    if req.method == 'POST':
        nickname = req.POST.get('nickname')
        projname = req.POST.get('project')
        if not nickname:
            dict.update({'err':"Empty username."})
        elif not projname:
            dict.update({'err':"Empty project."})
        else:
            print(nickname)
            print(projname)
            user = User.objects.filter(id=nickname)
            if(len(user) == 0):
                user = User()
                user.id = nickname
                user.save()
            else:
                user = user[0]
            project = Project.objects.filter(name=projname)
            if(len(project) == 0):
                project = Project()
                project.name = projname
                project.save()
            else:
                project = project[0]
            tokens = Token.objects.filter(user=user,project=project)
            if(len(tokens)>0):
                dict.update({'token':tokens[0].token})
            else:
                new_token = Token()
                new_token.token = ''.join(random.sample(string.ascii_letters + string.digits, 16))
                new_token.user = user
                new_token.project = project
                new_token.save()
                dict.update({'token':new_token.token})
    if req.method == 'GET':
        token = req.GET.get('token')
        if token:
            tt = Token.objects.filter(token=token)
            if(len(tt)!=1):
                jsondata={
                    "msg":"Token not auth."
                }
                return JsonResponse(jsondata)
                pass
            else:
                tt = tt[0]
                finx = req.GET.get('finx')
                if finx:
                    user = tt.user
                    proj = tt.project
                    x = req.GET.get('finx')
                    y = req.GET.get('finy')
                    pix = proj.pixel.filter(x=x,y=y)[0]
                    pix.finuser = user
                    pix.save()
                    jsondata={"msg":"success","projname":proj.name}
                    return JsonResponse(jsondata)
                else:
                    pixel = tt.project.pixel.filter(finuser="Anonymous").order_by("updtime")
                    tot = tt.project.pixel.all().count()
                    unsolved = tt.project.pixel.filter(finuser="Anonymous").count()
                    proj = tt.project
                    if unsolved>0:
                        pixel = pixel[random.randint(0,unsolved-1)]
                        jsondata={
                            'total':tot,
                            'unsolve':unsolved,
                            'msg':"success",
                            'x':pixel.x,
                            'y':pixel.y,
                            'color':pixel.color if pixel.color<10 else chr(pixel.color-10+ord('A')),
                            "projname":proj.name,
                        }
                    else:
                        jsondata={
                            'total':tot,
                            'unsolve':unsolved,
                            'msg':"finish",
                            "projname":proj.name,
                        }
                    return JsonResponse(jsondata)
    projs = Project.objects.all()
    projlist = []
    for p in projs:
        projlist.append(p.name)
    dict.update({'project':projlist})
    return ren2res('pixelhome.html',req,dict)
