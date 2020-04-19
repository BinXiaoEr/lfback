
from django.conf.urls import url, include
from django.contrib import admin
from sing.views import sing_hotrec,sing_info
urlpatterns = [
    url('^hotrec/',sing_hotrec),  # 热门歌单推荐
    url('^info/',sing_info)
]
