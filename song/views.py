from django.db.models import Q
from django.http import HttpResponse
from playlist.models import PlayInfo
from song.models import SongInfo
from sing.models import SingInfo
from tools import re_response, re_request

# 音乐播放
def play_music(request):
    reqall = re_request(request)  # json.loads(request.body.decode('utf-8'))
    tyep = reqall.get('type')
    _id = reqall.get('id')
    data = []
    title = ''
    if tyep == 'playlist':  # 说明是查询歌单的歌曲
        obj = PlayInfo.objects.get(play_id=_id)
        query_songs = obj.songs.split(',')
        for _ in SongInfo.objects.filter(song_id__in=query_songs). \
                values_list('song_id', 'title', 'img', 'author_one__name'):
            # MP3_URL = f'http://music.163.com/song/media/outer/url?id={_[0]}.mp3'
            mp3_url = 'http://music.163.com/song/media/outer/url?id=' + str(_[0]) + '.mp3'
            data.append({
                'title': _[1],
                'pic': _[2],
                'url': mp3_url,
                'author': _[3]
            })
        title = "歌单:" + obj.title + '的歌曲'
    if tyep == 'sing':  # 说明是查询歌手的歌曲
        obj = SingInfo.objects.get(sing_id=_id)
        for _ in SongInfo.objects. \
                filter(Q(author_one=_id) | Q(author_two=_id) | Q(author_three=_id)). \
                values_list('song_id', 'title', 'img', 'author_one__name'):
            mp3_url = 'http://music.163.com/song/media/outer/url?id=' + str(_[0]) + '.mp3'
            data.append({
                'title': _[1],
                'pic': _[2],
                'url': mp3_url,
                'author': _[3]
            })
        title = "歌手:" + obj.name + '歌曲'
    if tyep == 'song':  # 说明是具体某歌曲
        obj = SongInfo.objects.filter(song_id=_id). \
            values_list('song_id', 'title', 'img', 'author_one__name')[0]
        # MP3_URL = f'http://music.163.com/song/media/outer/url?id={obj[0]}.mp3'
        mp3_url = 'http://music.163.com/song/media/outer/url?id=' + str(obj[0]) + '.mp3'
        data.append({
            'title': obj[1],
            'pic': obj[2],
            'url': mp3_url,
            'author': obj[3]
        })
        title = '歌曲:' + obj[1]
    return re_response({'data': data, 'title': title})


# 热门音乐 通过歌单的前多少播放量获取音乐
def song_hotrec(request):
    data = []
    songids=[]
    for _ in PlayInfo.objects.all().values_list("songs").order_by('-amount')[:20]:
        for song_id in _[0].split(','):
            songids.append(song_id)
    for _ in SongInfo.objects.filter(song_id__in=songids).values_list("song_id", "title", 'img', 'author_one__name')[:27]:
        data.append({
            'id': _[0],
            'name': _[1],
            'picUrl': _[2],
            'singer': _[3]
        })
    return re_response(data)


def song_search(request):
    reqall = re_request(request)
    keyword = reqall.get('keyword')
    quryinfo = reqall.get('quryinfo')
    page = quryinfo['page']
    pagesize = quryinfo['pagesize']
    data = []
    total = 0
    singers = SingInfo.objects.filter(name__icontains=keyword).values_list('sing_id', flat=True)
    total += SongInfo.objects.filter(
        Q(title__icontains=keyword) | Q(author_id__in=list(singers))).count()

    for _ in SongInfo.objects.filter(Q(title__icontains=keyword) | Q(author_id__in=list(singers)))[
             (page - 1) * pagesize:page * pagesize]:
        data.append({
            'id': _.song_id,
            'title': _.title,
            'album': _.album_title,
            'singname': _.author_one.name,
            'singid': _.author_one.sing_id
        })
    # 获取歌手的歌单

    return re_response({'data': data, 'total': total})


def hello_view(request):
    return HttpResponse("hell world")
