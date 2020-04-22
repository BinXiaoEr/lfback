from django.shortcuts import render
from tools import re_response, re_request
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from users.models import User


def mylogin(request):
    reqall = re_request(request)
    username = reqall['username']
    password = reqall['password']
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        token = list(request.session.values())[-1]
        return re_response(
            {'state': 1, 'msg': '', 'data': {'id': user.id, 'name': user.username}, "token": token})
    else:
        return re_response({'state': 2, 'msg': ''})


def mylogout(request):
    reqall = re_request(request)
    username = reqall['username']
    userid = reqall['useid']
    user = User.objects.get(id=userid)
    if user:
        return re_response({'state': 1})


def myregister(request):
    reqall = re_request(request)
    username = reqall['username']
    password = reqall['password']
    if User.objects.filter(username=username).exists():
        # 用户名已经存在
        return re_response({'state': 2})
    else:
        User.objects.create(username=username, password=password)
        return re_response({'state': 1})
