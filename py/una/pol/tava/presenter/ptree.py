'''
Created on 28/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.model.mproject import ProjectModel
from py.una.pol.tava.base.entity import OPEN, CLOSED, HIDDEN
import topic as T


class ProjectTreeCtrlPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.NewProjectPub, T.PROJECT_NEW)
        pub.subscribe(self.DeleteSelectProjectPub, T.PROJECT_DELETE_CLICK)
        pub.subscribe(self.DeleteProjectPub, T.PROJECT_DELETE_OK)
        pub.subscribe(self.CloseProjectPub, T.PROJECT_CLOSE)
        pub.subscribe(self.OpenProjectPub, T.PROJECT_OPEN)
        pub.subscribe(self.RenameProjectPub, T.PROJECT_RENAME_UP)
        pub.subscribe(self.HideProjectPub, 'PROJECT.HIDE')
        pub.subscribe(self.UnHideProjectPub, 'PROJECT.LISTRESTORE')

    def NewProjectPub(self, message):
        project = message.data
        self.AddNode(project)

    def DeleteSelectProjectPub(self, message):
        pub.sendMessage(T.PROJECT_DELETE_SELECT)

    def DeleteProjectPub(self, message):
        project = self.GetProjectSelected()
        ProjectModel().delete(project)
        self.DeleteProjectItem()

    def CloseProjectPub(self, message):
        project = self.GetProjectSelected()
        project.state = CLOSED
        project = ProjectModel().upDate(project)
        self.UpdateProjectTree(project)

    def OpenProjectPub(self, message):
        project = self.GetProjectSelected()
        project.state = OPEN
        project = ProjectModel().upDate(project)
        self.UpdateProjectTree(project)

    def RenameProjectPub(self, message):
        project = message.data
        self.UpdateProjectTree(project)

    def HideProjectPub(self, message):
        project = self.GetProjectSelected()
        project.state = HIDDEN
        project = ProjectModel().upDate(project)
        self.DeleteProjectItem()

    def UnHideProjectPub(self, message):
        list_names = message.data
        for name in list_names:
            project = self.UpDateOpenForHideProject(name)
            self.AddNode(project)

    def UpdateProjectTree(self, project):
        self.DeleteProjectItem()
        self.AddNode(project)

    def UpDateOpenForHideProject(self, name_project):
        project = ProjectModel().getProjectForName(name_project)
        project.state = OPEN
        return ProjectModel().upDate(project)

    def AddNode(self, project):
        self.iview.AddProjectNode(project)

    def DeleteProjectItem(self):
        self.iview.DeleteProjectItem(self.iview.GetSelection())

    def InitializeTree(self):
        list_project = ProjectModel().getAll()
        self.iview.LoadProjectsInTree(list_project)

    def SendSelectedProject(self):
        pub.sendMessage(T.PROJECT_SELECTED, self.GetProjectSelected())
        if self.GetProjectSelected().state == OPEN:
            pub.sendMessage(T.PROJECT_SELECTED_OPEN)
        else:
            pub.sendMessage(T.PROJECT_SELECTED_CLOSE)

    def GetNamesProjects(self):
        return ProjectModel().getNamesProject()

    def GetProjectSelected(self):
        item_selected = self.iview.GetSelection()
        return self.iview.GetItemPyData(item_selected)
