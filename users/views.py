from tools import re_response, re_request
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User, UserHistory
from song.models import SongInfo
from sing.models import SingInfo, SingSim
from playlist.models import PlayInfo, PlayListSim
import random
# 可以记录用户最大的历史数目
MAX_HISTORY = 20


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
    """
    用户登录
    :param request:
    :return:
    """
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
    """
    用户注销
    :param request:
    :return:
    """
    reqall = re_request(request)
    username = reqall['username']
    userid = reqall['useid']
    user = User.objects.get(id=userid)
    if user:
        logout(request)
        return re_response({'state': 1})


def myregister(request):
    """
    用户注册
    :param request:
    :return:
    """
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
    """
    添加历史记录
    :param request:
    :return:
    """
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
        _=UserHistory.objects.get(**model_data)
        for k,v in model_data.items():
            setattr(_,k,v)
        _.save()
    elif UserHistory.objects.filter(userid=user_obj).count() < MAX_HISTORY:
        # 如果当前用户历史播放记录比设定值小 则直接插入新的数据
        UserHistory.objects.create(**model_data)
    else:
        # 要替换最早播放的音乐信息\
        user_history = UserHistory.objects.filter(userid=user_obj).order_by('add_time').first()
        user_history.__dict__.update(**model_data)
        user_history.save()
    return re_response({'state': 1})


def get_recommend(request):
    """
    获取用户推荐
    :param request:
    :return:
    """
    reall = re_request(request)
    userid = int(reall['userid'])  # 用户id
    histrorys = UserHistory.objects.filter(userid__id=userid). \
        order_by('add_time').values_list('song_id', 'sing_id', 'playlist_id')
    song_ids, sing_ids, plalist_ids = [], [], []

    for _ in histrorys:
        if _[0] not in song_ids:
            song_ids.append(_[0])
        if _[1] not in sing_ids:
            sing_ids.append(_[1])
        if _[2] not in plalist_ids:
            plalist_ids.append(_[2])

    singlist, sim_sings = _sing_rec(sing_ids)
    playlist, sim_playlist = _playlist_rec(plalist_ids)
    songlist = _song_rec(sim_playlist,sim_sings)

    # 用户历史记录获取
    userhistory=[]
    for _ in SongInfo.objects.filter(song_id__in=song_ids).values_list("song_id", "title", 'img', 'author_one__name'):
        userhistory.append({
            'id': _[0],
            'name': _[1],
            'picUrl': _[2],
            'singer': _[3]
        })
    return re_response({'singlist': singlist, 'playlist': playlist,'songlist':songlist,'userhistory':userhistory})


def _sing_rec(sing_ids):
    """
    通过歌手id获取推荐
    :param sing_ids:
    :return:
    """
    data = []
    sim_sings = SingSim.objects.filter(sing_id__in=sing_ids). \
        values_list("sim_sing__sing_id", flat=True).distinct().order_by('-sim')

    for _ in SingInfo.objects.filter(sing_id__in=sim_sings). \
                     values_list('sing_id', 'name', 'img').order_by('-colletsize')[:20]:
        data.append({
            'id': _[0],
            'singer': _[1],
            'picUrl': _[2]
        })
    return data, list(sim_sings)


def _playlist_rec(playlist_ids):
    """
    :param playlist_ids:
    :return:
    """
    sim_playlist = PlayListSim.objects.filter(playlist__play_id__in=playlist_ids). \
        values_list("sim_playlist__play_id", flat=True).distinct().order_by('-sim')
    datas = []
    for _ in PlayInfo.objects.filter(play_id__in=sim_playlist). \
                     values_list('play_id', 'title', 'img', 'amount').order_by('-amount')[:20]:
        datas.append({
            'id': _[0],
            'name': _[1],
            'picUrl': _[2],
            'playCount': _[3]
        })
    return datas, list(sim_playlist)


def _song_rec(sim_playlist, sim_sing):
    data = []
    for _ in SongInfo.objects.filter(
            Q(play_id__in=sim_playlist) | Q(author_one__sing_id__in=sim_sing)). \
                     values_list("song_id", "title", 'img', 'author_one__name')[:100]:
        data.append({
            'id': _[0],
            'name': _[1],
            'picUrl': _[2],
            'singer': _[3]
        })
    random.shuffle(data)
    return data[:54]
