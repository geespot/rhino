#coding=utf-8

class APIError(Exception):
    def __init__(self, status=500, data=u'Server Error'):
        self.status = status
        self.data = data