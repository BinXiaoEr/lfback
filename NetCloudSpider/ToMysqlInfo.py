import os
import sys
import django

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
os.chdir(dir_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_rec.settings")
django.setup()

from music_rec.settings import CHROME_PATH, SPLIT

from playlist.models import PlayInfo, PlayListTag
from song.models import SongInfo, SongTag
from sing.models import SingInfo
import json

local_path = os.path.dirname(os.path.abspath(__file__))
f = open(local_path + '/data/sing.txt', 'r')


class Tools:

    def get_tas(self):
        """
        获取 歌单标签
        :return: 
        """
        all_tags = {}
        for _ in PlayInfo.objects.all().values_list('tag', flat=True):
            if _ == '' or _ is None:
                continue
            for _tag in _.split(SPLIT):
                all_tags.setdefault(_tag, 0)
                all_tags[_tag] += 1
        for k, v in all_tags.items():
            PlayListTag.objects.create(name=k, nums=v)
        # print(all_tags)

    def get_playlist_tag(self):
        """
        获取歌单的tag外键
        :return:
        """
        for _ in PlayInfo.objects.all():
            tags = _.tag
            if tags == '':  # 如果都为空
                continue
            tag_list = tags.split(SPLIT)
            tag1 = tag_list[0]
            _.first_tag = PlayListTag.objects.get(name=tag1)
            if len(tag_list) > 1:
                tag2 = tag_list[1]
                _.second_tag = PlayListTag.objects.get(name=tag2).id
            if len(tag_list) > 2:
                tag3 = tag_list[2]
                _.thrid_tag = PlayListTag.objects.get(name=tag3).id
            _.save()

    def get_song_sing(self):
        for _ in SongInfo.objects.all():

            authors = _.author_id
            if _.author_one ==None or _.author_one =='':
                print(authors)
                continue
            all_author = authors.split(',')
            _.author_one =all_author[0]
            if len(all_author) > 1:
                tag2 = all_author[1]
                _.author_two=tag2
            if len(all_author) > 2:
                tag3 = all_author[2]
                _.author_three=tag3
            _.save()
    def get_collection_music(self):
        for _ in SingInfo.objects.all():
            sing_id=_.sing_id
            _one=SongInfo.objects.filter(author_one=sing_id).count()
            _two=SongInfo.objects.filter(author_two=sing_id).count()
            _three = SongInfo.objects.filter(author_three=sing_id).count()
            _.colletsize=_one+_three+_two
            print(sing_id,_.name,_one+_three+_two)
            _.save()

if __name__ == '__main__':
    tools = Tools()
    tools.get_collection_music()
