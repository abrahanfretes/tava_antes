'''
Created on 28/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.model.mproject import ProjectModel


class ProjectTreeCtrlPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.OnNew, 'PROJECT.NEW')
        pub.subscribe(self.OnDelete, 'PROJECT.DELETE')

    def OnAddNode(self, project):
        self.iview.AddProjectNode(project)

    def OnNew(self, message):
        project = message.data
        self.OnAddNode(project)

    def OnInitializeTree(self):
        list_project = ProjectModel().getAll()
        self.iview.OnInitializeTree(list_project)

    def GetNamesProjects(self):
        return ProjectModel().getNamesProject()

    def OnDelete(self, message):
        item = message.data
        self.iview.OnDeleteItem(item)
