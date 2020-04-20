from sing.models import SingInfo
from song.models import SongInfo
from django.db.models import Q
from tools import re_request,re_response

def sing_hotrec(request):
    data = []
    for _ in SingInfo.objects.filter(img__isnull=False).values_list('sing_id', 'name', 'img')[:20]:
        data.append({
            'id': _[0],
            'singer': _[1],
            'picUrl': _[2]
        })
    return re_response(data)


def sing_info(request):
    """
    :param request:
    :return:
    """
    reqall = re_request(request)#json.loads(request.body)
    _id = reqall.get('id')
    obj = SingInfo.objects.get(sing_id=_id)
    artist = {
        'name': obj.name,
        'desc': '',
        'musicSize': obj.musicsize,
        "albumSize": obj.albumsize,
        'colletSize': obj.colletsize,
        'picUrl': obj.img,
        'id': _id
    }

    songlist = []
    for _ in SongInfo.objects.filter(Q(author_one=_id)|Q(author_two=_id)|Q(author_three=_id)).\
            values_list('song_id', 'title', 'album_title'):
        songlist.append({
            'id': _[0],
            'title': _[1],
            'album': _[2]
        })
    data = {
        'artist': artist,
        'songlist': songlist
    }
    return re_response(data)