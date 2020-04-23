from django.db import models


# Create your models here.

class SingInfo(models.Model):
    sing_id = models.IntegerField(primary_key=True)
    name = models.CharField("歌手名称", max_length=255, null=True, blank=True)
    img = models.TextField("图片img", null=True, blank=True)
    musicsize = models.IntegerField('音乐数量', default=0)
    albumsize = models.IntegerField('专辑数量', default=0)
    colletsize = models.IntegerField('已收录歌曲数量', default=0)


class SingTag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('名称', null=True, max_length=255)
    sing_id=models.ForeignKey(SingInfo,to_field='sing_id')
