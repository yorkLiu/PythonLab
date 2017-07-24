# -*- coding: UTF-8 -*-
# coding:utf-8
import logging
import os

YHD_ALL_CATEGORY_URL='http://www.yhd.com/marketing/allproduct.html'
YHD_BASE_CHAT_URL ="http://webim.yhd.com/imFront/frontCheckPoint.action?merchantId={merchantId}&positionId=1&mcSiteId=3&sut=&csrInfo=%27%27&productInfo=&productId=0&pmInfoId=0&orderCode=0&sellerType=0"

# the max count page to get the merchant
MAX_FIND_PAGE_COUNT=20

# 第抓取到多少个 merchantId, 就存到文件中
EVERY_COUNT_WRITE_TO_FILE=10

# exclusive store names, split with comma (',')
EXCLUSIVE_STORE_NAMES='1号店自营'


LOGGER_FORMAT = '%(levelname)s:%(name)s:%(message)s'
logging.basicConfig(format=LOGGER_FORMAT)
logger = logging.getLogger('AD-YHD')
logger.setLevel(logging.INFO)

################ Configuration ENV START##################################
SAY_HI_BEFORE_MESSAGE=True

# phantomjs install path
PHANTOMJS_INSTALL_PATH='/Users/yongliu/Project/webDriver/phantomjs'
# output_dir
OUTPUT_DIR=os.path.join(os.path.expanduser("~"), 'YHD')


# store the merchants id file name from crawled
CRAWLED_MERCHANT_FILE_NAME_PREFIX='Crawled_Merchants_'
################ Configuration ENV END####################################

def get_output_dir():
    return OUTPUT_DIR

def get_webdriver_install_path():
    return PHANTOMJS_INSTALL_PATH



