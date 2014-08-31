'''
Created on 28/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.model.mproject import ProjectModel
from py.una.pol.tava.model.mresult import ResultModel
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
        pub.subscribe(self.HideProjectPub, T.PROJECT_HIDE)
        pub.subscribe(self.UnHideProjectPub, T.PROJECT_LISTRESTORE)

    def NewProjectPub(self, message):
        project = message.data
        self.AddProjectNode(project)

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
            self.AddProjectNode(project)

    def UpdateProjectTree(self, project):
        self.DeleteProjectItem()
        self.AddProjectNode(project)

    def UpDateOpenForHideProject(self, name_project):
        project = ProjectModel().getProjectForName(name_project)
        project.state = OPEN
        return ProjectModel().upDate(project)

    def AddProjectNode(self, project):

        if project.state == OPEN:
            project_item = self.iview.AddProjectOpenNode(project)
            # agregar paquete de arhivos
            package_result_item = self.iview.AddPackageResult(project_item)
            self.AddFileResult(package_result_item, project)

            # agregar paquete para test
            package_analizer_item = self.iview.AddPackageAnalyzer(project_item)
            print self.iview.GetItemText(package_analizer_item)

        else:
            project_item = self.iview.AddProjectCloseNode(project)
            #self.AddFileResult(project_item)

    def AddFileResult(self, package_item, project):
        #project = self.iview.GetItemPyData(item)
        for result in ResultModel().getResultsByProject(project):
            self.iview.AddResultAProject(package_item, result)

    def DeleteProjectItem(self):
        self.iview.DeleteProjectItem(self.iview.GetSelection())

    def InitializeTree(self):
        for project in ProjectModel().getAll():
            self.AddProjectNode(project)
            #self.iview.AddProjectNode(project)

    def SelectedItem(self):
        item = self.iview.GetSelection()

        if self.iview.GetItemPyData(item) is not None:
            parent_item = self.iview.GetItemParent(item)

            if(parent_item == self.iview.root):
                #verificar luego si esta correcto
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
