# -*- coding: UTF-8 -*-
import requests
import xml.dom.minidom
from bs4 import BeautifulSoup
import urllib
import re
import json
import time
from collections import deque
from multiprocessing import Pool
import contextlib
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

queue=deque() #创建队列
play={}      #创建元组
playurls=[]


def getTagText(tag):
        rc = ""
        dom=xml.dom.minidom.parse("play.xml")
        node = dom.getElementsByTagName(tag)[0]
        for node in node.childNodes:
            if node.nodeType in ( node.TEXT_NODE, node.CDATA_SECTION_NODE):
                rc=node.data
        return rc

music="http://play.baidu.com/data/music/songlink?songIds=$0$&hq=0&type=m4a,mp3&rate=%27%27&pt=0&flag=-1&s2p=-1&prerate=-1&bwt=-1&dur=-1&bat=-1&bp=-1&pos=-1&auto=-1"

headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
            'Referer':'http://play.xml.baidu.com/',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive'
        }

def DownHtml(url):
        print url
        try:
           savePlay=getTagText("savePlay")
           print("准备开始解析页面："+url+"  请稍候...")
           html=requests.get(url,headers=headers,timeout=2000)
           html.encoding="utf-8"
           soup=BeautifulSoup(html.text,"html.parser")
           div_html=soup.find("div",class_="search-song-list song-list song-list-hook")
           span_html=re.findall('<span class="music-icon-hook" data-musicicon=\'(.*?)\'>',str(div_html))
           for v in span_html:
               data=json.loads(v)
               play=data["id"],data["songTitle"]
               queue.append(play)
           while queue:
               time.sleep(5)
               music_tuple=queue.popleft()
               playUrl=music.replace("$0$",music_tuple[0])
               print(music_tuple[1]+".mp3进入下载通道,开始排队等待...\n")
               resultJson=requests.get(playUrl,headers=headers,timeout=2000)
               data=resultJson.json()
               if not data['data']:
                   pass
               else:
                   v=data["data"]["songList"][0]
                   print("正在下载, "+v["songName"]+".mp3 ...\n")
                   time.sleep(2)
                   urllib.urlretrieve(v["songLink"],savePlay+v["songName"]+".mp3")
                   print(v["songName"]+".mp3 下载完成,下载路径:"+savePlay+v["songName"]+".mp3")
        except Exception as e:
            print e
            pass

if __name__=="__main__":
    start = time.time()
    pageSize=int(getTagText("pageSize"))
    pageIndex=20
    url=getTagText("url")
    playurls.append(url)
    if pageSize>1:
        for v in range(pageSize):
            if v>0:
                purl=url+"?start="+str(pageIndex)+"&size=20&third_type=0"
                playurls.append(purl)
                pageIndex+=25

    with contextlib.closing(Pool(processes=4)) as pool:
        pool.map(DownHtml, playurls)
    print playurls
    print '本次下载共用时：', (time.time()-start)