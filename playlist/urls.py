
from django.conf.urls import url, include
from django.contrib import admin
from playlist.views import playlist_hotrec,playlist_tags,playlist_ontag
urlpatterns = [
    url('^hotrec/', playlist_hotrec),# 热门歌单推荐
    url('^alltags/',playlist_tags), # 获取所有歌单分类
    url('^tag_playlist',playlist_ontag)
]
