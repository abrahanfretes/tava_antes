'''
Created on 29/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
import topic as t


class ProjectMenuPresenter:
    def __init__(self, iview):
        self.iview = iview

    def OnOpen(self):
        pub.sendMessage(t.PROJECT_OPEN)

    def OnClose(self):
        pub.sendMessage(t.PROJECT_CLOSE)

    def OnDelete(self):
        pub.sendMessage(t.PROJECT_DELETE_CLICK)

    def OnRename(self, project):
        pub.sendMessage(t.PROJECT_RENAME, project)
