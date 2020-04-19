
from django.conf.urls import url, include
from django.contrib import admin
from playlist.views import playlist_hotrec
urlpatterns = [
    url('^hotrec/', playlist_hotrec),# 热门歌单推荐
]
