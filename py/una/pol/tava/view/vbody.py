# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''
import wx

from py.una.pol.tava.model.mproject import ProjectModel
from py.una.pol.tava.view.vtree import ProjectTreeCtrl
from wx import GetTranslation as _

import random

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NTB
import matplotlib.pyplot as plt
from wx.lib import scrolledpanel as scrolled

CP_EP = "CUERPO_PRINCIPAL_EXPLORADOR_PROYECTO"


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

        self.project_tree_panel = TreePanel(self, main_frame)
        self.AddPage(self.project_tree_panel, _(CP_EP))

        # Se configura la pestaña de navegación de proyectos.
        il = wx.ImageList(16, 16)
        self.SetImageList(il)
        tree_explorer_bmp = il.Add(wx.Bitmap("icons/tree_explorer.gif",
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

        right_notebook = wx.Notebook(right_panel)
        dpanel = pl(right_notebook)
        right_notebook.AddPage(dpanel, "Tab 1")

        # lado derecho del área de trabajo
        side_panel = SidePanel(right_panel)

        # Creamos el sizer para el contenido del panel derecho
        right_panel_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        right_panel_hsizer.Add(right_notebook, 2, wx.EXPAND)
        right_panel_hsizer.Add(side_panel, 0, wx.EXPAND)
        right_panel.SetSizer(right_panel_hsizer)

        self.splitter.SplitVertically(left_panel, right_panel, 300)
        self.splitter.SetSashPosition(300, True)
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


class DrawingPanel(wx.ScrolledWindow):
    def __init__(self, tab):
        wx.ScrolledWindow.__init__(self, tab, style=wx.CLIP_CHILDREN)
        self.SetBackgroundColour("#B2BEB5")


class Notes(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(170, -1), style=wx.RAISED_BORDER)
        tree = wx.TreeCtrl(self, size=(170, -1), style=wx.TR_HAS_BUTTONS)
        tree.AddRoot("Aqui hay una notaaa")
        sizer = wx.BoxSizer()
        sizer.Add(tree, 1, wx.EXPAND)
        self.SetSizer(sizer)


class Thumbs(scrolled.ScrolledPanel):

    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, size=(170, -1),
                                        style=wx.VSCROLL | wx.RAISED_BORDER)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.SetScrollRate(0, 250)
        btn = wx.BitmapButton(self, size=(150, 150))
        text = wx.StaticText(self, label="Tab 1")

        self.sizer.Add(text, flag=wx.ALIGN_CENTER | wx.TOP, border=5)
        self.sizer.Add(btn, flag=wx.TOP | wx.LEFT, border=6)


class SidePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(170, -1), style=wx.RAISED_BORDER)
        self.cp = wx.CollapsiblePane(self, style=wx.CP_DEFAULT_STYLE |
                                                  wx.CP_NO_TLW_RESIZE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        csizer = wx.BoxSizer(wx.VERTICAL)
        self.cp.GetPane().SetSizer(csizer)

        self.tabs = wx.Notebook(self.cp.GetPane())
        self.thumbs = Thumbs(self.tabs)
        self.notes = Notes(self.tabs)
        self.tabs.AddPage(self.thumbs, "Thumbnails")
        self.tabs.AddPage(self.notes, "Notes")
        csizer.Add(self.tabs, 1, wx.EXPAND)
        sizer.Add(self.cp, 1, wx.EXPAND)

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnToggleCollapse)

        self.cp.Expand()

    def OnToggleCollapse(self, evt):
#         frame = self.GetTopLevelParent()
        frame = self.GetParent()
        frame.Layout()


class pl(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = plt.figure()

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NTB(self.canvas)
        self.toolbar.Hide()

        bs = wx.BoxSizer()
        bs.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(bs)

    def plot(self):
        ''' plot some random stuff '''
        data = [random.random() for i in range(25)]
#         data = [random.randrange(0, 25)]
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.plot(data, '*-')
        self.canvas.draw()
