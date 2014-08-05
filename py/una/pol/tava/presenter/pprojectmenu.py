'''
Created on 29/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
import topic as t


class ProjectMenuPresenter:
    def __init__(self, iview):
        self.iview = iview

    def OnOpen(self, project, item):
        pub.sendMessage(t.PROJECT_OPEN, (project, item))

    def OnClose(self, project, item):
        pub.sendMessage(t.PROJECT_CLOSE, (project, item))

    def OnDelete(self, project, item):
        pub.sendMessage(t.PROJECT_DELETE, (project, item))

    def OnRename(self, project, item):
        pub.sendMessage(t.PROJECT_RENAME, (project, item))
