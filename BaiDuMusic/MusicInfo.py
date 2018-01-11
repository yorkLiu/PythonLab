# -*- coding: UTF-8 -*-

class MusicInfo(object):

    def __init__(self, song_id, song_author, song_title, song_info):
        self.song_id=song_id
        self.song_author=song_author
        self.song_title=song_title
        self.song_info=song_info

    @staticmethod
    def getItemIndex():
        return [' ','song_id', 'song_title','song_author','song_info']
