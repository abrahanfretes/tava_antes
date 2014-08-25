# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''
import wx

from py.una.pol.tava.view.vtree import ProjectTreeCtrl
from py.una.pol.tava.presenter.pbody import ProjectTreeNotebookPresenter
from wx import GetTranslation as _
import py.una.pol.tava.view.vi18n as C
import py.una.pol.tava.view.vimages as I


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
        right_notebook = wx.Notebook(right_panel, style=wx.SP_BORDER)

        # Definicion del panel que estara contenido en la notebook
        dpanel = wx.Panel(right_notebook, -1)

        # Establecemos el panel creado como pestaña para la notebook creada
        right_notebook.AddPage(dpanel, "Tab 1")

        # Creamos el sizer para el contenido del panel derecho
        right_panel_hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # Establecemos la notebook creada en el sizer
        right_panel_hsizer.Add(right_notebook, 1, wx.EXPAND)

        # Asociamos el sizer con el panel derecho
        right_panel.SetSizer(right_panel_hsizer)

        # Asociamos los paneles izquierdo y derecho al splitter
        self.splitter.SplitVertically(left_panel, right_panel, 300)
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
        self.SetBackgroundColour(self.GetThemeBackgroundColour())


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
