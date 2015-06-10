# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''
import wx
from wx import GetTranslation as _
import wx.lib.agw.aui as aui

import vconstants as vc
from py.una.pol.tava.view.vtree import ProjectTreeCtrl
from py.una.pol.tava.presenter.pbody import ProjectTreeNotebookPresenter
import py.una.pol.tava.view.vi18n as C
import py.una.pol.tava.view.vimages as I
from py.una.pol.tava.presenter.pbody import AUINotebookPresenter
from py.una.pol.tava.view.vsom import PanelSomConfig
from py.una.pol.tava.base import tavac as tvc
from py.una.pol.tava.view.parallel.vparallelcoordinatesgf import\
    WorkingPageParallelGF
from py.una.pol.tava.view.curves.vwrappercurves import AndrewsCurves
from py.una.pol.tava.view.parallel.wrapperparallel import ParrallelCoordenates
from py.una.pol.tava.view.vscatter_matrix import PanelScatterMatrixCongif
from py.una.pol.tava.view.boxplot.wrapperboxplot import BoxPlot


class MainPanel(wx.Panel):
    '''
    Clase Panel que representa al Cuerpo Principal que contendrá el panel de
    navegación de Proyectos, área de trabajo, etc.
    '''

    def __init__(self, parent):
        '''
        Constructor de la clase MainPanel.
        :param parent: referencia a la clase padre de MainPanel.
        '''
        super(MainPanel, self).__init__(parent)

        # Seteamos el color de fondo
        self.SetBackgroundColour('#3B444B')

        # Definicion del Splitter que divide el area de trabajo de la
        # exploración de proyectos
        self.splitter = wx.SplitterWindow(self, style=wx.SP_3D)

        # Definicion del panel izquierdo que contendra el panel de explorcion
        # de proyectos.
        left_panel = wx.Panel(self.splitter)
        left_panel.SetBackgroundColour('#FFFFFF')

        # Definicion de la clase Notebook para el explorador de proyectos
        self.project_tree_notebook = ProjectTreeNotebook(left_panel)

        # Definicion del Sizer para la clase Notebook
        project_tree_sizer = wx.BoxSizer()
        project_tree_sizer.Add(self.project_tree_notebook, 1, wx.EXPAND)

        # Asociamos el sizer al panel izquierdo
        left_panel.SetSizer(project_tree_sizer)

        # Definicion del panel derecho para el splitter
        right_panel = wx.Panel(self.splitter, -1)

        # Definicion del componente Notebook para el panel derecho
        right_notebook = AUINotebook(right_panel)

        # Creamos el sizer para el contenido del panel derecho
        right_panel_hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # Establecemos la notebook creada en el sizer
        right_panel_hsizer.Add(right_notebook, 1, wx.EXPAND)

        # Asociamos el sizer con el panel derecho
        right_panel.SetSizer(right_panel_hsizer)

        # Asociamos los paneles izquierdo y derecho al splitter
        self.splitter.SplitVertically(left_panel, right_panel, 210)
        self.splitter.SetMinimumPaneSize(200)

        # Creamos el sizer para colocar el Splitter y expandirlo
        # en el MainPanel
        body_sizer = wx.BoxSizer(wx.VERTICAL)
        body_sizer.Add(self.splitter, 1, wx.EXPAND | wx.ALL, 10)

        # Asociamos el sizer creado con la clase MainPanel
        self.SetSizer(body_sizer)


class ProjectTreeNotebook(wx.Notebook):
    '''
    Clase Notebook que contendrá la pestaña que albergará el árbol de
    proyectos.
    '''
    def __init__(self, parent):
        super(ProjectTreeNotebook, self).__init__(parent, style=wx.BK_DEFAULT)

        # Definición del Presenter
        self.presenter = ProjectTreeNotebookPresenter(self)

        # Creacion del panel contenedor del arbol de Proyectos
        self.project_tree_panel = TreePanel(self)

        # El panel es agregado como pagina del componente Notebook con su
        # correspondiente label
        self.AddPage(self.project_tree_panel, _(C.MP_PE))

        # Se añade el icono de explorador de proyectos a la unica pestaña.
        il = wx.ImageList(16, 16)
        self.SetImageList(il)
        tree_explorer_bmp = il.Add(I.tree_explorer_gif)
        self.SetPageImage(0, tree_explorer_bmp)

        # Se establece el color de fondo para el componente Notebook.
        self.SetBackgroundColour("#FFFFFF")


class TreePanel(wx.Panel):
    '''
    Clase Panel que contendrá el árbol de exploración de proyectos.
    '''
    def __init__(self, parent):
        super(TreePanel, self).__init__(parent)

        # Creamos el arbol de Proyectos y lo asociamos al Panel
        self.project_tree = ProjectTreeCtrl(self)

        # Creamos un boxSizer para el arbol de Proyectos y lo añadimos al Panel
        project_tree_vsizer = wx.BoxSizer(wx.VERTICAL)
        project_tree_vsizer.Add(self.project_tree, 1, wx.EXPAND | wx.ALL, 3)

        # Asociamos el sizer a la clase Panel
        self.SetSizer(project_tree_vsizer)


from py.una.pol.tava.view.metric.vwrappermetric import WrapperMetric


class AUINotebook(aui.AuiNotebook):
    '''
    AUI Notebook class
    '''

    def __init__(self, parent):
        '''
        Método de inicialización de la clase AUINotebook.
        :param parent: referencia al objeto padre de la clase.
        '''
        aui.AuiNotebook.__init__(self, parent=parent)

        # ------ Definiciones iniciales ----------------------
        self.presenter = AUINotebookPresenter(self)
        self.InitUI()
        # ----------------------------------------------------

    def InitUI(self):
        self.default_style = (aui.AUI_NB_DEFAULT_STYLE |
                              aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER)

        self.SetWindowStyleFlag(self.default_style)

        self.SetArtProvider(aui.ChromeTabArt())

    def OnAddPage(self, test, mode):
        if mode == vc.SOM:
            working_space = PanelSomConfig(self, test)
            self.AddPage(working_space, test.name + "- SOM", True)
        elif mode == tvc.MODE_PARALLEL_COORDINATES_GF:
            working_space = WorkingPageParallelGF(self, test)
            self.AddPage(working_space, test.name + "- Parallel", True)
        elif mode == tvc.MODE_PARALLEL_COORDINATES_AL:
            working_space = ParrallelCoordenates(self, test)
            self.AddPage(working_space, test.name + "- Parallel", True)
        elif mode == tvc.MODE_ANDREWS_CURVES:
            page_ac = AndrewsCurves(self, test)
            self.AddPage(page_ac, test.name + "Andrews Curves", True)
        elif mode == vc.SCATTER_MATRIX:
            working_space = PanelScatterMatrixCongif(self, test)
            self.AddPage(working_space, test.name + "- Scatter Matrix", True)
        elif mode == tvc.MODE_BOX_PLOT:
            page_bp = BoxPlot(self, test)
            self.AddPage(page_bp, test.name + " - Box Plot", True)
        elif mode == 50:
            print 'llegue 50'
            page_mt = WrapperMetric(self, test)
            self.AddPage(page_mt, test.name + " - Metric", True)
