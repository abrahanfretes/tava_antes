# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''

import wx
from py.una.pol.tava.presenter.ptree import ProjectTreeCtrlPresenter
from py.una.pol.tava.view.vmenu import ProjectMenu, ResultPackageMenu
from py.una.pol.tava.view.vmenu import AnalysisPackageMenu, ResultMenu
from py.una.pol.tava.view.vmenu import MetricsFilesPackageMenu
from py.una.pol.tava.view.vmenu import MetricsViewsPackageMenu
from py.una.pol.tava.view.vmenu import AnalysisMenu
from py.una.pol.tava.base.entity import CLOSED, Project
import wx.lib.agw.customtreectrl as CT
import py.una.pol.tava.view.vimages as I
from wx import GetTranslation as _
import py.una.pol.tava.view.vi18n as C


class ProjectTreeCtrl(CT.CustomTreeCtrl):
    '''
    Clase Arbol que contendra los projectos representados como hijos del arbol
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        super(ProjectTreeCtrl, self).__init__(parent)

        self.SetAGWWindowStyleFlag(CT.TR_HAS_BUTTONS | CT.TR_HIDE_ROOT)

        # Definicion del presenter de la clase
        self.presenter = ProjectTreeCtrlPresenter(self)

        # Establecemos el color del fondo del arbol a Blanco
        self.SetBackgroundColour('#FFFFFF')

        # Definicion del listado de imagenes empleadas por el arbol
        il = wx.ImageList(16, 16)
        self.folder_bmp = il.Add(I.folder_png)
        self.folder_open_bmp = il.Add(I.folderOpen_png)
        self.folder_closed_bmp = il.Add(I.folderClosed_png)
        self.file_bmp = il.Add(I.result_png)
        self.package_bmp = il.Add(I.package_result_png)
        self.package_close = il.Add(I.package_close_png)
        self.AssignImageList(il)

        # Definicion del nodo raiz del arbol
        self.root = self.AddRoot("Projects")

        # Inicializacion del arbol de proyectos
        self.presenter.InitializeTree()

        # Enlace del evento Context a la entidad de Proyecto
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnTreeContextMenu)

        # Enlace del evento de seleccion al metodo OnSelectedItemTree
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectedItemTree)

        # Enlace del evento de expansion de item al metodo OnItemTreeExpanded
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemTreeExpanded)

    def OnSelectedItemTree(self, event):
        self.presenter.GetTypeSelectedItem()

    def AddProjectOpenNode(self, project):
        project_item = self.AppendItem(self.root, project.name)
        self.SetItemPyData(project_item, project)
        self.SetItemImage(project_item, 0, wx.TreeItemIcon_Normal)
        self.SetItemImage(project_item, 1, wx.TreeItemIcon_Expanded)

        return project_item

    def AddProjectCloseNode(self, project):
        project_item = self.AppendItem(self.root, project.name)
        self.SetItemPyData(project_item, project)
        self.SetItemImage(project_item, 2, wx.TreeItemIcon_Normal)
        self.SetItemTextColour(project_item, '#BFBFBF')

        return project_item

    # Se reesscribe este metodo para el SortChildren
    def OnCompareItems(self, item1, item2):
        # si se ordenan proyectos
        # Se concatena el estado y el nombre del proyecto para tener encuenta
        # los dos atributos en la comparacion
        if self.GetItemParent(item1) == self.root:
            itemc1 = str(item1.GetData().state) + item1.GetData().name
            itemc2 = str(item2.GetData().state) + item2.GetData().name
        # si se ordenan Archivos
        else:
            itemc1 = item1.GetData().name
            itemc2 = item2.GetData().name

        return cmp(itemc1, itemc2)

    def OnTreeContextMenu(self, event):
        self.presenter.ContexMenu()

    def InitializeProjectMenu(self, date_item):
        menu = ProjectMenu(self, date_item)
        self.PopupMenu(menu)

    def InitializeResultPackageMenu(self, date_item):
        menu = ResultPackageMenu(self, date_item)
        self.PopupMenu(menu)

    def InitializeAnalysisPackageMenu(self, date_item):
        menu = AnalysisPackageMenu(self, date_item)
        self.PopupMenu(menu)

    def InitializeResultMenu(self, date_item):
        menu = ResultMenu(self, date_item)
        self.PopupMenu(menu)

    def InitializeAnalysisMenu(self, date_item):
        menu = AnalysisMenu(self, date_item)
        self.PopupMenu(menu)

    # menus para Metrics
    def InitializeMetricsFilesPackageMenu(self, project):
        menu = MetricsFilesPackageMenu(self, project)
        self.PopupMenu(menu)

    def InitializeMetricsViewsPackageMenu(self, project):
        menu = MetricsViewsPackageMenu(self, project)
        self.PopupMenu(menu)

    def AddResultToProject(self, package_item, result):
        result_item = self.AppendItem(package_item, result.name)
        self.SetItemImage(result_item, 3, wx.TreeItemIcon_Normal)
        self.SetItemPyData(result_item, result)

    def AddTestToProject(self, package_item, test):
        test_item = self.AppendItem(package_item, test.name)
        self.SetItemImage(test_item, 3, wx.TreeItemIcon_Normal)
        self.SetItemPyData(test_item, test)

    # -- Parte del árbol para la parte gáfica
    def AddItemTestGraphic(self, project_item):
        item = self.AppendItem(project_item, self.getPackageGraphicsName())
        self.SetItemImage(item, 5, wx.TreeItemIcon_Normal)
        self.SetItemImage(item, 4, wx.TreeItemIcon_Expanded)
        return item

    def AddPackageResult(self, project_item):
        item = self.AppendItem(project_item, self.getPackageGraphicsFileName())
        self.SetItemImage(item, 5, wx.TreeItemIcon_Normal)
        self.SetItemImage(item, 4, wx.TreeItemIcon_Expanded)
        return item

    def AddPackageAnalyzer(self, project_item):
        item = self.AppendItem(project_item, self.getPackageGraphicsTestName())
        self.SetItemImage(item, 5, wx.TreeItemIcon_Normal)
        self.SetItemImage(item, 4, wx.TreeItemIcon_Expanded)
        return item

    # -- Parte del árbol para la parte gáfica
    def AddItemTestMetrics(self, project_item):
        item = self.AppendItem(project_item, self.getPackageMetricsName())
        self.SetItemImage(item, 5, wx.TreeItemIcon_Normal)
        self.SetItemImage(item, 4, wx.TreeItemIcon_Expanded)
        return item

    def AddMetricResults(self, tm_item):
        item = self.AppendItem(tm_item, self.getPackageMetricsFileName())
        self.SetItemImage(item, 5, wx.TreeItemIcon_Normal)
        self.SetItemImage(item, 4, wx.TreeItemIcon_Expanded)
        return item

    def AddPackageMetricViews(self, tm_item):
        item = self.AppendItem(tm_item, self.getPackageMetricsTestName())
        self.SetItemImage(item, 5, wx.TreeItemIcon_Normal)
        self.SetItemImage(item, 4, wx.TreeItemIcon_Expanded)
        return item

    def OnItemTreeExpanded(self, event):
        item = self.GetSelection()
        date_item = self.GetItemPyData(item)

        if date_item is None:
            return
        elif isinstance(date_item, Project):
            if date_item.state == CLOSED:
                self.Collapse(item)

    def getPackageGraphicsName(self):
        return _(C.VTREE_PGN)

    def getPackageGraphicsFileName(self):
        return _(C.VTREE_PGFN)

    def getPackageGraphicsTestName(self):
        return _(C.VTREE_PGTN)

    def getPackageMetricsName(self):
        return _(C.VTREE_PMN)

    def getPackageMetricsFileName(self):
        return _(C.VTREE_PMFN)

    def getPackageMetricsTestName(self):
        return _(C.VTREE_PMMN)
