'''
Created on 28/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.model.mproject import ProjectModel
from py.una.pol.tava.model.mresult import ResultModel
from py.una.pol.tava.base.entity import OPEN, HIDDEN
import topic as T


class ProjectTreeCtrlPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.NewProjectPub, T.PROJECT_NEW)
        pub.subscribe(self.DeleteProjectPub, T.PROJECT_DELETE_OK)
        pub.subscribe(self.DeleteSelectProjectPub, T.PROJECT_DELETE_CLICK)
        pub.subscribe(self.UpDateStateProjectPub, T.PROJECT_STATE_UPDATE)
        pub.subscribe(self.RenameProjectPub, T.PROJECT_RENAME_UP)
        pub.subscribe(self.UnHideProjectPub, T.PROJECT_LISTRESTORE)
        pub.subscribe(self.AddFilePub, T.ADDEDFILE_PROJECT)

    #------ funciones encargadas de recepcionar mensajes ----------------------
    def NewProjectPub(self, message):
        self.NewProject(message.data)

    def DeleteProjectPub(self, message):
        self.DeleteProject()

    def DeleteSelectProjectPub(self, message):
        pub.sendMessage(T.PROJECT_DELETE_SELECT)

    def UpDateStateProjectPub(self, message):
        state = message.data
        item, project = self.getItemEndDataSelected()
        project.state = state
        if state == HIDDEN:
            self.UpdateProjectData(project)
            self.DeleteProjectItem(item)
        else:
            self.UpDateProject(project, item)

    def UnHideProjectPub(self, message):
        list_names = message.data
        for name in list_names:
            project = self.GetProjectByName(name)
            self.NewProject(project)

    def RenameProjectPub(self, message):
        project = message.data
        self.UpDateFromtProjectItem(project)

    def AddFilePub(self, message):
        project = message.data
        self.UpDateFromtProjectItem(project)
    #----------------------------------------------------

    #--------- Funciones generales (abm, model and view) ----------------------

    def NewProject(self, project):
        self.NewProjectItem(project)

    def DeleteProject(self):
        item, project = self.getItemEndDataSelected()
        self.DeleteProjectData(project)
        self.DeleteProjectItem(item)

    def UpDateProject(self, project, item):
        self.UpdateProjectData(project)
        self.UpdateProjectItem(project, item)

    def UpDateFromtProjectItem(self, project):
        item = self.getItemSelected()
        self.UpdateProjectItem(project, item)

    def InitializeTree(self):
        for project in ProjectModel().getAll():
            self.NewProjectItem(project)
    #----------------------------------------------------

    #- funciones encargadas del arbol de proyectos ----------------------------
    #----- abm of view -------------------------------------------------
    def NewProjectItem(self, project):
        if project.state == OPEN:
            pitem = self.AddProjectOpenNodeItem(project)
            pr_item = self.AddPackageResultItem(pitem)
            self.NewFileResultItem(pr_item, project)
            self.sortTree(pr_item)
            self.AddPackageAnalyzerItem(pitem)
        else:
            self.AddProjectCloseNodeItem(project)
        self.sortTree(self.iview.root)

    def DeleteProjectItem(self, item):
        self.iview.Delete(item)

    def UpdateProjectItem(self, project, item):
        self.DeleteProjectItem(item)
        self.NewProjectItem(project)

    def NewFileResultItem(self, package_item, project):
        for result in ResultModel().getResultsByProject(project):
            self.AddFileResultItemInProject(package_item, result)
    #----------------------------------------------------------

    #---- funciones auxiliares enlazados a la vista(view)---------------
    def AddProjectOpenNodeItem(self, project):
        return self.iview.AddProjectOpenNode(project)

    def AddProjectCloseNodeItem(self, project):
        return self.iview.AddProjectCloseNode(project)

    def AddPackageResultItem(self, project_item):
        return self.iview.AddPackageResult(project_item)

    def AddPackageAnalyzerItem(self, project_item):
        return self.iview.AddPackageAnalyzer(project_item)

    def sortTree(self, item):
        self.iview.SortChildren(item)

    def AddFileResultItemInProject(self, package_item, result):
        self.iview.AddResultAProject(package_item, result)
    #------------------------------------------------------------

    #------ funciones encargadas de verificar el tipo de item seleccionado ----

    def GetTypeSelectedItem(self):
        item, data = self.getItemEndDataSelected()
        if data is not None:
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

    def GetPackageResultSelected(self):
        item_selected = self.iview.GetSelection()
        parent_item = self.iview.GetItemParent(item_selected)

        #si la seleccion es un proyecto
        if parent_item == self.iview.root:
            for item in item_selected.GetChildren():
                if self.iview.GetItemText(item) == 'Resultados':
                    return item
        #si la seleccion es un paquete resultado
        return item_selected

    def ContexMenu(self):

        item = self.iview.GetSelection()
        parent_item = self.iview.GetItemParent(item)

        #seleccion de un proyecto
        if(parent_item == self.iview.root):
            project = self.iview.GetItemPyData(item)
            self.iview.InitializeProjectMenu(project)

        #seleccion de un paquete resultado
        elif self.iview.GetItemText(item) == 'Resultados':
            project = self.iview.GetItemPyData(parent_item)
            self.iview.InitializeResultPackageMenu(project)

        #seleccion de un paquete analisis
        elif self.iview.GetItemText(item) == 'Pruebas':
            project = self.iview.GetItemPyData(parent_item)
            self.iview.InitializeAnalysisPackageMenu(project)

        #seleccion de un archivo resultado
        elif self.iview.GetItemText(parent_item) == 'Resultados':
            self.iview.InitializeResultMenu(item)

        #seleccion de un analisis
        elif self.iview.GetItemText(parent_item) == 'Pruebas':
            self.iview.InitializeAnalysisMenu(project)

    def getItemSelected(self):
        return self.iview.GetSelection()

    def getItemDate(self, item):
        return self.iview.GetItemPyData(item)

    def getItemEndDataSelected(self):
        item = self.iview.GetSelection()
        data = self.iview.GetItemPyData(item)
        return item, data
    #----------------------------------------------------

    #- funciones encargadas del abm de datos de proyectos(model)----------
    #----- abm of data-------------------------------------------------
    def DeleteProjectData(self, project):
        ProjectModel().delete(project)

    def UpdateProjectData(self, project):
        return ProjectModel().upDate(project)

    def GetProjectByName(self, name):
        return ProjectModel().getProjectForName(name)
    #----------------------------------------------------------
