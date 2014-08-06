'''
Created on 29/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
import topic as t


class ToolBarPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.OnDisableOpenPub, t.PROJECT_SELECTED_OPEN)
        pub.subscribe(self.OnDisableClosePub, t.PROJECT_SELECTED_CLOSE)

        pub.subscribe(self.OnDisableIcomProjectAllPub, t.PROJECT_CLOSE)
        pub.subscribe(self.OnDisableIcomProjectAllPub, t.PROJECT_OPEN)

    def OnDisableIcomProjectAll(self):
        self.iview.OnAllDisable()

    def OnCloseProjectSend(self):
        pub.sendMessage(t.PROJECT_CLOSE)

    def OnNewProject(self):
        pub.sendMessage(t.BAR_PROJECT_NEW)

    def OnOpenProject(self):
        pub.sendMessage(t.PROJECT_OPEN)

    def OnDeleteProject(self):
        pub.sendMessage(t.PROJECT_DELETE_CLICK)

    def OnDisableOpenPub(self, message):
        self.iview.OnOpenDisable()

    def OnDisableClosePub(self, message):
        self.iview.OnCloseDisable()

    def OnDisableIcomProjectAllPub(self, message):
        self.OnDisableIcomProjectAll()
