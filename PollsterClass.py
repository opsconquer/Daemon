#coding:utf-8
#
#PollsterClass.py
'''
The base class of pollster
'''
class Pollster(object):
    def __init__(self, name):
        self.name = name

    '''
    Implement this method.
    '''
    def getSample(self):
        pass

