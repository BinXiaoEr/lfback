from playlist.models import PlayInfo, PlayListTag
from tools import re_request, re_response
from django.db.models import Q

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


def playlist_tags(request):
    reall = re_request(request)
    queryinfo = reall.get('queryinfo')
    page = queryinfo['pagenum']
    pagesize = queryinfo['pagesize']
    total=PlayListTag.objects.all().count()
    data = []

    for _ in PlayListTag.objects.all().order_by('-nums')[(page-1)*pagesize:page*pagesize]:
        data.append({
            'id': _.id,
            'name': _.name
        })
    return re_response({'data':data,'total':total})


def playlist_ontag(request):
    reall = re_request(request)
    queryinfo=reall.get('queryinfo')
    page=queryinfo['pagenum']
    pagesize=queryinfo['pagesize']
    print(reall)
    _id = reall.get('id')
    tagname=PlayListTag.objects.get(id=_id).name
    data = []
    total=PlayInfo.objects.filter(Q(first_tag=_id)|Q(second_tag=_id)|Q(thrid_tag=_id)).count()
    for _ in PlayInfo.objects.filter(Q(first_tag=_id)|Q(second_tag=_id)|Q(thrid_tag=_id)).\
                     values_list('title', 'play_id', 'img','author')[(page-1)*pagesize:page*pagesize]:
        data.append({
            'title': _[0],
            'id': _[1],
            'artist': _[3],
            'picUrl': _[2]
        })
    return re_response({'data':data,'total':total,'tagname':tagname})
