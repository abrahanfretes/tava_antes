'''
Created on 28/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.model.mproject import ProjectModel
from py.una.pol.tava.base.entity import OPEN, CLOSED, HIDDEN
import topic as t


class ProjectTreeCtrlPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.OnNewPub, t.PROJECT_NEW)

        pub.subscribe(self.OnDeleteClickPub, t.PROJECT_DELETE_CLICK)
        pub.subscribe(self.OnDeletedOkPub, t.PROJECT_DELETE_OK)

        pub.subscribe(self.OnClosedPub, t.PROJECT_CLOSE)
        pub.subscribe(self.OnOpenPub, t.PROJECT_OPEN)
        pub.subscribe(self.OnRenameUpPub, t.PROJECT_RENAME_UP)
        pub.subscribe(self.OnHidePub, 'PROJECT.HIDE')
        pub.subscribe(self.OnUnHidePub, 'PROJECT.LISTRESTORE')

    def OnUnHidePub(self, message):
        list_names = message.data
        for name in list_names:
            project = self.UpDateOpenForHideProject(name)
            self.OnAddNode(project)

    def UpDateOpenForHideProject(self, name_project):
        project = ProjectModel().getProjectForName(name_project)
        project.state = OPEN
        return ProjectModel().upDate(project)

    def OnAddNode(self, project):
        self.iview.AddProjectNode(project)

    def OnDelete(self):
        self.iview.OnDeleteItem(self.iview.GetSelection())

    def OnInitializeTree(self):
        list_project = ProjectModel().getAll()
        self.iview.OnInitializeTree(list_project)

    def OnSelectedProjectSend(self):
        pub.sendMessage(t.PROJECT_SELECTED, self.GetProjectSelected())
        if self.GetProjectSelected().state == OPEN:
            pub.sendMessage(t.PROJECT_SELECTED_OPEN)
        else:
            pub.sendMessage(t.PROJECT_SELECTED_CLOSE)

    def GetNamesProjects(self):
        return ProjectModel().getNamesProject()

    def OnUpDateTree(self, project):
        self.OnDelete()
        self.OnAddNode(project)

    def OnClose(self):
        project = self.GetProjectSelected()
        project.state = CLOSED
        project = ProjectModel().upDate(project)
        self.OnUpDateTree(project)

    def OnOpen(self):
        project = self.GetProjectSelected()
        project.state = OPEN
        project = ProjectModel().upDate(project)
        self.OnUpDateTree(project)

    def OnRenameUpPub(self, message):
        project = message.data
        self.OnUpDateTree(project)

    def OnNewPub(self, message):
        project = message.data
        self.OnAddNode(project)

    def OnDeleteClickPub(self, message):
        pub.sendMessage(t.PROJECT_DELETE_SELECT, self.GetProjectSelected())

    def OnDeletedOkPub(self, message):
        project = self.GetProjectSelected()
        ProjectModel().delete(project)
        self.OnDelete()

    def OnClosedPub(self, message):
        self.OnClose()

    def OnOpenPub(self, message):
        self.OnOpen()

    def GetProjectSelected(self):
        item_selected = self.iview.GetSelection()
        return self.iview.GetItemPyData(item_selected)

    def OnHidePub(self, message):
        project = self.GetProjectSelected()
        project.state = HIDDEN
        project = ProjectModel().upDate(project)
        self.OnDelete()
