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
import time
import random
from music_rec.settings import CHROME_PATH, SPLIT

from playlist.models import PlayInfo

local_path=os.path.dirname(os.path.abspath(__file__))

class PlayListSpider:
    netcloud_url = 'https://music.163.com/#'
    playlist_baseurl = 'https://music.163.com/#/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit={}&offset={}'
    END = 10  # 终止列表

    def get_playlist(self):
        """
        获取热门歌单列表 id:网址
        :return: None
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors')

        for i in range(self.END):
            driver = webdriver.Chrome(executable_path=CHROME_PATH, chrome_options=chrome_options)
            playlist_info = {}
            url = self.playlist_baseurl.format('35', str(i * 35))
            driver.get(url)
            driver.switch_to.frame('g_iframe')
            wait = ui.WebDriverWait(driver, 30)

            try:
                wait.until(lambda driver: driver.find_elements_by_xpath(
                    '//ul[@id="m-pl-container"]/li/p[@class="dec"]/a'))
            except Exception:
                print('没有"m-pl-container"的标签，歌单推荐页')

            link_ids = driver.find_elements_by_xpath(
                '//ul[@id="m-pl-container"]/li/p[@class="dec"]/a')
            for _link in link_ids:
                platlist_url: str = _link.get_attribute('href')
                print(platlist_url)
                id = platlist_url.split('=')[1]
                playlist_info[id] = platlist_url

            with open('data/platlist.txt', 'a') as f:
                for k, v in playlist_info.items():
                    f.write('\n' + k + SPLIT + v)
            time.sleep(random.choice(list(range(4, 6))))

    def playlist_info(self):
        """
        获取具体的歌单信息
        :return:
        """
        all_playlists = []
       # print(sys.argv[0])
        #os.path.exists('./NetCloudSpide')
        if os.path.exists(local_path+'/data/left_playlist.txt'):
            with open(local_path+'/data/left_playlist.txt', 'r') as f:
                for line in f.readlines():
                    line = line.strip('\n')
                    if line == '':
                        continue
                    all_playlists.append(line)
        else:
            with open(local_path+'/data/platlist.txt', 'r') as f:
                for line in f.readlines():
                    line = line.strip('\n')
                    if line == '':
                        continue
                    all_playlists.append(line)
        # 先爬取前0-50个歌单
        start_ = 50
        end_ = 500

        for i in range(start_, end_):
            _ = all_playlists[i]

            playlist_id = _.split(SPLIT)[0]
            playlist_url = _.split(SPLIT)[1]
            if PlayInfo.objects.filter(play_id=playlist_id).exists():
                print(f'歌单{playlist_id}已经存在')
                continue
            try:
                print(_)
                self._get_playlist_info(playlist_id, playlist_url)
            except:
                print('Error:url or selenium  wrong', playlist_id, playlist_url)
                f = open(local_path + '/data/left_playlist.txt', 'w')
                for i in all_playlists[i:]:
                    _id = i.split(SPLIT)[0]
                    _url = i.split(SPLIT)[1]
                    f.write('\n' + _id + SPLIT + _url)
                    break

                f.close()

    def _get_playlist_info(self, id: str, url: str):
        """
        歌单图片链接 歌单名称 歌单作者 歌单播放量 歌单标签(可能存在没有) tag
        歌单描述 歌单收藏量 歌单评论数 歌单描述  歌单里面的歌曲列表
        :param id: 歌单id
        :param url:  歌单url
        :return:
        """
        chrome_options = Options()

        # chrome_options = self._random_proxy(chrome_options)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(executable_path=CHROME_PATH, chrome_options=chrome_options)
        driver.get(url)
        driver.implicitly_wait(5)
        driver.switch_to.frame('g_iframe')
        wait = ui.WebDriverWait(driver, 10)
        try:
            wait.until(
                lambda driver: driver.find_element_by_tag_name('table'))
        except Exception:
            print('没有"m-table"的标签，歌单详情页')

        # with open('data/playlis_detail.html','w') as f:
        #     f.write(driver.page_source)
        # 歌单标题
        list_title = driver.find_element_by_xpath('//div[contains(@class,"tit")]/h2').text
        # 歌单图片链接
        list_img = driver.find_element_by_xpath(
            '//div[@class="cover u-cover u-cover-dj"]/img').get_attribute('data-src')
        # 歌单作者:
        list_author = driver.find_element_by_xpath('//div[@class="user f-cb"]/span/a').text
        # 歌单标签 和描述 都可能存在有和没有
        tag = driver.find_elements_by_xpath('//div[@class="tags f-cb"]/a[@class="u-tag"]/i')
        list_tag = ''
        if tag is not None:
            _tags = []
            for _ in tag:
                _tags.append(_.text)
            list_tag = f'{SPLIT}'.join(_tags)
        list_describe = ''
        try:
            _describe = driver.find_element_by_xpath('//p[@id="album-desc-more"]')
            if _describe is not None:
                list_describe = driver.find_element_by_xpath(
                    '//p[@id="album-desc-more"]').get_attribute('innerHTML')
        except:
            ...
        # 歌单收藏量
        list_collection = driver.find_element_by_xpath('//div[@class="btns f-cb"]/a[3]/i').text[
                          1:-1]
        # 歌单分享量
        list_forward = driver.find_element_by_xpath('//div[@class="btns f-cb"]/a[4]/i').text[1:-1]
        # 歌单评论数
        list_comment = driver.find_element_by_xpath('//div[@class="btns f-cb"]/a[6]/i/span').text
        # 歌单播放量
        list_amount = driver.find_element_by_xpath('//div[@class="n-songtb"]//strong').text
        # 歌单里面的歌曲
        list_song = []
        all_song = driver.find_elements_by_xpath(
            '//div[@id="m-playlist"]//div[@class="n-songtb"]//tr/td[2]//a')
        for link in all_song:
            platlist_url: str = link.get_attribute('href')
            song_id = platlist_url.split('=')[1]
            # list_song.append(song_id + SPLIT + platlist_url)\
            list_song.append(song_id)

        data = {
            'title': list_title,
            'img': list_img,
            'author': list_author,
            'tag': list_tag,
            'describe': list_describe,
            'collection': list_collection,
            'forward': list_forward,
            'comment': list_comment,
            'amount': list_amount,
            'songs': ','.join(list_song),
            'play_id': id,
        }
        #  print(data)
        if not PlayInfo.objects.filter(play_id=id).exists():
            PlayInfo.objects.create(**data)
            # db_playlist.insert_one(data)
            print("数据插入成功", end='--')
            print(data)
        else:
            print('该数据已经存在')
        # driver.quit()
        time.sleep(random.choice(list(range(1, 4))))


if __name__ == '__main__':

    netcloud = PlayListSpider()
    # netcloud.get_playlist()
    netcloud.playlist_info()
    url = 'https://music.163.com/playlist?id=3129764102'
    #netcloud._get_playlist_info('3129764102', url)
    ...
