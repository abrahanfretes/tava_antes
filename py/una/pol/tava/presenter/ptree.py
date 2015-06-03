# -*- encoding: utf-8 -*-
'''
Created on 28/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.model.mproject import ProjectModel
from py.una.pol.tava.model.mresult import ResultModel
from py.una.pol.tava.model.mmetric import MetricModel
from py.una.pol.tava.model.mtestconfig import TestConfigModel
from py.una.pol.tava.base.entity import OPEN, CLOSED, Project, MoeaProblem
from py.una.pol.tava.base.entity import Result, TestConfig
import topic as T


class ProjectTreeCtrlPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.NewProjectPub, T.PROJECT_NEW)
        pub.subscribe(self.UdDateProjectPub, T.PROJECT_UPDATE)
        pub.subscribe(self.DeleteProjectPub, T.PROJECT_DELETE)
        pub.subscribe(self.UpDateStateProjectPub, T.PROJECT_STATE_UPDATE)

    # ----- funciones encargadas de recepcionar mensajes ----------------------
    def NewProjectPub(self, message):
        project = message.data
        self.NewProjectItem(project)

    def UdDateProjectPub(self, message):
        project = message.data
        self.UdDateItemProject(project)

    def DeleteProjectPub(self, message):
        project = self.getItemDate()
        self.DeleteProjectData(project)
        self.DeleteProjectItem()

    def UpDateStateProjectPub(self, message):
        state = message.data
        project = self.getItemDate()
        project.state = state
        self.UpdateProjectData(project)
        self.UdDateItemProject(project)
    # ----------------------------------------------------

    # -----------  NewProjectItem ----------------------------------------
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
            # parte gráfica
            tg_item = self.AddTestGraphicNodeItem(pitem)
            tg_pr_item = self.AddItemPackageResult(tg_item)
            tg_pt_item = self.AddPackageAnalyzerItem(tg_item)
            self.AddItemsFileResult(tg_pr_item, project)
            self.AddItemsTestConfig(tg_pt_item, project)
            self.sortTree(tg_pr_item)
            self.sortTree(tg_pt_item)

            # parte métrica
            tm_item = self.AddTestMetricsNodeItem(pitem)
            tm_mr_item = self.AddNodeItemMetricResults(tm_item)
            tm_mv_item = self.AddNodePackageMetricViews(tm_item)
            self.AddItemsFileMetricResult(tm_mr_item, project)
            self.AddItemsTestMetric(tm_mv_item, project)

        elif project.state == CLOSED:
            self.AddProjectCloseNodeItem(project)

        self.sortTree(self.iview.root)

    def AddProjectOpenNodeItem(self, project):
        return self.iview.AddProjectOpenNode(project)

    # agregación de graficas
    def AddTestGraphicNodeItem(self, project_item):
        return self.iview.AddItemTestGraphic(project_item)

    def AddItemPackageResult(self, project_item):
        return self.iview.AddPackageResult(project_item)

    def AddItemsFileResult(self, package_item, project):
        for result in ResultModel().getResultsByProject(project):
            self.iview.AddResultToProject(package_item, result)

    def AddPackageAnalyzerItem(self, project_item):
        return self.iview.AddPackageAnalyzer(project_item)

    def AddItemsTestConfig(self, package_test, project):
        for test in TestConfigModel().getTestConfigByProject(project):
            self.iview.AddTestToProject(package_test, test)

    # agregación de metricas
    def AddTestMetricsNodeItem(self, project_item):
        return self.iview.AddItemTestMetrics(project_item)

    def AddNodeItemMetricResults(self, tm_item):
        return self.iview.AddMetricResults(tm_item)

    def AddNodePackageMetricViews(self, tm_item):
        return self.iview.AddPackageMetricViews(tm_item)

    def AddItemsFileMetricResult(self, package_item, project):
        for result_metric in MetricModel().getResultMetricByProjectId(project.id):
            self.iview.AddResultMetricToProject(package_item, result_metric)

    def AddItemsTestMetric(self, package_test, project):
        pass

    def sortTree(self, item):
        self.iview.SortChildren(item)

    def AddProjectCloseNodeItem(self, project):
        return self.iview.AddProjectCloseNode(project)
    # ---------------------------------------------------

    # ----------  DeleteProjectItem  -------------------------------------
    def DeleteProjectItem(self):
        '''
        Función que elimina un item proyecto del arbol.
        Elimina el item proyecto selecionado o si la seleccion afecta a algun
        item hijo.
        '''
        item_project = self.GetItemPorjectSelected()
        self.iview.Delete(item_project)
    # ---------------------------------------------------

    # ----------  UdDateItemProject  -------------------------------------
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
    # ---------------------------------------------------

    # ----------  InitializeTree  -------------------------------------
    def InitializeTree(self):
        for project in ProjectModel().getAll():
            self.NewProjectItem(project)
    # --------------------------------------------------

    # ------------ GetItemPorjectSelected  ------------------------------------
    def GetItemPorjectSelected(self):
        '''
        Funcion para obtener el item del projecto a partir del item
        seleccionado, los item selccionados pueden ser, Projecto, Resultado,
        TestConfig, PackageResult, PackageAnlizae. En todos los casos retorna
        el item del projecto a ser actualizado.
        '''
        item, data = self.getItemEndDataSelected()

        # proyecto
        if isinstance(data, Project):
            return item

        # paquetes de primer nivel
        if(self.IsPackageGraphic(item)):
            return self.iview.GetItemParent(item)

        if(self.IsPackageMetric(item)):
            return self.iview.GetItemParent(item)

        # paquetes de segundo nivel
        if(self.IsPackageGraphicFiles(item)):
            return self.GetGrandFather(item)

        if(self.IsPackageGraphicTest(item)):
            return self.GetGrandFather(item)

        if(self.IsPackageMetricFile(item)):
            return self.GetGrandFather(item)

        if(self.IsPackageMetricTest(item)):
            return self.GetGrandFather(item)

        # archivos
        if isinstance(data, Result):
            item_aux = self.iview.GetItemParent(item)
            return self.GetGrandFather(item_aux)

        if isinstance(data, TestConfig):
            item_aux = self.iview.GetItemParent(item)
            return self.GetGrandFather(item_aux)

        if isinstance(data, MoeaProblem):
            item_aux = self.iview.GetItemParent(item)
            return self.GetGrandFather(item_aux)

    def IsPackageGraphic(self, item):
        package_graphic = self.iview.getPackageGraphicsName()
        toRet = (self.iview.GetItemText(item) == package_graphic)
        return toRet

    def IsPackageMetric(self, item):
        package_metric = self.iview.getPackageMetricsName()
        toRet = (self.iview.GetItemText(item) == package_metric)
        return toRet

    def IsPackageGraphicFiles(self, item):
        package_file = self.iview.getPackageGraphicsFileName()
        toRet = (self.iview.GetItemText(item) == package_file)
        return toRet

    def IsPackageGraphicTest(self, item):
        package_test = self.iview.getPackageGraphicsTestName()
        toRet = (self.iview.GetItemText(item) == package_test)
        return toRet

    def IsPackageMetricFile(self, item):
        package_file = self.iview.getPackageMetricsFileName()
        toRet = (self.iview.GetItemText(item) == package_file)
        return toRet

    def IsPackageMetricTest(self, item):
        package_test = self.iview.getPackageMetricsTestName()
        toRet = (self.iview.GetItemText(item) == package_test)
        return toRet

    def GetGrandFather(self, item):
        father = self.iview.GetItemParent(item)
        return self.iview.GetItemParent(father)
    # -------------------------------------------------------------------------

    # ----- funciones auxiliares desde la vista -------------------------------

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
                # verificar luego si esta correcto
                pub.sendMessage(T.PROJECT_SELECTED, self.GetProjectSelected())

                if self.GetProjectSelected().state == OPEN:
                    pub.sendMessage(T.PROJECT_SELECTED_OPEN)
                else:
                    pub.sendMessage(T.PROJECT_SELECTED_CLOSE)

    def GetProjectSelected(self):
        item_selected = self.iview.GetSelection()
        return self.iview.GetItemPyData(item_selected)

    def ContexMenu(self):

        item, data = self.getItemEndDataSelected()
        parent_item = self.iview.GetItemParent(item)

        # seleccion de un proyecto
        if(parent_item == self.iview.root):
            self.iview.InitializeProjectMenu(data)

        # seleccion de un paquete Graphics
        elif self.iview.GetItemText(item) == self.iview.getPackageGraphicsName():
            # falta agregar menu para este item
            print 'se selecciono un Graphics'

        # seleccion de un paquete bajo Graphics
        elif self.iview.GetItemText(parent_item) == self.iview.getPackageGraphicsName():

            # seleccion de un paquete Graphics Files
            if self.iview.GetItemText(item) == self.iview.getPackageGraphicsFileName():
                project_item = self.iview.GetItemParent(parent_item)
                project = self.iview.GetItemPyData(project_item)
                self.iview.InitializeResultPackageMenu(project)

            # seleccion de un paquete Graphics Tests
            elif self.iview.GetItemText(item) == self.iview.getPackageGraphicsTestName():
                project_item = self.iview.GetItemParent(parent_item)
                project = self.iview.GetItemPyData(project_item)
                self.iview.InitializeAnalysisPackageMenu(project)

        # seleccion de un paquete Graphics  - Files o Test
        elif self.iview.GetItemText(self.iview.GetItemParent(parent_item)) == self.iview.getPackageGraphicsName():

            # seleccion de un File
            if self.iview.GetItemText(parent_item) == self.iview.getPackageGraphicsFileName():
                self.iview.InitializeResultMenu(item)

            # seleccion de un Test
            elif self.iview.GetItemText(parent_item) == self.iview.getPackageGraphicsTestName():
                self.iview.InitializeAnalysisMenu(data)

        # seleccion de un paquete Metrics
        elif self.iview.GetItemText(item) == self.iview.getPackageMetricsName():
            # falta agregar menu para este item
            print 'se selecciono un Metric'

        # seleccion de un paquete bajo Metrics
        elif self.iview.GetItemText(parent_item) == self.iview.getPackageMetricsName():

            # seleccion de un paquete Metrics Files
            if self.iview.GetItemText(item) == self.iview.getPackageMetricsFileName():
                project_item = self.iview.GetItemParent(parent_item)
                project = self.iview.GetItemPyData(project_item)
                self.iview.InitializeMetricsFilesPackageMenu(project)

            # seleccion de un paquete Metrics Tests
            elif self.iview.GetItemText(item) == self.iview.getPackageMetricsTestName():
                project_item = self.iview.GetItemParent(parent_item)
                project = self.iview.GetItemPyData(project_item)
                print ' menu Metric Package File'
                self.iview.InitializeMetricTestPackageMenu(project)

        # seleccion de un paquete Metrics  - Files o Test
        elif self.iview.GetItemText(self.iview.GetItemParent(parent_item)) == self.iview.getPackageMetricsName():

            # seleccion de un File
            if self.iview.GetItemText(parent_item) == self.iview.getPackageMetricsFileName():
                print ' menu Metric File'
                # self.iview.InitializeResultMenu(item)

            # seleccion de un Test
            elif self.iview.GetItemText(parent_item) == self.iview.getPackageMetricsTestName():
                print ' menu Metric Test'
                #self.iview.InitializeAnalysisMenu(data)

    def getItemSelected(self):
        return self.iview.GetSelection()

    def getItemDate(self):
        item = self.iview.GetSelection()
        return self.iview.GetItemPyData(item)

    def getItemEndDataSelected(self):
        item = self.iview.GetSelection()
        data = self.iview.GetItemPyData(item)
        return item, data
    # ----------------------------------------------------

    # - funciones encargadas del abm de datos de proyectos(model)----------
    # ----- abm of data-------------------------------------------------
    def DeleteProjectData(self, project):
        ProjectModel().delete(project)

    def UpdateProjectData(self, project):
        return ProjectModel().upDate(project)

    def GetProjectByName(self, name):
        return ProjectModel().getProjectForName(name)
    # ----------------------------------------------------------
