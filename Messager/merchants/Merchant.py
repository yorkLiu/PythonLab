# -*- coding: utf-8 -*-
# coding:utf-8

from scrapy.selector import Selector
import requests
import json
import os
from merchants.Category import Category
import config
from config import logger
from utils import Utils


def crawl_merchant():
    m = Merchant()
    m.run()

class Merchant:

    def __init__(self):
        self.merchant_set=set()
        self.pagging_suffix='#page=%s&sort=1'

        self.crawled_merchant_file_name=Utils.get_today_crawled_file_name()


    def parse(self, url):
        base_url = url
        temp_set = set()

        for i in range(1, config.MAX_FIND_PAGE_COUNT+1):
            if i > 1:
                url_idx=base_url.format(page=i)
            else:
                url_idx = url

            print url_idx
            r = requests.get(url_idx)
            html_content = r.content
            selector = Selector(text=html_content, type='html')

            if i == 1:
                sel_url = selector.xpath('//input[@id="jsonUrlValue"]/@value')
                if sel_url:
                    jsonstr = sel_url.extract()[0]
                    jsona = json.loads(jsonstr, strict=True)
                    base_url = Utils.convert_yhd_url(jsona['searchUrl']).replace('p1', 'p{page}')
                    # print base_url

            for sel in selector.xpath('//p[contains(@class, "storeName")]'):
                merchantId = sel.xpath('string(./a/@merchantid)').extract()[0]
                storeName = unicode(sel.xpath('string(./a/@title)').extract()[0]).encode('utf-8')
                # print merchantId
                # print merchantId, storeName
                # logger.info("store name: %s, Merchant ID: %s", storeName, merchantId)

                if merchantId and storeName not in (config.EXCLUSIVE_STORE_NAMES.split(",")):
                    if merchantId not in self.merchant_set:
                        self.merchant_set.add(merchantId)
                        temp_set.add(merchantId)
                        if len(temp_set) == config.EVERY_COUNT_WRITE_TO_FILE:
                            Utils.append_contents_to_file(self.crawled_merchant_file_name, temp_set)
                            temp_set.clear()

            # check the temp_set is empty or not
            # if not empty, need write the content to file
            if len(temp_set) > 0:
                Utils.append_contents_to_file(self.crawled_merchant_file_name, temp_set)
                temp_set.clear()


    def run(self):
        self.merchant_set.clear()
        ###### pre-fill the crawled merchant [START]################################
        crawled_contents = Utils.get_file_contents(self.crawled_merchant_file_name)
        self.merchant_set = set(crawled_contents if crawled_contents else [])
        ###### pre-fill the crawled merchant [END]##################################

        for c in Category().get_all_categories():
            url = c['url']
            text = c['text']
            logger.info('Crawl the category: %s with the url: %s', text, url)
            self.parse(url)

        print "Crawl the YHD merchant DONE."

