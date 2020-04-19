import os
import sys
import django

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
os.chdir(dir_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_rec.settings")
django.setup()

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.chrome.options import Options
from music_rec.settings import CHROME_PATH, SPLIT

from playlist.models import PlayInfo
from song.models import SongInfo
from sing.models import SingInfo
import requests
import json

local_path = os.path.dirname(os.path.abspath(__file__))
f = open(local_path + '/data/sing.txt', 'r')


class SingSpider:
    def __init__(self):

        self.all_authors=[]
        for line in f.readlines():
            line = line.strip('\n')
            if line == '' or line in self.all_authors:
                continue
            self.all_authors.append(line)

    def author_from_txt(self):
        for _ in self.all_authors:
            sing_id=_.split(SPLIT)[0]
            name=_.split(SPLIT)[1]
            if SingInfo.objects.filter(sing_id=sing_id).exists():
                continue
            SingInfo.objects.create(sing_id=sing_id,name=name)



if __name__=='__main__':
    singspider=SingSpider()
    singspider.author_from_txt()