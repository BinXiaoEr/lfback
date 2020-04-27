import sys
import django
import os

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
os.chdir(dir_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_rec.settings")
django.setup()

from playlist.models import PlayInfo, PlayListTag, PlayListSim
from music_rec.settings import SPLIT
import itertools
import numpy as np
import json
import math

dir_data_path = os.path.dirname(os.path.abspath(__file__)) + '/data/'
SPLIT2 = '|=|'


class RecPlayList:
    """
    歌单相似度
    """

    def __init__(self):
        if not os.path.exists(dir_data_path + '/playlist_all.txt'):
            self._data_from_mysql()

        self.all_tags = list(PlayListTag.objects.all().values_list('name', flat=True))  # 获取所有tag标签
        self.raw_datas = []  # 获取文本
        self.tag_one_count = {}  # 获取每个tag 有多少个
        with open(dir_data_path + '/playlist_all.txt', 'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                if line == '':
                    continue
                self.raw_datas.append(line)
        self.playids = []
        self.playlist_matrix_list = self.playlist_tag_rate()  # 歌单 tage 评分
        self.playlist_counts = self.playlist_tag_count()  # tag之间数量统计  得到矩阵C，C[i][j]表示同时分别i和j的用户数
        self.tag_sim_matrix = self.cal_playlist_rec()
        for i in self.tag_sim_matrix:
            print(i)
        # print(self.tag_sim_matrix)
        # for i in self.playlist_counts:
        #     print(i)
        # print(self.raw_datas)

    def _data_from_mysql(self):
        """
        获取数据库表单信息进入文件
        playid tags infoward(分享量)
        :return:
        """
        f = open(dir_data_path + '/playlist_all.txt', 'w')
        for _ in PlayInfo.objects.all().values_list('play_id', 'tag', 'forward'):
            _id = _[0]
            tag = _[1]
            forward = _[2]
            if forward == '' or forward is None:
                forward = "1"
            if tag is "" or tag is None:
                tag = '其他'
            # print(str(_id) + SPLIT2 + tag + SPLIT2 + forward)
            f.write(str(_id) + SPLIT2 + tag + SPLIT2 + forward + '\n')
        f.close()

    def playlist_tag_rate(self):
        """
        获取歌单的tag - rate
        :return:
        """
        playlist_matrix_dict = {}
        for data in self.raw_datas:
            split_data = data.split(SPLIT2)
            playid = split_data[0]  # playlistid
            tags = split_data[1]  # tag
            rate = split_data[2]  # 评分
            playlist_matrix_dict.setdefault(playid, {})
            for tag in tags.split(SPLIT):
                playlist_matrix_dict[playid][tag] = rate
                self.tag_one_count.setdefault(tag, 0)
                self.tag_one_count[tag] += 1  # 获取每个tag有多少个

        playlist_matrix_list = []

        for playid, tag_rates in playlist_matrix_dict.items():
            self.playids.append(playid)
            zero_data = [0] * len(self.all_tags)
            for tag, rate in tag_rates.items():
                index = self.all_tags.index(tag)
                zero_data[index] = int(rate)
            playlist_matrix_list.append(zero_data)

        return playlist_matrix_list

    def playlist_tag_count(self):
        """
        获取 相关物品之间的数量 用于计算相似度
        :return: 
        """
        ...
        tag_to_count = {}
        for data in self.raw_datas:
            split_data = data.split(SPLIT2)
            tags = split_data[1]  # tag
            tag_list = tags.split(SPLIT)
            # 两两排列组合
            tagiter = itertools.combinations(tag_list, 2)
            if tagiter:
                # 如果有排列组合
                for i in tagiter:
                    _i1 = i[0]
                    _i2 = i[1]
                    tag_to_count.setdefault(_i1 + '|*|' + _i2, 0)
                    # 计算数量
                    tag_to_count[_i1 + '|*|' + _i2] += 1
        _playlist_counts = [([0] * len(self.all_tags)) for i in range(len(self.all_tags))]
        print(_playlist_counts)
        if len(tag_to_count):
            for k, v in tag_to_count.items():
                _i1 = k.split('|*|')[0]
                _i2 = k.split('|*|')[1]
                index1 = self.all_tags.index(_i1)
                index2 = self.all_tags.index(_i2)
                #                print(_i1,_i2,v,index1,index2)
                _playlist_counts[index1][index2] = v
                _playlist_counts[index2][index1] = v

        return _playlist_counts

    def cal_playlist_rec(self):
        """
        计算每个tag之间的相似度
        通过
        |N(i)&N(j)|/sqrt(N(i)*N(j))

        :return:
        """
        tag_sim_matrix = [([0] * len(self.all_tags)) for i in range(len(self.all_tags))]
        for i in range(len(self.playlist_counts)):
            for j in range(len(self.playlist_counts)):
                mixed_data = self.playlist_counts[i][j]  # 喜欢i和j共同的人数
                i_data = self.tag_one_count[self.all_tags[i]]  # 获取i的数量
                j_data = self.tag_one_count[self.all_tags[j]]  # 获取i的数量

                tag_sim_matrix[i][j] = mixed_data / math.sqrt(i_data * j_data)
        return tag_sim_matrix

    # 获取每个歌单相关的tag 推荐
    def recommend(self):

        pass


class Playlistsim:
    """
    获取歌单之间的相似度
       """

    def __init__(self):
        self.playtag = self.getPlayTags()
        self.sim = self.getSingSim()

    def getPlayTags(self):
        playlistTagDict = dict()
        if not os.path.exists(dir_data_path + '/playlist_all.txt'):
            f = open(dir_data_path + '/playlist_all.txt', 'w')
            for _ in PlayInfo.objects.all().values_list('play_id', 'tag', 'forward'):
                _id = _[0]
                tag = _[1]
                forward = _[2]
                if forward == '' or forward is None:
                    forward = "1"
                if tag is "" or tag is None:
                    tag = '其他'
                # print(str(_id) + SPLIT2 + tag + SPLIT2 + forward)
                f.write(str(_id) + SPLIT2 + tag + SPLIT2 + forward + '\n')
            f.close()

        with open(dir_data_path + '/playlist_all.txt', 'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                if line == '':
                    continue
                split_data = line.split(SPLIT2)
                playid = split_data[0]  # playlistid
                tags = split_data[1]  # tag
                for tag in tags.split(SPLIT):
                    playlistTagDict.setdefault(str(playid), set())

                    playlistTagDict[str(playid)].add(tag)
        return playlistTagDict

    def getSingSim(self):
        sim = dict()
        if os.path.exists(dir_data_path + "playlist_sim.json"):
            sim = json.load(open(dir_data_path + "playlist_sim.json", "r", encoding="utf-8"))
        else:
            i = 0
            for sing1 in self.playtag.keys():
                sim[sing1] = dict()
                for sing2 in self.playtag.keys():
                    if sing1 != sing2:
                        j_len = len(self.playtag[sing1] & self.playtag[sing2])
                        if j_len != 0:
                            result = j_len / len(self.playtag[sing1] | self.playtag[sing2])
                            if sim[sing1].__len__() < 20 or result > 0.8:
                                sim[sing1][sing2] = result
                            else:
                                # 找到最小值 并删除
                                minkey = min(sim[sing1], key=sim[sing1].get)
                                del sim[sing1][minkey]
                i += 1
                print(str(i) + "\t" + str(sing1))
            json.dump(sim, open(dir_data_path + "playlist_sim.json", "w", encoding="utf-8"))
        print("歌单相似度计算完毕！")
        return sim

    def transform(self):
        fw = open(dir_data_path + "playlist_sim.txt", "a", encoding="utf-8")
        for s1 in self.sim.keys():
            for s2 in self.sim[s1].keys():
                fw.write(s1 + "," + s2 + "," + str(self.sim[s1][s2]) + "\n")
        fw.close()
        print("Over!")


def playlistsim_to_mysql():
    """
    歌手相似度写入数据库
    :return:
    """

    with open(dir_data_path + 'playlist_sim.txt', 'r') as f:
        playlistinfo = {}
    for line in f.readlines():
        line = line.strip()
        if line == '':
            continue
        s1 = line.split(',')[0]
        s2 = line.split(',')[1]
        sim = line.split(',')[2]
        print(s1, s2, sim)
        playlist_instance1 = playlistinfo.get(s1, False)
        playlist_instance2 = playlistinfo.get(s2, False)
        if not playlist_instance1:
            playlist_instance1 = PlayInfo.objects.get(play_id=s1)
            playlistinfo[s1] = playlist_instance1
        if not playlist_instance2:
            playlist_instance2 = PlayInfo.objects.get(play_id=s2)
            playlistinfo[s2] = playlist_instance2

        PlayListSim.objects.create(playlist=playlist_instance1, sim_playlist=playlist_instance2,
                                   sim=sim)


if __name__ == '__main__':
    # recplay = RecPlayList()
    # recplay._data_from_mysql()
    # playsim = Playlistsim()
    # playsim.transform()
    playlistsim_to_mysql()
