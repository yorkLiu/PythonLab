# -*- coding: utf-8 -*-
# coding:utf-8

class UserInfo:

    def __init__(self, username, userId, cid, cookiesjar):
        self._username = username
        self._userId = userId
        self._cid = cid
        self._cookiesjar = cookiesjar


    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def userId(self):
        return self._userId

    @userId.setter
    def userId(self, value):
        self._userId = value

    @property
    def cid(self):
        return self._cid

    @cid.setter
    def cid(self, value):
        self._cid = value

    @property
    def cookiesjar(self):
        return self._cookiesjar

    @cookiesjar.setter
    def cookiesjar(self, cookieJar):
        self._cookiesjar = cookieJar