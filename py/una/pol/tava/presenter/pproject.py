'''
Created on 28/07/2014

@author: afretes
'''
from py.una.pol.tava.model.mproject import ProjectModel as pro
from wx.lib.pubsub import Publisher as pub
import topic as t


class NewProjectDialogPresenter():
    def __init__(self, iview):
        self.iview = iview
        self.listNamesProject = self.GetNamesProject()

    def GetNamesProject(self):
        return pro().getNamesProject()

    def OnNew(self, name):

        project = pro().add(name)
        pub.sendMessage(t.PROJECT_NEW, project)

    def IsNameValido(self, name):
        return name not in self.listNamesProject and bool(name)
