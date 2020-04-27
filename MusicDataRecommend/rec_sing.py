import sys
import django
import os

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
os.chdir(dir_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_rec.settings")
django.setup()

dir_data_path = os.path.dirname(os.path.abspath(__file__)) + '/data/'

from sing.models import SingTag, SingSim, SingInfo
import json


class SingSimClass:
    """
    获取歌手之间的相似度
    """

    def __init__(self):
        self.singTags = self.getSingTags()
        self.sim = self.getSingSim()

    def getSingTags(self):
        singTagsDict = dict()
        for _ in SingTag.objects.all().values_list("sing_id", "name"):
            singTagsDict.setdefault(str(_[0]), set())
            singTagsDict[str(_[0])].add(_[1])

        return singTagsDict

    def getSingSim(self):
        sim = dict()
        if os.path.exists(dir_data_path + "sing_sim.json"):
            sim = json.load(open(dir_data_path + "sing_sim.json", "r", encoding="utf-8"))
        else:
            i = 0
            for sing1 in self.singTags.keys():
                sim[sing1] = dict()
                for sing2 in self.singTags.keys():
                    if sing1 != sing2:
                        j_len = len(self.singTags[sing1] & self.singTags[sing2])
                        if j_len != 0:
                            result = j_len / len(self.singTags[sing1] | self.singTags[sing2])
                            if sim[sing1].__len__() < 20 or result > 0.8:
                                sim[sing1][sing2] = result
                            else:
                                # 找到最小值 并删除
                                minkey = min(sim[sing1], key=sim[sing1].get)
                                del sim[sing1][minkey]
                i += 1
                print(str(i) + "\t" + str(sing1))
            json.dump(sim, open(dir_data_path + "sing_sim.json", "w", encoding="utf-8"))
        print("歌曲相似度计算完毕！")
        return sim

    def transform(self):
        fw = open(dir_data_path + "sing_sim.txt", "a", encoding="utf-8")
        for s1 in self.sim.keys():
            for s2 in self.sim[s1].keys():
                fw.write(s1 + "," + s2 + "," + str(self.sim[s1][s2]) + "\n")
        fw.close()
        print("Over!")


def singsim_to_mysql():
    """
    歌手相似度写入数据库
    :return:
    """

    singinfo = {}
    with open(dir_data_path + 'sing_sim.txt', 'r') as f:
        i = 0
        bulk_insert = []
        for line in f.readlines():
            line = line.strip()
            if line == '':
                continue
            s1 = line.split(',')[0]
            s2 = line.split(',')[1]
            sim = line.split(',')[2]
            print(s1, s2, sim)
            sing_instance1 = singinfo.get(s1, False)
            sing_instance2 = singinfo.get(s2, False)
            if not sing_instance1:
                sing_instance1 = SingInfo.objects.get(sing_id=s1)
                singinfo[s1] = sing_instance1
            if not sing_instance2:
                sing_instance2 = SingInfo.objects.get(sing_id=s2)
                singinfo[s2] = sing_instance2
            bulk_insert.append(SingSim(sing=sing_instance1, sim_sing=sing_instance2, sim=sim))
            i += 1
            if i >=1000:
                SingSim.objects.bulk_create(bulk_insert)

                print('1000条数据插入成功')
                bulk_insert=[]
                i = 0

        if bulk_insert:
            SingSim.objects.bulk_create(bulk_insert)
            print('1000条数据插入成功')
            bulk_insert = []
            i = 0


if __name__ == '__main__':
    sing = SingSimClass()
    sing.transform()
   # singsim_to_mysql()
