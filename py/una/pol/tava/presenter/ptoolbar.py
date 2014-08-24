'''
Created on 29/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
import topic as T


class ToolBarPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.EnableDisableOpenProjectPub,
                      T.PROJECT_SELECTED_OPEN)
        pub.subscribe(self.EnableDisableCloseProjectPub,
                      T.PROJECT_SELECTED_CLOSE)
        pub.subscribe(self.DisableAllProjectPub, T.PROJECT_CLOSE)
        pub.subscribe(self.DisableAllProjectPub, T.PROJECT_OPEN)
        pub.subscribe(self.DisableAllProjectPub, T.PROJECT_DELETE_OK)
        pub.subscribe(self.DisableAllProjectPub, 'PROJECT.HIDE')
        pub.subscribe(self.UpdateLabelsPub, T.LANGUAGE_CHANGED)

    def DisableAllProject(self):
        self.iview.DisableAllProject()

    def CloseProject(self):
        pub.sendMessage(T.PROJECT_CLOSE)

    def NewProject(self):
        pub.sendMessage(T.BAR_PROJECT_NEW)

    def OpenProject(self):
        pub.sendMessage(T.PROJECT_OPEN)

    def DeleteProject(self):
        pub.sendMessage(T.PROJECT_DELETE_CLICK)

    def OnHideProject(self):
        pub.sendMessage('PROJECT.HIDE')

    def UnHideProject(self):
        pub.sendMessage('PROJECT.UNHIDE')

    def EnableDisableOpenProjectPub(self, message):
        self.iview.EnableDisableOpenProject()

    def EnableDisableCloseProjectPub(self, message):
        self.iview.EnableDisableCloseProject()

    def DisableAllProjectPub(self, message):
        self.DisableAllProject()

    def UpdateLabelsPub(self, message):
        self.iview.SetLabels()
