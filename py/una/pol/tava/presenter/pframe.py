'''
Created on 04/08/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub


class FramePresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.OnNewProjectBarPub, 'BAR.PROJECT.NEW')

    def OnNewProjectBarPub(self, message):
        self.iview.OnBarNewProject()
