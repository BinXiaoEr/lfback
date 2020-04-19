from django.db import models

from sing.models import SingInfo
# Create your models here.


class SongInfo(models.Model):
    song_id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField("标题", max_length=255, null=True, blank=True)
    img = models.CharField("图片地址", max_length=255, null=True, blank=True)
    author_id = models.CharField("作者", max_length=255, null=True, blank=True)
    album_title = models.CharField("专辑", max_length=255, null=True, blank=True)
    album_id = models.CharField("专辑id", max_length=255, null=True, blank=True)
    album_img = models.TextField("专辑img", null=True, blank=True)
    play_id = models.CharField('歌单id', null=True, max_length=255)
    author_one=models.ForeignKey(SingInfo,to_field='sing_id')
    author_two=models.CharField(max_length=10,null=True, blank=True)
    author_three=models.CharField(max_length=10,null=True, blank=True)


class SongTag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('名称', null=True, max_length=255)
