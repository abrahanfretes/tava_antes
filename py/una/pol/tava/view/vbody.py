# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''
import wx

from py.una.pol.tava.model.mproject import ProjectModel
from py.una.pol.tava.view.vtree import ProjectTreeCtrl
from py.una.pol.tava.presenter.pbody import ProjectTreeNotebookPresenter
from wx import GetTranslation as _
import py.una.pol.tava.view.vi18n as C

import wx.propgrid as wxpg
from wx.lib.pubsub import Publisher as pub


class TreePanel(wx.Panel):
    def __init__(self, parent, main_frame):
        super(TreePanel, self).__init__(parent)

        # Creamos el arbol de Proyectos
        self.project_tree = ProjectTreeCtrl(self, main_frame)

        # Creamos un boxSizer para el arbol de Proyectos
        project_tree_vsizer = wx.BoxSizer(wx.VERTICAL)
        project_tree_vsizer.Add(self.project_tree, 1, wx.EXPAND | wx.ALL, 3)
        self.SetSizer(project_tree_vsizer)


class ProjectTreeNotebook(wx.Notebook):
    def __init__(self, parent, main_frame):
        super(ProjectTreeNotebook, self).__init__(parent, style=wx.BK_DEFAULT)

        self.presenter = ProjectTreeNotebookPresenter(self)

        self.project_tree_panel = TreePanel(self, main_frame)
        self.AddPage(self.project_tree_panel, _(C.MP_PE))

        # Se configura la pestaña de navegación de proyectos.
        il = wx.ImageList(16, 16)
        self.SetImageList(il)
        tree_explorer_bmp = il.Add(wx.Bitmap("view/icons/tree_explorer.gif",
                                             wx.BITMAP_TYPE_GIF))
        self.SetPageImage(0, tree_explorer_bmp)
        self.SetBackgroundColour(self.GetThemeBackgroundColour())


class MainPanel(wx.Panel):
    '''
    Clase que representa al Cuerpo Principal que contendrá el panel de
    navegación de Proyectos, área de trabajo y panel de propiedades de los
    objetos.
    '''

    def __init__(self, parent):
        '''
        Constructor de la clase MainPanel.
        :param parent: referencia a la clase padre de MainPanel.
        '''
        super(MainPanel, self).__init__(parent)
        self.SetBackgroundColour('#3B444B')

        self.splitter = wx.SplitterWindow(self, style=wx.SP_3D)

        # Se define un panel izquierdo que contendra el espacio de navegación
        # de los proyectos y una Notebook para la pestaña de navegación.
        left_panel = wx.Panel(self.splitter)
        left_panel.SetBackgroundColour('#FFFFFF')
        self.project_tree_notebook = ProjectTreeNotebook(left_panel, parent)
        project_tree_sizer = wx.BoxSizer()
        project_tree_sizer.Add(self.project_tree_notebook, 1, wx.EXPAND)

        left_panel.SetSizer(project_tree_sizer)

        # Creamos el panel derecho para el splitter
        right_panel = wx.Panel(self.splitter, -1)

        rigth_splitter = wx.SplitterWindow(right_panel)

        right_notebook = wx.Notebook(rigth_splitter, style=wx.SP_BORDER)
        dpanel = wx.Panel(right_notebook, -1)
        right_notebook.AddPage(dpanel, "Tab 1")

        # lado derecho del área de trabajo
        side_panel = PropertiesPanel(rigth_splitter)

        rigth_splitter.SplitVertically(right_notebook, side_panel, 700)
        rigth_splitter.SetMinimumPaneSize(1)

        # Creamos el sizer para el contenido del panel derecho
        right_panel_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        right_panel_hsizer.Add(rigth_splitter, 1, wx.EXPAND)
        right_panel.SetSizer(right_panel_hsizer)

        self.splitter.SplitVertically(left_panel, right_panel, 300)
        self.splitter.SetMinimumPaneSize(200)

        # Creamos el sizer para colocar el widget Splitter y expandirlo
        # en el Cuerpo Principal
        body_sizer = wx.BoxSizer(wx.VERTICAL)
        body_sizer.Add(self.splitter, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(body_sizer)

    def LoadProjects(self):
        proPresenter = ProjectModel()
        namesProjects = []
        for p in proPresenter.getAll():
            self.project_tree.AddProjectNode(self.project_tree.root,
                                              p.nombre, p.id)
            namesProjects.append(p.name)
        if self.project_tree.root:
            self.project_tree.SortChildren(self.project_tree.root)
        return namesProjects


class PropertiesPanel(wx.Panel):
    def __init__(self, parent):
        pub.subscribe(self.OnChange, "project.selected")
        wx.Panel.__init__(self, parent)
        topsizer = wx.BoxSizer(wx.VERTICAL)

        # Difference between using PropertyGridManager vs PropertyGrid is that
        # the manager supports multiple pages and a description box.
        pg = wxpg.PropertyGrid(self, style=wxpg.PG_AUTO_SORT |
                              wxpg.PG_TOOLBAR | wxpg.PG_SPLITTER_AUTO_CENTER)

        # Show help as tooltips
        pg.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)

        pg.Append(wxpg.PropertyCategory("Project Properties"))
        name = pg.Append(wxpg.StringProperty("Name", value=""))
        pg.SetPropertyValue(name, "Proyecto1")
        pg.DisableProperty(name)
        date = pg.Append(wxpg.DateProperty("Date", value=wx.DateTime_Now()))
        pg.DisableProperty(date)

        p = wx.Panel(self, wx.ID_ANY)
        text = wx.StaticText(p, label="Properties")
        text.SetForegroundColour(wx.BLACK)
        bsizer = wx.BoxSizer(wx.VERTICAL)
        bsizer.Add(text, 1, wx.ALL | wx.EXPAND)
        p.SetSizer(bsizer)
        p.SetBackgroundColour("#F07746")

        topsizer.Add(p, 0, wx.EXPAND | wx.ALL)

        topsizer.Add(pg, 1, wx.EXPAND | wx.ALL)

        self.SetSizer(topsizer)
        topsizer.SetSizeHints(self)

    def OnChange(self, message):
        print("esto tiene data")
        print message.data
        print("esto tiene data")
