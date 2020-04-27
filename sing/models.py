from django.db import models


# Create your models here.

class SingInfo(models.Model):
    sing_id = models.IntegerField(primary_key=True)
    name = models.CharField("歌手名称", max_length=255, null=True, blank=True)
    img = models.TextField("图片img", null=True, blank=True)
    musicsize = models.IntegerField('音乐数量', default=0)
    albumsize = models.IntegerField('专辑数量', default=0)
    colletsize = models.IntegerField('已收录歌曲数量', default=0)

    def __str__(self):
        return self.sing_id

    class Meta:
        db_table = "SingInfo"
        verbose_name_plural = "歌手信息"


class SingTag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('名称', null=True, max_length=255)
    # sing_id = models.ForeignKey(SingInfo, to_field='sing_id',on_delete=models.DO_NOTHING)
    sing_id = models.ForeignKey(SingInfo, to_field='sing_id', on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.id

    class Meta:
        db_table = "SingTag"
        verbose_name_plural = "歌手类型"


class SingSim(models.Model):
    sing = models.ForeignKey(SingInfo, to_field='sing_id', verbose_name="歌手iD",on_delete=models.DO_NOTHING)
    sim_sing = models.ForeignKey(SingInfo, related_name='sim_sing', to_field='sing_id',
                                 verbose_name="相似歌手ID",on_delete=models.DO_NOTHING)
    sim = models.FloatField(blank=True, verbose_name="相似度")

    def __str__(self):
        return self.sing_id

    class Meta:
        db_table = "SingSim"
        verbose_name_plural = "歌手相似"
