# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests, hashlib, sys, click, re, base64, binascii, json, os

class Ting56Pipeline(object):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Proxy-Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, sdch",
        # 'Connection': 'close',
    }
    download_folder = "tingshu"
    download_session = requests.Session()
    timeout = 60
    def process_item(self, item, spider):
        downloadUrl = item['url']
        chapterName = self.getChapterName(downloadUrl)
        # downloadUrl = 'http://m10.music.126.net/20181029213938/19503101df87d152a129efa7df304978/ymusic/75c0/3926/f381/769f28f87045c3e415ae1445da03e67b.mp3'
        self.get_song_by_url(downloadUrl,chapterName,self.download_folder)
        return item

    def getChapterName(self,strSource):
        # retlist = re.findall("\/(.*?).mp3", strSource)
        retlist = strSource.split("/")
        mp3Name = retlist[len(retlist)-1]
        retlist2 = re.findall("(.*?).mp3", mp3Name)
        return retlist2[0]

    def get_song_by_url(self, song_url, song_name, folder):
        """
        下载歌曲到本地
        :params song_url: 歌曲下载地址
        :params song_name: 歌曲名字
        :params song_num: 下载的歌曲数
        :params folder: 保存路径
        """
        if not os.path.exists(folder):
            os.makedirs(folder)
        # fpath = os.path.join(folder, str(song_num) + '_' + song_name + '.mp3')
        fpath = os.path.join(folder, song_name + '.mp3')
        if sys.platform == 'win32' or sys.platform == 'cygwin':
            valid_name = re.sub(r'[<>:"/\\|?*]', '', song_name)
            if valid_name != song_name:
                # click.echo('{} will be saved as: {}.mp3'.format(song_name, valid_name))
                fpath = os.path.join(folder, valid_name + '.mp3')

        if not os.path.exists(fpath):

            resp = requests.get(
                song_url, headers=self.headers, timeout=60, stream=True)

            # resp = requests.Session().get(song_url, headers=self.headers, allow_redirects=False)
            # resp = requests.Session().get(song_url, headers=self.headers, timeout=60, stream=True)
# allow_redirects=False的意义为拒绝默认的301/302重定向从而可以通过html.headers[‘Location’]拿到重定向的URL
#             resume_url = resp.headers['location']


            # length = int(resp.headers.get('content-length'))
            with open(fpath, 'wb') as song_file:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        song_file.write(chunk)