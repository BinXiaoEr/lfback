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
from song.models import SongInfo
from sing.models import SingInfo, SingTag
from django.db.models import Q

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
            if _.author_one == None or _.author_one == '':
                print(authors)
                continue
            all_author = authors.split(',')
            _.author_one = all_author[0]
            if len(all_author) > 1:
                tag2 = all_author[1]
                _.author_two = tag2
            if len(all_author) > 2:
                tag3 = all_author[2]
                _.author_three = tag3
            _.save()

    def get_collection_music(self):
        for _ in SingInfo.objects.all():
            sing_id = _.sing_id
            _.colletsize = SongInfo.objects.filter(
                Q(author_one=sing_id) | Q(author_two=sing_id) | Q(author_three=sing_id)).count()
            print(sing_id)
            _.save()

    def get_sing_tag(self):
        """
        通过歌单获取 歌手的tag
        :return:
        """
        author_taglist = []
        bulk_insert = []
        i = 0
        for _ in PlayInfo.objects.all():
            all_songs = _.songs.split(',')
            tags = _.tag.split(SPLIT)
            for tag in tags:
                for author_id in SongInfo.objects.filter(song_id__in=all_songs).values_list(
                        'author_one'):
                    author = SingInfo.objects.get(sing_id=author_id[0])
                    cmb_author = str(author_id) + tag
                    if cmb_author not in author_taglist:
                        bulk_insert.append(SingTag(name=tag, sing_id=author))
                        print(author.name,tag)
                        author_taglist.append(cmb_author)
                        i += 1
            if i >= 1000:
                SingTag.objects.bulk_create(bulk_insert)
                i = 0
                bulk_insert.clear()
        if bulk_insert:
            SingTag.objects.bulk_create(bulk_insert)


if __name__ == '__main__':
    tools = Tools()
    # tools.get_collection_music()
    tools.get_sing_tag()
