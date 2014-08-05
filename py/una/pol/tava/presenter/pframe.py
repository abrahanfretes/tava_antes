'''
Created on 04/08/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
import topic as t


class FramePresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.OnNewProjectBarPub, t.BAR_PROJECT_NEW)
        pub.subscribe(self.OnRenameProjectPub, t.PROJECT_RENAME)

    def OnNewProjectBarPub(self, message):
        self.iview.OnBarNewProject()

    def OnRenameProjectPub(self, message):
        self.iview.OnRenameProject(message)
