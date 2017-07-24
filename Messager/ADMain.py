#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding:utf-8

from multiprocessing import Value, Queue, Process
import os
import config
from merchants.Message import run_send_msg
from merchants.Merchant import crawl_merchant
import argparse
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def run(username, password, msg):
    """
    start the program
    :param username:
    :param password:
    :param msg:
    :return:
    """
    p_crawler = Process(target=crawl_merchant)
    p_messager = Process(target=run_send_msg, args=(username, password, msg))
    p_crawler.start()
    p_messager.start()

    p_crawler.join()
    p_messager.join()

    # print p_crawler.pid
    print p_messager.pid

if __name__ == "__main__":
    help_text = """
        -d <output dir> Output dir path
        -u <username> YHD login username
        -p <password> YHD login password
        -m <message> Send merchant message
        Usage:
           python ADMain.py -u testUser -p testPwd -m 'this is a test message'
    """
    parser = argparse.ArgumentParser(description='Simulate to login YHD', add_help=True)
    parser.add_argument('-u', '--username',  help='YHD login user name', default='')
    parser.add_argument('-p', '--password',  help='YHD login password', default='')
    parser.add_argument('-m', '--message',  help='Send Merchant message', default='')
    parser.add_argument('-d', '--outputdir',  help='Output dir path', default='')
    parser.add_argument('-wp', '--webdriverpath',  help='The WebDriver path', default='')

    options = parser.parse_args()

    if options.outputdir:
        config.OUTPUT_DIR = os.path.expanduser(options.outputdir)

    if options.webdriverpath:
        config.PHANTOMJS_INSTALL_PATH = os.path.expanduser(options.webdriverpath)

    if options.username and options.password and options.message:
        run(options.username, options.password, options.message)
    else:
        print help_text



# # if __name__ == "main":
# msg = '专 > 业 > 刷 > 单, 全 > 人 > 工，量 > 大 > 从 > 优, 详 > 询 > 客 > 服 Q::Q:: 1514652955'
# username = '17164309540'
# password = 'ecu303'
#
# # p_merchant = Process(target=crawl_merchant)
# p_msg = Process(target=run_send_msg, args=(username,password, msg))
#
# # p_merchant.start()
# p_msg.start()
#
# # p_merchant.join()
# p_msg.join()
#
# # m = set(['242021', '39326','7936','154819', '70339','168405','238012'])
# # run_send_msg(username, password, msg, m)






