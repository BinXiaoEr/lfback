from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    sings=models.CharField('喜欢的歌手', max_length=100, blank=True, null = True)
    playlist=models.CharField('喜欢的歌单', max_length=100, blank=True, null = True)


    class Meta(AbstractUser.Meta):

        app_label = "users"



class UserHistory(models.Model):
    userid = models.IntegerField("用戶id")

# Create your models here.
