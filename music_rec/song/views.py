from django.db.models import Q
from django.http import HttpResponse
from playlist.models import PlayInfo
from song.models import SongInfo
from sing.models import SingInfo
import json


# 音乐播放
def play_music(request):
    reqall = json.loads(request.body)
    tyep = reqall.get('type')
    _id = reqall.get('id')
    data = []
    title = ''
    if tyep == 'playlist':  # 说明是查询歌单的歌曲
        obj = PlayInfo.objects.get(play_id=_id)
        query_songs = obj.songs.split(',')
        for _ in SongInfo.objects.filter(song_id__in=query_songs). \
                values_list('song_id', 'title', 'img', 'author_one__name'):
            MP3_URL = f'http://music.163.com/song/media/outer/url?id={_[0]}.mp3'
            data.append({
                'title': _[1],
                'pic': _[2],
                'url': MP3_URL,
                'author': _[3]
            })
        title = "歌单:" + obj.title + '的歌曲'
    if tyep == 'sing':  # 说明是查询歌手的歌曲
        obj = SingInfo.objects.get(sing_id=_id)
        for _ in SongInfo.objects. \
                filter(Q(author_one=_id) | Q(author_two=_id) | Q(author_three=_id)). \
                values_list('song_id', 'title', 'img', 'author_one__name'):
            MP3_URL = f'http://music.163.com/song/media/outer/url?id={_[0]}.mp3'
            data.append({
                'title': _[1],
                'pic': _[2],
                'url': MP3_URL,
                'author': _[3]
            })
        title = "歌手:" + obj.name + '歌曲'
    if tyep == 'song':  # 说明是具体某歌曲
        obj = SongInfo.objects.filter(song_id=_id). \
            values_list('song_id', 'title', 'img', 'author_one__name')[0]
        MP3_URL = f'http://music.163.com/song/media/outer/url?id={obj[0]}.mp3'
        data.append({
            'title': obj[1],
            'pic': obj[2],
            'url': MP3_URL,
            'author': obj[3]
        })
        title = '歌曲:' + obj[1]
    return HttpResponse(json.dumps({
        'state': 1,
        'messgae': '成功',
        'data': data,
        'title': title
    }))


# 音乐推荐
def song_hotrec(request):
    data = []

    for _ in SongInfo.objects.all().values_list("song_id","title",'img','author_one__name')[:20]:
        data.append({
            'id':_[0],
            'name': _[1],
            'picUrl':_[2],
            'singer':_[3]
        })

    return HttpResponse(json.dumps(
        {'state': 1,
         'messgae': '成功',
         'data': data
         }
    ))
