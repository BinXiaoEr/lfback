from django.db import models


class PlayListTag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('名称', null=True, max_length=255)
    nums = models.IntegerField("数量", default=1)

    def __unicode__(self):
        return self.id

    class Meta:
        db_table = "PlayListTag"
        verbose_name_plural = "歌单tag标签"


# Create your models here.
class PlayInfo(models.Model):
    play_id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField("标题", max_length=255, null=True, blank=True)
    img = models.CharField("图片地址", max_length=255, null=True, blank=True)
    author = models.CharField("作者", max_length=255, null=True, blank=True)
    tag = models.CharField("标签", max_length=255, null=True, blank=True)
    describe = models.TextField("描述", null=True, blank=True)
    collection = models.CharField("收藏量", max_length=255, null=True, blank=True)
    forward = models.CharField("分享量", max_length=255, null=True, blank=True)
    comment = models.CharField("评论量", max_length=255, null=True, blank=True)
    # amount = models.CharField("播放量", max_length=255, null=True, blank=True)
    amount = models.IntegerField("播放量",default=0)
    songs = models.TextField("歌单歌曲", null=True, blank=True)
    first_tag = models.ForeignKey(PlayListTag, to_field='id', on_delete=models.DO_NOTHING)  # 主要tag
    # first_tag = models.IntegerField(default=59)
    second_tag = models.IntegerField(default=59)  #
    thrid_tag = models.IntegerField(default=59)

    def __unicode__(self):
        return self.play_id

    class Meta:
        db_table = "PlayInfo"
        verbose_name_plural = "歌单信息"


class PlayListSim(models.Model):
    playlist = models.ForeignKey(PlayInfo, to_field='play_id', verbose_name="歌单iD",
                                 on_delete=models.DO_NOTHING)
    sim_playlist = models.ForeignKey(PlayInfo, related_name='sim_playlist', to_field='play_id',
                                     verbose_name="相似歌单ID", on_delete=models.DO_NOTHING)
    sim = models.FloatField(blank=True, verbose_name="相似度")

    def __unicode__(self):
        return self.playlist

    class Meta:
        db_table = "PlayListSim"
        verbose_name_plural = "歌单相似"
