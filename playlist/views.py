from playlist.models import PlayInfo
from tools import re_request,re_response

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
    return re_response(datas)
