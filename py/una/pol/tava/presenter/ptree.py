# -*- encoding: utf-8 -*-
'''
Created on 28/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.model.mproject import ProjectModel
from py.una.pol.tava.model.mresult import ResultModel
from py.una.pol.tava.model.mtestconfig import TestConfigModel
from py.una.pol.tava.base.entity import OPEN, CLOSED, Project
from py.una.pol.tava.base.entity import Result, TestConfig
import topic as T


class ProjectTreeCtrlPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.NewProjectPub, T.PROJECT_NEW)
        pub.subscribe(self.UdDateProjectPub, T.PROJECT_UPDATE)
        pub.subscribe(self.DeleteProjectPub, T.PROJECT_DELETE_OK)
        pub.subscribe(self.DeleteSelectProjectPub, T.PROJECT_DELETE_CLICK)
        pub.subscribe(self.UpDateStateProjectPub, T.PROJECT_STATE_UPDATE)
        pub.subscribe(self.UnHideProjectPub, T.PROJECT_LISTRESTORE)
        pub.subscribe(self.AddFilePub, T.ADDEDFILE_PROJECT)

    #------ funciones encargadas de recepcionar mensajes ----------------------
    def NewProjectPub(self, message):
        project = message.data
        self.NewProjectItem(project)

    def UdDateProjectPub(self, message):
        project = message.data
        self.UdDateItemProject(project)

    def DeleteProjectPub(self, message):
        self.DeleteProject()

    def DeleteSelectProjectPub(self, message):
        pub.sendMessage(T.PROJECT_DELETE_SELECT)

    def UpDateStateProjectPub(self, message):
        state = message.data
        project = self.getItemDate()
        project.state = state
        self.UpdateProjectData(project)
        self.UdDateItemProject(project)

    def UnHideProjectPub(self, message):
        list_names = message.data
        for name in list_names:
            project = self.GetProjectByName(name)
            self.NewProjectItem(project)

    def AddFilePub(self, message):
        project = message.data
        self.UdDateItemProject(project)
    #----------------------------------------------------

    #-----------  NewProjectItem ----------------------------------------
    def NewProjectItem(self, project):
        '''
        Función que agrega un item proyecto al arbol.
        Clasifica a los proyectos para su insercion; si esta en un estado OPEN,
        agrega sus correspondientes item Result e item TestConfig, en caso
        contrario, solo agrega el item proyecto.

        :project: Project, representa el proyecto a ser agregado al arbol.
        '''
        if project.state == OPEN:
            pitem = self.AddProjectOpenNodeItem(project)
            pr_item = self.AddItemPackageResult(pitem)
            pt_item = self.AddPackageAnalyzerItem(pitem)

            self.AddItemsFileResult(pr_item, project)
            self.sortTree(pr_item)

            self.AddItemsTestConfig(pt_item, project)
            self.sortTree(pr_item)

        elif project.state == CLOSED:
            self.AddProjectCloseNodeItem(project)

        self.sortTree(self.iview.root)

    def AddProjectOpenNodeItem(self, project):
        return self.iview.AddProjectOpenNode(project)

    def AddItemPackageResult(self, project_item):
        return self.iview.AddPackageResult(project_item)

    def AddItemsFileResult(self, package_item, project):
        for result in ResultModel().getResultsByProject(project):
            self.iview.AddResultToProject(package_item, result)

    def AddPackageAnalyzerItem(self, project_item):
        return self.iview.AddPackageResult(project_item)

    def AddItemsTestConfig(self, package_test, project):
        for test in TestConfigModel().getTestConfigByProject(project):
            self.iview.AddTestToProject(package_test, test)

    def sortTree(self, item):
        self.iview.SortChildren(item)

    def AddProjectCloseNodeItem(self, project):
        return self.iview.AddProjectCloseNode(project)
    #---------------------------------------------------

    #----------  DeleteProjectItem  -------------------------------------
    def DeleteProjectItem(self):
        '''
        Función que elimina un item proyecto del arbol.
        Elimina el item proyecto selecionado o si la seleccion afecta a algun
        item hijo.
        '''
        item_project = self.GetItemPorjectSelected()
        self.iview.Delete(item_project)
    #---------------------------------------------------

    #----------  UdDateItemProject  -------------------------------------
    def UdDateItemProject(self, project):
        '''
        Función que actualiza un item proyecto del arbol.
        Elimina el item del proyecto que se encuentra en el arbol y agrega uno
        nuevo con los atributos actualizados pasado como parametro.

        :project: Project, representa el proyecto actualizado a ser agregado al
        arbol.
        '''
        self.DeleteProjectItem()
        self.NewProjectItem(project)
    #---------------------------------------------------

    #----------  InitializeTree  -------------------------------------
    def InitializeTree(self):
        for project in ProjectModel().getAll():
            self.NewProjectItem(project)
    #---------------------------------------------------

    #------------- GetItemPorjectSelected  ------------------------------------
    def GetItemPorjectSelected(self):
        '''
        Funcion para obtener el item del projecto a partir del item
        seleccionado, los item selccionados pueden ser, Projecto, Resultado,
        TestConfig, PackageResult, PackageAnlizae. En todos los casos retorna
        el item del projecto a ser actualizado.
        '''
        item, data = self.getItemEndDataSelected()

        if isinstance(data, Project):
            return item

        if isinstance(data, Result):
            return self.GetGrandFather(item)

        if isinstance(data, TestConfig):
            return self.GetGrandFather(item)

        if(self.IsPackageResult(item)):
            return self.iview.GetItemParent(item)

        if(self.IsPackageAnalyzer(item)):
            return self.iview.GetItemParent(item)

    def IsPackageResult(self, item):
        toRet = (self.iview.GetItemText(item) == 'Resultados')
        return toRet

    def IsPackageAnalyzer(self, item):
        toRet = (self.iview.GetItemText(item) == 'Pruebas')
        return toRet

    def GetGrandFather(self, item):
        father = self.iview.GetItemParent(item)
        return self.iview.GetItemParent(father)
    #--------------------------------------------------------------------------

    #------------ GetTypeSelectedItem -----------------------------------------
    def GetTypeSelectedItem(self):

        item, data = self.getItemEndDataSelected()
        item_parent = self.iview.GetItemParent(item)
        if item_parent is not None:
            item_parent_py_data = self.iview.GetItemPyData(item_parent)

            if isinstance(item_parent_py_data, Project):
                pub.sendMessage(T.PROJECT_SELECTED, item_parent_py_data)

        if data is not None:
            parent_item = self.iview.GetItemParent(item)
            if(parent_item == self.iview.root):
                #verificar luego si esta correcto
                pub.sendMessage(T.PROJECT_SELECTED, self.GetProjectSelected())

                if self.GetProjectSelected().state == OPEN:
                    pub.sendMessage(T.PROJECT_SELECTED_OPEN)
                else:
                    pub.sendMessage(T.PROJECT_SELECTED_CLOSE)

    #--------------------------------------------------------------------------

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
