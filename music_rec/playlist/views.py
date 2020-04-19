from django.http import HttpResponse
from playlist.models import PlayInfo

import json


def playlist_hotrec(request):
    """
    热门歌单推荐
    :param request:
    :return:
    """
    datas = []
    for _ in PlayInfo.objects.filter().values_list('play_id', 'title', 'img', 'amount')[:20]:
        datas.append({
            'id': _[0],
            'name': _[1],
            'picUrl': _[2],
            'playCount': _[3]
        })
    return HttpResponse(
        json.dumps({
            'state': 1,
            'message': '成功',
            'data': datas
        }))
