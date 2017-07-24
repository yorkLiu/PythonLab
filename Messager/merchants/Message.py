# -*- coding: UTF-8 -*-
# coding:utf-8
import os
import json
import requests
import re
import datetime
import time
import sys
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
from config import logger
from merchants.UserInfo import UserInfo
from exception.Exceptions import MerChantException
from exception.Exceptions import UserLoginFailedException
from utils import Utils


reload(sys)
sys.setdefaultencoding("utf-8")

def run_send_msg(username, password, adv_msg):
    msg = Message(adv_msg)
    msg.run(username, password)

def run_send_msg_batch(username, password, adv_msg, merchants):
    msg = Message(adv_msg)
    msg.run_batch(username, password, merchants)

class Message:

    def __init__(self, adv_msg):
        self.yhd_login_url = 'https://passport.yhd.com/passport/login_input.do'
        self.yhd_user_cid_url = 'http://webim.yhd.com/customer/login.action?jsonpCallback=cid'
        self.yhd_check_merchant_url='http://webim.yhd.com/customer/route.action?jsonpCallback=a&positionId=1&rightQueryStr=%7B%22pmInfoId%22%3A%220%22%2C%22productId%22%3A%220%22%2C%22orderCode%22%3A%220%22%2C%22merchantId%22%3A%{merchantId}%22%2C%22positionId%22%3A%221%22%2C%22mcSiteId%22%3A%223%22%2C%22sellerType%22%3A%220%22%7D&merchantId={merchantId}&cid={cid}&sellerType=0'
        self.yhd_chat_url='http://webim.yhd.com/imFront/frontCheckPoint.action?merchantId={merchantId}&positionId=1&mcSiteId=3&sut=&csrInfo=%27%27&productInfo=&productId=0&pmInfoId=0&orderCode=0&sellerType=0'


        self.today_label = datetime.datetime.today().strftime('%Y-%m-%d')
        self.sent_merchant_txt_file_name = os.path.join(config.get_output_dir(), 'Sent_Merchants_%s.txt' % self.today_label)
        self.failed_sent_merchant_txt_file_name = os.path.join(config.get_output_dir(), 'Failed_Sent_Merchants_%s.txt' % self.today_label)

        self.adv_message = adv_msg

        self.driver = webdriver.PhantomJS(config.get_webdriver_install_path())
        self.driver.maximize_window()

    def take_screenshot(self, filename):
        filepath = os.path.join(config.get_output_dir(), filename)
        self.driver.get_screenshot_as_file(filepath)
        return filepath

    def save_success_send_file(self, content):
        Utils.append_content_to_file(self.sent_merchant_txt_file_name, content)

    def save_failed_send_file(self, content):
        Utils.append_content_to_file(self.failed_sent_merchant_txt_file_name, content)

    def try_login(self, username, password, u_ele_id, p_ele_id, v_ele_id):
        """
        try to login
        :param username: user name
        :param password: password
        :param u_ele_id: username element id
        :param p_ele_id: password element id
        :param v_ele_id: vcode element id
        :return:
        """
        login_success = False

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, u_ele_id)))
        u_ele = self.driver.find_element_by_id(u_ele_id)
        p_ele = self.driver.find_element_by_id(p_ele_id)
        u_ele.clear()
        p_ele.clear()

        u_ele.send_keys(username)
        p_ele.send_keys(password)
        p_ele.send_keys(Keys.ENTER)

        for i in range(4):
            try:
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'hd_login_name')))
                login_success = True
                break
            except TimeoutException, e:
                vcode_ele = self.driver.find_element_by_id('vcd')
                if vcode_ele and vcode_ele.is_displayed():
                    file_path = self.take_screenshot('input_vcode_%s.png' % username)
                    vcode_inputted = raw_input("Please enter the the vcode with open [%s]: " % file_path)
                    vcode_ele.send_keys(vcode_inputted)
                    p_ele.send_keys(Keys.ENTER)


        return login_success

    def login(self, username, password):
        try:
            self.driver.get(self.yhd_login_url)

            login_success = self.try_login(username,password, 'un', 'pwd', 'vcd')

            if not login_success:
                raise UserLoginFailedException(username, 'Invalid username')

            time.sleep(5)
            cookies = self.driver.get_cookies()
            cookiejar = RequestsCookieJar()

            for cookie in cookies:
                cookiejar.set(cookie['name'], cookie['value'])

            r = requests.get(self.yhd_user_cid_url, cookies=cookiejar)
            rt = r.content.replace("cid(", '').replace(")", '')
            jsonobj = json.loads(rt, strict=True)
            cid= jsonobj['cid']
            usn = jsonobj['userName']
            uid = jsonobj['userId']

            u = UserInfo(username, uid, cid, cookiejar)

            return u
        except Exception, e:
            logger.error(e.message, e)
        finally:
            self.take_screenshot('%s.png' % username)
            # self.driver.quit()

    def verify_merchant(self, merchantId, cid, cookiejar):
        """
        Verify this :merchantId can be send message
        if msg return '无可服务客服', means this merchant could not sent message
        :param merchantId:
        :param cid:
        :param cookiejar:
        :return:
        """
        passed = True
        if merchantId and cid and cookiejar:
            r = requests.get(self.yhd_check_merchant_url.format(merchantId=merchantId, cid=cid), cookies=cookiejar)
            ret_data = r.content
            ret_data_str = re.findall(r'.*\((.+?)\)',ret_data)[0]
            json_data = json.loads(ret_data_str, strict=True)

            if json_data and str(json_data['errorCode']) not in ('0'):
                error_code = json_data['errorCode']
                error_msg = json_data['desc']
                print "Merchant[%s] - %s" % (merchantId, error_msg)
                if error_msg and str(error_msg).__contains__('无可服务客服'):
                    passed = False
                    logger.error('MerchantId: %s, %s', merchantId, error_msg)
                    raise MerChantException(merchantId, '%s:%s' % (error_code, error_msg))
        return passed

    def send_msg(self, merchantId, cid, cookiejar, require_verify=True):
        verify_passed = True
        if require_verify:
            verify_passed = self.verify_merchant(merchantId,cid, cookiejar)

        if verify_passed:
            url = self.yhd_chat_url.format(merchantId=merchantId)

            ##########   define the script that no alert, confirm and onbeforeunload pop up box [START]#####
            self.driver.execute_script("window.alert = function(){}")
            self.driver.execute_script("window.confirm = function(){return true;}")
            self.driver.execute_script("window.onbeforeunload=null")
            ##########   define the script that no alert, confirm and onbeforeunload pop up box [E D]#######

            self.driver.get(url)
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'richEditor')))
            time.sleep(5)

            ele = self.driver.find_element_by_id('richEditor')
            if ele:
                ele.click()
                # say hi firstly
                if config.SAY_HI_BEFORE_MESSAGE:
                    ele.send_keys("Hi....")
                    time.sleep(2)
                    ele.send_keys(Keys.ENTER)
                    time.sleep(2)

                ele.send_keys(unicode(self.adv_message).decode('utf-8'))
                time.sleep(2)
                ele.send_keys(Keys.ENTER)
                time.sleep(3)
                logger.info("sent adv msg to [%s] successfully!", merchantId)
                self.take_screenshot('message_sent_%s.png' % merchantId)

        # if merchantId and cid and cookiejar:
        #     r = requests.get(self.yhd_check_merchant_url.format(merchantId=merchantId, cid=cid), cookies=cookiejar)
        #     ret_data = r.content
        #     ret_data_str = re.findall(r'.*\((.+?)\)',ret_data)[0]
        #     json_data = json.loads(ret_data_str, strict=True)
        #
        #     if json_data:
        #         error_code = json_data['errorCode']
        #         error_msg = json_data['desc']
        #         print "Merchant[%s] - %s" % merchantId, error_msg
        #         if error_msg and str(error_msg).__contains__('无可服务客服'):
        #             logger.error('MerchantId: %s, %s', merchantId, error_msg)
        #             raise MerChantException(merchantId, '%s:%s' % (error_code, error_msg))
        #
        #
        #     # if json_data and json_data['errorCode'] != 0:
        #     #     error_msg = json_data['desc']
        #     #     print error_msg
        #     #     logger.error('MerchantId: %s, %s', merchantId, error_msg)
        #     #     raise MerChantException(merchantId, error_msg)
        #
        #     else:
        #


    def get_sent_merchants(self):
        return Utils.get_file_contents(self.sent_merchant_txt_file_name)

    def get_crawled_merchants(self):
        return Utils.get_file_contents(Utils.get_today_crawled_file_name())

    def get_failed_sent_merchants(self):
        return Utils.get_file_contents(self.failed_sent_merchant_txt_file_name)

    def run(self, username, password):
        try:
            userInfo = self.login(username, password)
            if not userInfo:
                error_msg = 'User Login Failed, please view the screenshot: %s' % os.path.join(config.get_output_dir(), '%s.png' % username)
                logger.error(error_msg)
                raise UserLoginFailedException(username, error_msg)

            user_cid = userInfo.cid
            user_cookie = userInfo.cookiesjar
            send_msg_processor_sleep_time = 0 # 记录 等待了多少次， 最多只等待三次
            failed_send_set = set()
            idx = 0

            while True:
                all_merchants = self.get_crawled_merchants()
                sent_merchants = self.get_sent_merchants()
                # failed_send_merchants = self.get_failed_sent_merchants()
                crawled_merchants_set = set(all_merchants if all_merchants else [])
                sent_merchants_set = set(sent_merchants if sent_merchants else [])
                # failed_send_merchants_set = set(failed_send_merchants if failed_send_merchants else [])
                not_sent_merchants= crawled_merchants_set - sent_merchants_set

                not_sent_size = len(not_sent_merchants)

                if not_sent_size > 0:
                    for merchantId in not_sent_merchants:
                        try:
                            idx = idx + 1
                            logger.info("Send message to [%s] of [%s/%s]", merchantId, idx, not_sent_size)
                            self.send_msg(merchantId, user_cid, user_cookie)
                            self.save_success_send_file(merchantId)
                        except Exception, e:
                            print e
                            self.take_screenshot('failed_%s.png' % merchantId)
                            logger.error("Failed send message to merchant: %s ", merchantId)
                            if merchantId not in failed_send_set:
                                failed_send_set.add(merchantId)
                                self.save_failed_send_file(merchantId)

                            if idx > len(crawled_merchants_set) * 2:
                                break

                else:
                    if send_msg_processor_sleep_time > 3:
                        logger.warn("Quite this program, no newest merchant found. >>>>Bye Bye.>>>>")
                        break
                    send_msg_processor_sleep_time = send_msg_processor_sleep_time + 1
                    time.sleep(20) # sleep 20 secs

        finally:
            self.driver.quit()

    def run_batch(self, username, password, merchants):
        try:
            userInfo = self.login(username, password)
            if not userInfo:
                error_msg = 'User Login Failed, please view the screenshot: %s' % os.path.join(config.get_output_dir(), '%s.png' % username)
                logger.error(error_msg)
                raise UserLoginFailedException(username, error_msg)

            user_cid = userInfo.cid
            user_cookie = userInfo.cookiesjar
            idx = 0

            sent_merchants_set = set(self.get_sent_merchants() if self.get_sent_merchants() else [])

            for merchantId in merchants:
                if merchantId not in sent_merchants_set:
                    try:
                        idx = idx + 1
                        logger.info("Send message to %s [%s/%s]", merchantId, idx, len(merchants))
                        self.send_msg(merchantId, user_cid, user_cookie)
                        self.save_success_send_file(merchantId)
                    except Exception, e:
                        logger.error(e)
        finally:
            self.driver.quit()