from django.conf.urls import url
from song.views import play_music,song_hotrec,hello_view,song_search


urlpatterns = [
     url('^play/', play_music),# 热门歌单推荐
     url('^hotrec/',song_hotrec),
     url('^hello/',hello_view),
     url('^search/',song_search)
]
