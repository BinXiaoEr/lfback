from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    sings = models.CharField('播放的歌手', max_length=100, blank=True, null=True)
    playlist = models.CharField('播放的歌单', max_length=100, blank=True, null=True)
    phonenumber = models.CharField('电话号码', max_length=100, blank=True, null=True)
    realname = models.CharField('真实姓名', max_length=100, blank=True, null=True)

    class Meta(AbstractUser.Meta):
        app_label = "users"
        db_table = "UsersInfo"
        verbose_name_plural = "用户信息"


class UserHistory(models.Model):
    userid = models.ForeignKey(User, to_field='id',on_delete=models.DO_NOTHING)
    song_id = models.TextField("歌曲id", blank=True, null=True)
    sing_id = models.TextField("歌手id", blank=True, null=True)
    playlist_id = models.TextField("歌单id", blank=True, null=True)  # 可能会存在没有
    add_time = models.DateTimeField(auto_now=True)  # 设置日期添加时限
    # class Meta:
    #     db_table = "UserHistory"
    #     verbose_name_plural = "用户记录"