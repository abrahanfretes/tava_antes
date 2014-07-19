# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''
import wx
import ArbolProyecto
from py.una.pol.tava.presenter.proPresenter import ProyectoPresenter
from wx import GetTranslation as _

import random

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NTB
import matplotlib.pyplot as plt
from wx.lib import scrolledpanel as scrolled

CP_EP = "CUERPO_PRINCIPAL_EXPLORADOR_PROYECTO"


class CuerpoPrincipal(wx.Panel):
    '''
    Clase que representa al Cuerpo Principal que contendrá el panel de
    navegación de Proyectos, área de trabajo y panel de propiedades de los
    objetos.
    '''

    def __init__(self, parent):
        '''
        Constructor de la clase CuerpoPrincipal.
        :param parent: referencia a la clase padre de CuerpoPrincipal.
        '''
        super(CuerpoPrincipal, self).__init__(parent)
        self.SetBackgroundColour('#3B444B')

        # Creamos un splitter window, separador de ventanas
        self.splitter = wx.SplitterWindow(self, style=wx.NO_3D | wx.SP_3D)

        # Creamos el panel izquierdo contenedor del arbol de proyectos
        leftPanel = wx.Panel(self.splitter)
        leftPanel.SetBackgroundColour('#FFFFFF')

        # Definimos un objeto Notebook que contendrá la única pestaña de
        # navegación de proyectos
        notebook = wx.Notebook(leftPanel, style=wx.BK_DEFAULT)

        # Definimos el panel padre del Arbol de Proyectos
        panelTreeProjects = wx.Panel(notebook)

        # Creamos el arbol de Proyectos
        self.arbolProyecto = ArbolProyecto.ArbolProyecto(panelTreeProjects)

        # Seteamos la referencia al Frame Principal en el objeto arbol
        self.arbolProyecto.setFramePrincipalReference(parent)

        # Cargamos los proyectos existentes y creamos una lista de nombres
        # de proyectos
        self.nameProjects = self.loadProjects()

        # Creamos un boxSizer para el arbol de Proyectos
        boxTreeProject = wx.BoxSizer(wx.VERTICAL)
        boxTreeProject.Add(self.arbolProyecto, 1, wx.EXPAND | wx.ALL, 10)

        panelTreeProjects.SetSizer(boxTreeProject)

        # Colocamos el panel del arbol dentro del componente Notebook
        notebook.AddPage(panelTreeProjects, _(CP_EP))
        il = wx.ImageList(16, 16)
        notebook.SetImageList(il)
        icon = il.Add(wx.Bitmap("icons/tree_explorer.gif", wx.BITMAP_TYPE_GIF))
        notebook.SetPageImage(0, icon)
        notebook.SetBackgroundColour(notebook.GetThemeBackgroundColour())

        # Creamos un Sizer que contendra al objeto Notebook, para luego
        # expandirlo por panel de Navegacion de Proyectos
        sizerTreeProjects = wx.BoxSizer()
        sizerTreeProjects.Add(notebook, 1, wx.EXPAND)
        leftPanel.SetSizer(sizerTreeProjects)

#         self.rightPanel = p1(self.splitter)

        # Creamos el panel derecho para el splitter
        rightPanel = wx.Panel(self.splitter, -1)

        # Creamos el sizer para el contenido del panel derecho
        rightBox = wx.BoxSizer(wx.HORIZONTAL)

        tabs = wx.Notebook(rightPanel)
#         dpanel = DrawingPanel(tabs)
        dpanel = p1(tabs)
#         dpanel.plot()
        tabs.AddPage(dpanel, "Tab 1")

        spanel = SidePanel(rightPanel)

        # Add the display widget to the right panel
        rightBox.Add(tabs, 2, wx.EXPAND)
        rightBox.Add(spanel, 0, wx.EXPAND)
        # Set the size of the right panel to that required by the
        # display widget
        rightPanel.SetSizer(rightBox)
        # Put the left and right panes into the split window

        self.splitter.SplitVertically(leftPanel, rightPanel, 300)
        self.splitter.SetSashPosition(300, True)
        self.splitter.SetMinimumPaneSize(200)

        # Creamos el sizer para colocar el widget Splitter y expandirlo
        # en el Cuerpo Principal
        boxProjectBrowser = wx.BoxSizer(wx.VERTICAL)
        boxProjectBrowser.Add(self.splitter, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(boxProjectBrowser)

    def loadProjects(self):
        proPresenter = ProyectoPresenter()
        namesProjects = []
        for p in proPresenter.getAll():
            self.arbolProyecto.AddProjectNode(self.arbolProyecto.root,
                                              p.nombre, p.id)
            namesProjects.append(p.nombre)
        if self.arbolProyecto.root:
            self.arbolProyecto.SortChildren(self.arbolProyecto.root)
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


class p1(wx.Panel):
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
