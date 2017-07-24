# coding:utf-8
# -*- coding: utf-8 -*-
import config
import requests
import scrapy

class Category:


    def get_all_categories(self):
        """
        Get all merchants for all categories
        :return: array of all category urls
        [
            {url: category url, text: category name}...
        ]
        """
        results = []
        r = requests.get(config.YHD_ALL_CATEGORY_URL)
        html_content = r.content
        selector = scrapy.Selector(text=html_content, type='html')
        for sel in  selector.xpath("//div[@class='mt']//a"):
            href = str(sel.xpath('@href').extract()[0]).replace("//", 'http://')
            text = unicode(sel.xpath('text()').extract()[0]).encode('utf-8')
            results.append({'url': href, 'text': text})

        return results

    @staticmethod
    def get_all_categories_urls_only():
        """
        Get all merchants for all categories (urls only)
        :return: array of all category urls
        """
        urls = []
        for c in Category().get_all_categories():
            urls.append(c['url'])

        print urls

    def get_categories(self, category_names):
        """
        Get the associated @category_names merchants
        :param category_names:
        :return: array of merchants IDs
        """

        pass
