import os
import sys
import django

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
os.chdir(dir_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_rec.settings")
django.setup()

from music_rec.settings import CHROME_PATH, SPLIT
from playlist.models import PlayInfo
from song.models import SongInfo
from sing.models import SingInfo
import requests
import json
import time, random

local_path = os.path.dirname(os.path.abspath(__file__))


class SongSpider:

    def __init__(self):
        self.f = open(local_path + '/data/sing.txt', 'a')
        self.f_in = open(local_path + '/data/song_ready.txt', 'a')  # 判断该歌曲有没有写入
        self.all_song = []
        with open(local_path + '/data/song_ready.txt', 'r') as fs:
            for line in fs.readlines():
                line = line.strip('\n')
                if line == '':
                    continue
                self.all_song.append(line)

    def get_song_list(self):
        playlist_obj = PlayInfo.objects.all().values_list('play_id', 'songs')
        # print(playlist_obj)
        for obj in playlist_obj:
            # print(obj)
            play_id = obj[0]
            songs = obj[1]
            songs_list = songs.split(',')
            querys = []
            for _i in songs_list:
                if _i in self.all_song and SongInfo.objects.filter(song_id=_i).exists():
                    continue
                querys.append(_i)
                self.f_in.write('\n' + _i)
            if len(querys) == 0:
                continue

            if len(querys) > 40:
                querys = querys[:40]

            query_songs = ','.join(querys)

            local_url = f'http://localhost:3000/song/detail?ids={query_songs}'

            infos = json.loads(requests.get(local_url).content)
            self.parse_song_info(infos, play_id)
            time.sleep(random.choice(range(2, 6)))

    def parse_song_info(self, infos, play_id=None):
        print(infos)
        songs = infos.get('songs', False)
        if songs:
            for _ in songs:
                song_id = _['id']  # 歌单id
                if SongInfo.objects.filter(song_id=song_id).exists():
                    continue
                title = _['name']  # 歌曲名称
                album_title = _['al'].get('name')  # 专辑名称
                album_id = _['al'].get('id')  # 专辑id
                album_img = _['al'].get('picUrl')  # 专辑图片
                img = album_img  # 歌曲的图片和专辑图片一样
                author = []
                ars = _.get('ar', None)  # 作者
                if ars is not None and len(ars) > 0:
                    for ar in ars:
                        author.append(str(ar['id']))
                        self.f.write('\n' + str(ar['id']) + SPLIT + ar['name'])
                data = {
                    'title': title,
                    'song_id': str(song_id),
                    'album_title': album_title,
                    'album_id': str(album_id),
                    'album_img': album_img,
                    'img': img,
                    'author_id': ','.join(author)
                }
                if play_id is not None:
                    data['play_id'] = play_id
                SongInfo.objects.create(**data)
                print('歌曲插入成功--', end='')
                print(data)

    def get_hot_song(self, sing_id):
        """
        获取用户的热门歌曲

        :return:
        """
        local_url = f'http://localhost:3000/artist/top/song?id={sing_id}'
        infos = json.loads(requests.get(local_url).content)['songs']
        for _ in infos:
            song_id = _['id']  # 歌单id
            if SongInfo.objects.filter(song_id=song_id).exists():
                continue
            title = _['name']  # 歌曲名称
            album_title = _['al'].get('name')  # 专辑名称
            album_id = _['al'].get('id')  # 专辑id
            album_img = _['al'].get('picUrl')  # 专辑图片
            img = album_img  # 歌曲的图片和专辑图片一样
            author = [] # id
            author_name=[] #name
            ars = _.get('ar', None)  # 作者
            if ars is not None and len(ars) > 0:
                for ar in ars:
                    author.append(str(ar['id']))
                    author_name.append(ar['name'])
                    # self.f.write('\n' + str(ar['id']) + SPLIT + ar['name'])
            data = {
                'title': title,
                'song_id': str(song_id),
                'album_title': album_title,
                'album_id': str(album_id),
                'album_img': album_img,
                'img': img,
                'author_id': ','.join(author)
            }
            for i in range(len(author)):
                _au=author[i]
                if SingInfo.objects.filter(sing_id=_au).exists():
                    ...
                else:
                    SingInfo.objects.create(sing_id=_au,name=author_name[i])
                if i==0:
                    data['author_one']=SingInfo.objects.get(sing_id=_au)
                if i==1:
                    data['author_two'] = _au
                if i==2:
                    data['author_three'] = _au
            try:
                SongInfo.objects.create(**data)
                print('歌曲插入成功--', end='')
                print(data)
            except:
                print('发生错误 跳过')
                f=open(local_path+'/data/hot_song.txt','a')
                f.write('\n'+str(song_id)+str(title))
                f.close()

    def get_hot_sing(self):
        for i in range(0, 1):
            local_url = f'http://localhost:3000/top/artists?offset={i}&limit=50'
            infos = json.loads(requests.get(local_url).content)['artists']
            for info in infos:
                name = info['name']
                sing_id = info['id']
                img = info['img1v1Url']
                musicsize = info['musicSize']
                albumsize = info['albumSize']
                if not SingInfo.objects.filter(sing_id=sing_id).exists():
                    SingInfo.objects.create(sing_id=sing_id, img=img, name=name
                                            , musicsize=musicsize, albumsize=albumsize)
                else:
                    _obj = SingInfo.objects.get(sing_id=sing_id)
                    _obj.img = img
                    _obj.musicsize = musicsize
                    _obj.albumsize = albumsize
                    _obj.save()
                self.get_hot_song(sing_id)
                time.sleep(random.choice(range(2, 5)))


if __name__ == '__main__':
    songspider = SongSpider()
    #songspider.get_song_list()
    songspider.get_hot_sing()
