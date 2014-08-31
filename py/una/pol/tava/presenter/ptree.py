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

    #------ funciones encargadas de recepcionar mensajes ----------------------
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
            project = ProjectModel().getProjectForName(name)
            self.AddProjectNode(project)

    #----------------------------------------------------

    #- funciones encargadas de inicializar y actualizar el arbol de proyectos -

    def InitializeTree(self):
        for project in ProjectModel().getAll():
            self.AddProjectNode(project)

    def AddProjectNode(self, project):

        if project.state == OPEN:
            project_item = self.iview.AddProjectOpenNode(project)
            # agregar paquete para arhivos
            package_result_item = self.iview.AddPackageResult(project_item)
            self.AddFileResult(package_result_item, project)

            # agregar paquete para pruebas
            package_analizer_item = self.iview.AddPackageAnalyzer(project_item)
            print self.iview.GetItemText(package_analizer_item)

        else:
            project_item = self.iview.AddProjectCloseNode(project)

    def AddFileResult(self, package_item, project):
        for result in ResultModel().getResultsByProject(project):
            self.iview.AddResultAProject(package_item, result)

    def UpdateProjectTree(self, project):
        self.DeleteProjectItem()
        self.AddProjectNode(project)

    def DeleteProjectItem(self):
        self.iview.DeleteProjectItem(self.iview.GetSelection())

    #----------------------------------------------------

    #------ funciones encargadas de verificar el tipo de item seleccionado ----

    def GetTypeSelectedItem(self):
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

    #----------------------------------------------------

    #------ funciones auxiliares desde la vista -------------------------------
    def GetProjectSelected(self):
        item_selected = self.iview.GetSelection()
        return self.iview.GetItemPyData(item_selected)
    #----------------------------------------------------
