'''
Created on 28/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.model.mproject import ProjectModel
from py.una.pol.tava.base.entity import CLOSED
from py.una.pol.tava.base.entity import OPEN
import topic as t


class ProjectTreeCtrlPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.OnNewPub, t.PROJECT_NEW)
        pub.subscribe(self.OnDeletePub, t.PROJECT_DELETE)
        pub.subscribe(self.OnClosedPub, t.PROJECT_CLOSE)
        pub.subscribe(self.OnOpenPub, t.PROJECT_OPEN)

    def OnAddNode(self, project):
        self.iview.AddProjectNode(project)

    def OnDelete(self, item):
        self.iview.OnDeleteItem(item)

    def OnInitializeTree(self):
        list_project = ProjectModel().getAll()
        self.iview.OnInitializeTree(list_project)

    def OnSelectedProject(self, project, item):
        pub.sendMessage(t.PROJECT_SELECTED, (project, item))

    def GetNamesProjects(self):
        return ProjectModel().getNamesProject()

    def OnUpDateTree(self, project, item):
        self.OnDelete(item)
        self.OnAddNode(project)

    def OnClose(self, project, item):
        project.state = CLOSED
        project = ProjectModel().upDate(project)

        self.OnUpDateTree(project, item)

    def OnOpen(self, project, item):
        project.state = OPEN
        project = ProjectModel().upDate(project)

        self.OnUpDateTree(project, item)

    def OnNewPub(self, message):
        project = message.data
        self.OnAddNode(project)

    def OnDeletePub(self, message):
        project_item = message.data
        project = project_item[0]
        item = project_item[1]

        ProjectModel().delete(project)
        self.OnDelete(item)

    def OnClosedPub(self, message):
        project_item = message.data
        project = project_item[0]
        item = project_item[1]

        self.OnClose(project, item)

    def OnOpenPub(self, message):
        project_item = message.data
        project = project_item[0]
        item = project_item[1]

        self.OnOpen(project, item)
