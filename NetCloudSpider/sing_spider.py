import os
import sys
import django

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
os.chdir(dir_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_rec.settings")
django.setup()

from music_rec.settings import CHROME_PATH, SPLIT
from song.models import SongInfo
from sing.models import SingInfo
import requests
import json
import time
import random

local_path = os.path.dirname(os.path.abspath(__file__))
f = open(local_path + '/data/sing.txt', 'r')


class SingSpider:
    # def __init__(self):
    #
    #     self.all_authors = []
    #     for line in f.readlines():
    #         line = line.strip('\n')
    #         if line == '' or line in self.all_authors:
    #             continue
    #         self.all_authors.append(line)

    def author_from_txt(self):
        for _ in self.all_authors:
            sing_id = _.split(SPLIT)[0]
            name = _.split(SPLIT)[1]
            if SingInfo.objects.filter(sing_id=sing_id).exists():
                continue
            SingInfo.objects.create(sing_id=sing_id, name=name)

    def sing_info(self):
        for _ in SingInfo.objects.filter(img__isnull=True):
            sing_id = _.sing_id
            local_url = f'http://localhost:3000/artists?id={sing_id}'
            _req = requests.get(local_url)
            if _req.status_code != 200:
                continue
            infos = json.loads(_req.content)
            sing_info = infos.get('artist')
            _.musicsize = sing_info['musicSize']
            _.albumsize = sing_info['albumSize']
            _.img = sing_info['picUrl']
            songs = infos.get('hotSongs')

            for song_info in songs[:30]:
                song_id = song_info['id']  # 歌单id
                if SongInfo.objects.filter(song_id=song_id).exists():
                    continue
                title = song_info['name']  # 歌曲名称
                album_title = song_info['al'].get('name')  # 专辑名称
                album_id = song_info['al'].get('id')  # 专辑id
                album_img = song_info['al'].get('picUrl')  # 专辑图片
                img = album_img  # 歌曲的图片和专辑图片一样
                # author = []
                # ars = song_info.get('ar', None)  # 作者
                data = {
                    'title': title,
                    'song_id': str(song_id),
                    'album_title': album_title,
                    'album_id': str(album_id),
                    'album_img': album_img,
                    'img': img,
                    'author_id': sing_id,
                    'author_one': _
                }
                SongInfo.objects.create(**data)
                print('歌曲插入成功--', end='')
                print(data)
            _.save()

            # time.sleep(random.choice(range(2, 5)))


if __name__ == '__main__':
    singspider = SingSpider()
    singspider.sing_info()
    # singspider.author_from_txt()
