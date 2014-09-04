'''
Created on 29/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.base.entity import OPEN, CLOSED
import topic as T


class ProjectMenuPresenter:
    def __init__(self, iview):
        self.iview = iview

    def AddFileInProject(self, project):
        pub.sendMessage(T.PROJECT_ADDFILE, project)

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
        pub.sendMessage(T.PROJECT_HIDE)

    def InitialEnableItem(self):
        # Si el estado del proyecto es Abierto, se desabilitan las sgtes
        # opciones
        if self.iview.project.state == OPEN:
            self.iview.open_item.Enable(False)
            self.iview.hide_item.Enable(False)

        # Si el estado del proyecto es Cerrado, se desabilitan las sgtes
        # opciones
        if self.iview.project.state == CLOSED:
            self.iview.closed_item.Enable(False)
            self.iview.rename_item.Enable(False)
            self.iview.properties_item.Enable(False)


class ResultPackageMenuPresenter:
    def __init__(self, iview):
        self.iview = iview

    def AddFileInProject(self, project):
        pub.sendMessage(T.PROJECT_ADDFILE, project)
