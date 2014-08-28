'''
Created on 29/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
import topic as T


class ProjectMenuPresenter:
    def __init__(self, iview):
        self.iview = iview

    def AddFileInProject(self, project):
        pub.sendMessage('PROJECT.ADDFILE', project)

    def OpenProject(self):
        pub.sendMessage(T.PROJECT_OPEN)

    def CloseProject(self):
        pub.sendMessage(T.PROJECT_CLOSE)

    def DeleteProject(self):
        pub.sendMessage(T.PROJECT_DELETE_CLICK)

    def RenameProject(self, project):
        pub.sendMessage(T.PROJECT_RENAME, project)

    def ShowProperties(self):
        pub.sendMessage(T.PROJECT_PROPERTIES)

    def HideProject(self):
        pub.sendMessage('PROJECT.HIDE')
