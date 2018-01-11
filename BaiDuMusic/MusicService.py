# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import os
import re
import json
from collections import deque
import time
import urllib
import requests
from multiprocessing import Pool
import contextlib
from functools import partial

from bs4 import BeautifulSoup

import MessageResource as MsgRes
from MusicInfo import MusicInfo


############### fixed python multiprocessing issue in class [start] ###########################
## refer: https://blog.tankywoo.com/2015/09/06/cant-pickle-instancemethod.html
import copy_reg
import types
def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)
############### fixed python multiprocessing issue in class [end] #############################


music_tag_url_prefix='http://music.baidu.com/tag/'
# 1: 新歌榜
# 2: 热歌榜
# 6: KTV热歌榜
# 7: 叱咤歌曲榜
# 8: Billboard
# 9: 雪碧音碰音榜
# 11: 摇滚榜
# 14: 影视金曲榜
# 18: Hito中文榜
# 20: 华语金曲榜
# 21: 欧美金曲榜
# 22: 经典老歌榜
# 23: 情歌对唱榜
# 24: 影视金曲榜
music_category_url='http://tingapi.ting.baidu.com/v1/restserver/ting?from=android&version=5.6.5.0&method=baidu.ting.billboard.billList&format=json&type={typeId}&offset={offset}&size={totalCount}'
music_search_url='http://tingapi.ting.baidu.com/v1/restserver/ting?from=android&version=5.6.5.0&method=baidu.ting.search.catalogSug&format=json&query={queryText}'

download_music_url='http://play.baidu.com/data/music/songlink?songIds={songIds}&hq=0&type=m4a,mp3&rate=%27%27&pt=0&flag=-1&s2p=-1&prerate=-1&bwt=-1&dur=-1&bat=-1&bp=-1&pos=-1&auto=-1'



class MusicService:
    def __init__(self):
        self.queue = deque()

    def findMusicByTag(self, tag):
        urls = []
        baseUrl = music_tag_url_prefix + tag
        pageIndex = 20
        urls.append(baseUrl)
        for i in range(1):
            pageIndex = (i+1) * pageIndex
            pageUrl = baseUrl+"?start="+str(pageIndex)+"&size=20&third_type=0"
            urls.append(pageUrl)

        for url in urls:
            print("Ready resolve url：[%s] please wait..." % url)
            html = requests.get(url, headers=MsgRes.get_header(), timeout=2000)
            html.encoding = "utf-8"
            soup = BeautifulSoup(html.text, "html.parser")
            div_html = soup.find("div", class_="search-song-list song-list song-list-hook")
            span_html = re.findall('<span class="music-icon-hook" data-musicicon=\'(.*?)\'>', str(div_html))
            for v in span_html:
                data = json.loads(v)
                print data

    def findMusicByCategory(self, categoryId):
        # url = music_category_url.format(typeId=categoryId, offset=offset, totalCount=MsgRes.every_page_show_count)
        field_mapping={'root': 'song_list',
                       'song_id':'song_id',
                       'author':'author',
                       'title':'title',
                       'info':'info',
                       }
        result = []
        for i in range(MsgRes.total_search_page_count):
            offset = i * MsgRes.every_page_show_count
            url = music_category_url.format(typeId=categoryId, offset=offset, totalCount=MsgRes.every_page_show_count)
            data = self.getData(url, field_mapping)
            if len(data) == 0:
                break

            result.extend(data)

        return result

    def searchMusic(self, searchText):
        if searchText:
            url = music_search_url.format(queryText=searchText)
            field_mapping = {'root': 'song',
                             'song_id': 'songid',
                             'author': 'artistname',
                             'title': 'songname',
                             'info': 'info',
                             }
            return self.getData(url, field_mapping)

        else:
            return self.findMusicByCategory(MsgRes.default_search_type_id)

    def getData(self, url, mappingMap):
        results = []
        if url:
            r = requests.get(url, headers=MsgRes.get_header(), timeout=3000)
            data = json.loads(r.content, encoding='utf-8')
            if mappingMap['root'] in data and data[mappingMap['root']]:
                for item in data[mappingMap['root']]:
                    song_id = item[mappingMap['song_id']]
                    song_author = item[mappingMap['author']]
                    song_title = item[mappingMap['title']]
                    song_info = item[mappingMap['info']]
                    results.append(MusicInfo(song_id, song_author, song_title, song_info))
        return results

    def downloadMusicWithMultipleProcess(self, songIds):
        start = time.time()
        self.queue.extendleft(songIds)
        max_processes_count = 4 if len(songIds) > 4 else 1

        with contextlib.closing(Pool(processes=max_processes_count)) as pool:
            pool.map(self.downloadMusic, list(songIds))

        print "Done.. Spend:", (time.time()-start)

    def downloadMusic(self, songId):
        download_folder_path = MsgRes.default_download_music_folder_path
        MsgRes.checkpath(download_folder_path)
        try:
            if songId:
                self.queue.remove(songId)
                print '--8******self.queue:', self.queue, '-:', len(self.queue)
                download_url = download_music_url.format(songIds=songId)
                result = requests.get(download_url, headers=MsgRes.get_header(), timeout=3000)
                if not result:
                    pass
                data = result.json()
                if not data['data']:
                    pass
                else:
                    v = data["data"]["songList"][0]
                    song_name = v['songName']
                    song_link = v['songLink']
                    # str(song_link).split("?")[0]

                    print("正在下载, %s.mp3" % song_name)
                    time.sleep(1)
                    music_file_name = os.path.join(download_folder_path, '%s%s' % (song_name, '.mp3'))
                    urllib.urlretrieve(song_link, music_file_name)
                    print('%s 下载完成,存放在: [%s]' % ('%s%s' % (song_name, '.mp3'), music_file_name))
        except:
            pass



    def getReminderDownload(self):
        print 'queue len:', len(self.queue)
        return len(self.queue)

    # def downloadMusic(self, songIds):
    #     queue= deque()
    #     queue.extendleft(songIds)
    #     download_folder_path = MsgRes.default_download_music_folder_path
    #     MsgRes.checkpath(download_folder_path)
    #     while queue:
    #         songId = queue.popleft()
    #         download_url = download_music_url.format(songIds=songId)
    #         result = requests.get(download_url, headers=MsgRes.get_header(),timeout=3000)
    #         data = result.json()
    #         if not data['data']:
    #             pass
    #         else:
    #             v = data["data"]["songList"][0]
    #             song_name = v['songName']
    #             song_link = v['songLink']
    #             # str(song_link).split("?")[0]
    #
    #             print("正在下载, %s.mp3" %  song_name)
    #             time.sleep(2)
    #             music_file_name = os.path.join(download_folder_path, '%s%s' % (song_name, '.mp3'))
    #             urllib.urlretrieve(song_link,  music_file_name)
    #             print('%s 下载完成,存放在: [%s]' % ('%s%s' % (song_name, '.mp3'), music_file_name) )

if __name__ == "__main__":
    q = deque()
    q.extendleft([1,2,3,4,5,6,7])
    print q, len(q)
    q.remove(1)
    print q, len(q)