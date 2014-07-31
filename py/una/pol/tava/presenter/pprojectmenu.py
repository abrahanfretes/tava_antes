'''
Created on 29/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub


class ProjectMenuPresenter:
    def __init__(self, iview):
        self.iview = iview

    def OnOpen(self, project, item):
        pub.sendMessage('PROJECT.OPEN', (project, item))

    def OnClose(self, project, item):
        pub.sendMessage('PROJECT.CLOSED', (project, item))

    def OnDelete(self, project, item):
        pub.sendMessage('PROJECT.DELETE', (project, item))
