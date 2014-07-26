# -*- coding: utf-8 -*-
'''
Created on 27/06/2014

@author: aferreira
'''

import wx

from MenuPrincipal import MenuPrincipal
from CuerpoPrincipal import CuerpoPrincipal
from ToolBarPrincipal import ToolBarPrincipal
from I18nHelper import I18nHelper
from py.una.pol.tava.view import projectview


class FramePrincipal (wx.Frame):
    '''
    Clase que representa al Frame raíz que contendrá a los demás componentes.
    '''

    def __init__(self, parent):
        '''
        :param parent: referencia a la clase padre del Frame Principal.
        '''
        super(FramePrincipal, self).__init__(parent, title='TAVA',
                                             size=wx.Size(1200, 800),
                                             style=wx.DEFAULT_FRAME_STYLE |
                                             wx.TAB_TRAVERSAL)
        self.setI18n()
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.InitUI()
        self.Centre(wx.BOTH)
#         self.Maximize()
        self.Show(True)

    def setI18n(self):
        self.i18n = I18nHelper()

    def InitUI(self):
        '''
        Método de inicialización del Menú, Toolbar y Cuerpo principal del
        programa.
        '''
        self.setMenuPrincipal()
        self.setToolbarPrincipal()
        self.setCuerpoPrincipal()

    def setMenuPrincipal(self):
        '''
        Creación de la clase MenuPrincipal como parte del Frame Principal.
        '''
        self.menuPrincipal = MenuPrincipal(self)
        self.SetMenuBar(self.menuPrincipal)

    def setToolbarPrincipal(self):
        '''
        Creación de la clase ToolBarPrincipal como parte del Frame Principal.
        '''
        self.toolBarPrincipal = ToolBarPrincipal(self)
        self.SetToolBar(self.toolBarPrincipal)

    def setCuerpoPrincipal(self):
        '''
        Creación de la clase CuerpoPrincipal como parte del Frame Principal.
        '''
        self.cuerpoPrincipal = CuerpoPrincipal(self)

    def OnNuevoProyecto(self, e):
        '''
        Método que inicializa la clase de creación de un Nuevo Proyecto.
        :param e: evento de selección de Menú.
        '''

        projectview.NewProjectDialog(self)

    def OnExitAplication(self, e):

        result = wx.MessageBox("Desea Salir de la Aplicacion",
                               style=wx.CENTER | wx.ICON_WARNING | wx.YES_NO)
        if result == wx.YES:
            self.Close()
