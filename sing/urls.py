
from django.conf.urls import url, include
from django.contrib import admin
from sing.views import sing_hotrec,sing_info,hot_sing
urlpatterns = [
    url('^hotrec/',sing_hotrec),  # 热门歌单推荐
    url('^info/',sing_info),
    url('^hot_sing/',hot_sing)
]
