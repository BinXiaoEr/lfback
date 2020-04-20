from django.shortcuts import render
from tools import re_response, re_request
from django.contrib.auth import authenticate
from users.models import User
# Create your views here.
from django.contrib.auth import login, logout

def mylogin(request):
    reqall=re_request(request)
    username=reqall['username']
    password=reqall['password']
    user = authenticate(username=username, password=password)
    if user:
        login(request,user)
        token=list(request.session.values())[-1]
        return re_response({'state':1,'msg':'','data':{'id':user.id,'name':user.username},"token":token})
    else:
        return re_response({'state': 2, 'msg': ''})


def mylogout(request):
    pass


def myregister(request):
    pass
