from tools import re_response, re_request
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User, UserHistory
from song.models import SongInfo

MAX_HISTORY = 2

# 设置用户还可通过电话号码进行登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(phonenumber=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def mylogin(request):
    reqall = re_request(request)
    username = reqall['username']
    password = reqall['password']
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        token = list(request.session.values())[-1]
        return re_response(
            {'state': 1, 'msg': '', 'data': {'id': user.id, 'name': user.realname}, "token": token})
    else:
        return re_response({'state': 2, 'msg': ''})


def mylogout(request):
    reqall = re_request(request)
    username = reqall['username']
    userid = reqall['useid']
    user = User.objects.get(id=userid)
    if user:
        logout(request)
        return re_response({'state': 1})


def myregister(request):
    reqall = re_request(request)
    username = reqall['username']
    password = reqall['password']
    email = reqall['email']
    phone = reqall['phone']
    realname = reqall['realname']
    if User.objects.filter(Q(username=username) | Q(phonenumber=phone)).exists():
        # 用户名已经存在
        return re_response({'state': 2})
    else:
        User.objects.create(username=username, password=make_password(password), phonenumber=phone,
                            email=email, realname=realname)
        return re_response({'state': 1})


def add_history(request):
    reqall = re_request(request)
    uid = int(reqall['userid'])  # userid
    tyep = reqall['type']  # 播放的是歌单还是什么
    tyep_id = reqall['id']  # 播放类型id
    songid = reqall['songid']
    user_obj = User.objects.get(id=uid)
    # 要记录
    model_data = {
        'song_id': songid,
        'userid': user_obj
    }
    if tyep == 'playlist':  # 说明是查询歌单的歌曲
        model_data['playlist_id'] = tyep_id
        author = SongInfo.objects.get(song_id=songid).author_one
        model_data['sing_id'] = author.sing_id  # 添加用户信息
    if tyep == 'sing':  # 说明是查询歌手的歌曲
        model_data['sing_id'] = tyep_id
        playlist_id = SongInfo.objects.get(song_id=songid).play_id
        if playlist_id is not None:
            model_data['playlist_id'] = playlist_id
    if tyep == 'song':  # 说明是具体某歌曲
        author = SongInfo.objects.get(song_id=songid).author_one
        model_data['sing_id'] = author.sing_id  # 添加用户信息
        playlist_id = SongInfo.objects.get(song_id=songid).play_id
        if playlist_id is not None:
            model_data['playlist_id'] = playlist_id
    # 对用户记录
    if UserHistory.objects.filter(**model_data).exists():
        # 如果播放的是同一个音乐 则要更新时间
        UserHistory.objects.update(**model_data)
    elif UserHistory.objects.filter(userid=user_obj).count() < MAX_HISTORY:
        # 如果当前用户历史播放记录比设定值小 则直接插入新的数据
        UserHistory.objects.create(**model_data)
    else:
        # 要替换最早播放的音乐信息\
        user_history = UserHistory.objects.filter(userid=user_obj).order_by('add_time').first()
        user_history.__dict__.update(**model_data)
        user_history.save()
    return re_response({'state': 1})
