# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''
import wx
import ArbolProyecto

import random

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NTB
import matplotlib.pyplot as plt


class CuerpoPrincipal(wx.Panel):
    '''
    Clase que representa al Cuerpo Principal que contendra el panel de
    navegación de Proyectos, área de trabajo y panel de propiedades de los
    objetos.
    '''

    def __init__(self, parent):
        '''
        Constructor de la clase CuerpoPrincipal.
        :param parent: referencia a la clase padre de CuerpoPrincipal.
        '''
        super(CuerpoPrincipal, self).__init__(parent)
        self.SetBackgroundColour('#4f5049')

        #Diccionario que sera empleado para
        self.dictPathProjects = {}

        # Creamos un splitter window
        self.splitter = wx.SplitterWindow(self, -1)

        # Creamos un boxSizer para el arbol de Proyectos
        boxTreeProject = wx.BoxSizer(wx.VERTICAL)

        # Creamos el panel contenedor del arbol de proyectos
        panelProjectBrowser = wx.Panel(self.splitter)
        panelProjectBrowser.SetBackgroundColour('#FFFFFF')
        panelProjectBrowser.SetLabel("Explorador de Proyectos")

        notebook = wx.Notebook(panelProjectBrowser)
        panelTreeProjects = wx.Panel(notebook)

        # Creamos el arbol de Proyectos

        self.arbolProyecto = ArbolProyecto.ArbolProyecto(panelTreeProjects)

        # Seteamos la referencia al Frame Principal
        self.arbolProyecto.setFramePrincipalReference(parent)

#         pathWorkspace = self.Parent.workspace
#
#         listProject = getJerarquia([], pathWorkspace)
#
#         listado = listProject[1]
#         if listado:
#             for i in listado:
#                 self.dictPathProjects[i[0]] = pathWorkspace + "/" + i[0]

        # Registramos el path de los Proyectos
#         self.dictPathProjects[self.textNameProject.Value] = path

#         self.arbolProyecto.AddTreeNodes(self.arbolProyecto.root,
#                                         listProject[1])

        boxTreeProject.Add(self.arbolProyecto, 1, wx.EXPAND | wx.ALL, 10)

        panelTreeProjects.SetSizer(boxTreeProject)

        notebook.AddPage(panelTreeProjects, "Explorador de Proyectos")
        il = wx.ImageList(16, 16)
        notebook.SetImageList(il)
        icon = il.Add(wx.Bitmap("icons/tree_explorer.gif", wx.BITMAP_TYPE_GIF))
        notebook.SetPageImage(0, icon)
        notebook.SetBackgroundColour(notebook.GetThemeBackgroundColour())

        sizerTreeProjects = wx.BoxSizer()
        sizerTreeProjects.Add(notebook, 1, wx.EXPAND)
        panelProjectBrowser.SetSizer(sizerTreeProjects)

        self.rightPanel = p1(self.splitter)
#         rightPanel.plot()
        self.splitter.SplitVertically(panelProjectBrowser, self.rightPanel,
                                      300)

#         # Create the right panel
#         rightPanel = wx.Panel(self.splitter, -1)
#         # Create the right box sizer that will contain the panel's contents
#         rightBox = wx.BoxSizer(wx.VERTICAL)
#         # Create a widget to display static text and store it in the right
#         # panel
#         self.display = wx.StaticText(rightPanel, -1, '', (10, 10),
#                                      style=wx.ALIGN_CENTRE)
#         # Add the display widget to the right panel
#         rightBox.Add(self.display, -1, wx.EXPAND)
#         # Set the size of the right panel to that required by the
#         # display widget
#         rightPanel.SetSizer(rightBox)
#         # Put the left and right panes into the split window
#         self.splitter.SplitVertically(panelProjectBrowser, rightPanel,300)

        boxProjectBrowser = wx.BoxSizer(wx.VERTICAL)
        boxProjectBrowser.Add(self.splitter, 1, wx.EXPAND | wx.ALL, 20)
        self.SetSizer(boxProjectBrowser)


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
#         data = [random.random() for i in range(25)]
        data = [random.randrange(0, 25)]
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.plot(data, '*-')
        self.canvas.draw()
