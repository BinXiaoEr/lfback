from playlist.models import PlayInfo, PlayListTag
from tools import re_request, re_response
from song.models import SongInfo
from django.db.models import Q
from music_rec.settings import SPLIT


def playlist_hotrec(request):
    """
    热门歌单 获取播放量前20
    :param request:
    :return:
    """
    datas = []
    for _ in PlayInfo.objects.all().values_list('play_id', 'title', 'img', 'amount').order_by(
            '-amount')[:20]:
        datas.append({
            'id': _[0],
            'name': _[1],
            'picUrl': _[2],
            'playCount': _[3]
        })
    return re_response(datas)


def playlist_tags(request):
    """
    歌单标签获取
    :param request:
    :return:
    """
    reall = re_request(request)
    queryinfo = reall.get('queryinfo')
    page = queryinfo['pagenum']
    pagesize = queryinfo['pagesize']
    total = PlayListTag.objects.all().count()
    data = []

    for _ in PlayListTag.objects.all().order_by('-nums')[(page - 1) * pagesize:page * pagesize]:
        data.append({
            'id': _.id,
            'name': _.name
        })
    return re_response({'data': data, 'total': total})


def playlist_ontag(request):
    """
    标签下的所有歌单
    :param request:
    :return:
    """
    reall = re_request(request)
    queryinfo = reall.get('queryinfo')
    page = queryinfo['pagenum']
    pagesize = queryinfo['pagesize']
    _id = reall.get('id')
    tagname = PlayListTag.objects.get(id=_id).name
    data = []
    total = PlayInfo.objects. \
        filter(Q(first_tag__id=_id) | Q(second_tag=_id) | Q(thrid_tag=_id)).count()
    for _ in PlayInfo.objects.filter(Q(first_tag__id=_id) | Q(second_tag=_id) | Q(thrid_tag=_id)). \
                     values_list('title', 'play_id', 'img', 'author').order_by("-amount")[
             (page - 1) * pagesize:page * pagesize]:
        data.append({
            'title': _[0],
            'id': _[1],
            'artist': _[3],
            'picUrl': _[2]
        })
    return re_response({'data': data, 'total': total, 'tagname': tagname})


def playlist_info(request):
    reall = re_request(request)
    play_id = reall['id']
    songlist = []

    for _ in SongInfo.objects.filter(play_id=play_id). \
            values_list('song_id', 'title', 'album_title', 'author_one__name',
                        'author_one__sing_id'):
        songlist.append({
            'id': _[0],
            'title': _[1],
            'album': _[2],
            'sname': _[3],
            'sid': _[4]
        })
    playlist_obj = PlayInfo.objects.get(play_id=play_id)
    playlist = {
        'name': playlist_obj.title,
        'desc': playlist_obj.describe,
        'picUrl': playlist_obj.img,
        'id': play_id,
        'tags': "|".join(playlist_obj.tag.split(SPLIT)),
        'nums': len(songlist)
    }
    return re_response({'playlist': playlist, 'songlist': songlist})
