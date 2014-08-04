# -*- coding: utf-8 -*-
'''
Created on 27/06/2014

@author: aferreira
'''

import wx

from py.una.pol.tava.view.vmenu import MainMenuBar
from py.una.pol.tava.view.vbody import MainPanel
from py.una.pol.tava.view.vtoolbar import MainToolBar
from py.una.pol.tava.view.vi18n import I18nLocale
from py.una.pol.tava.view.vproject import NewProjectDialog
from py.una.pol.tava.presenter.pframe import FramePresenter


class MainFrame(wx.Frame):
    '''
    Clase que representa al Frame raíz que contendrá a los demás componentes.
    '''

    def __init__(self, parent):
        '''
        :param parent: referencia a la clase padre del Frame Principal.
        '''
        super(MainFrame, self).__init__(parent, title='TAVA',
                                             size=wx.Size(1200, 800),
                                             style=wx.DEFAULT_FRAME_STYLE |
                                             wx.TAB_TRAVERSAL)
        #se agrega el presenter
        self.presenter = FramePresenter(self)

        self.setI18n()
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.InitUI()
        self.Centre(wx.BOTH)
#         self.Maximize()
        self.Show(True)

    def setI18n(self):
        self.i18n = I18nLocale()

    def InitUI(self):
        '''
        Método de inicialización del Menú, Toolbar y Cuerpo principal del
        programa.
        '''
        self.SetMainMenuBar()
        self.SetMainToolBar()
        self.SetMainPanel()

    def SetMainMenuBar(self):
        '''
        Creación de la clase vmenu como parte del Frame Principal.
        '''
        self.main_menubar = MainMenuBar(self)
        self.SetMenuBar(self.main_menubar)

    def SetMainToolBar(self):
        '''
        Creación de la clase vtoolbar como parte del Frame Principal.
        '''
        self.main_toolbar = MainToolBar(self)
        self.SetToolBar(self.main_toolbar)

    def SetMainPanel(self):
        '''
        Creación de la clase vbody como parte del Frame Principal.
        '''
        self.main_panel = MainPanel(self)

    def OnNewProject(self, e):
        '''
        Método que inicializa la clase de creación de un Nuevo Proyecto.
        :param e: evento de selección de Menú.
        '''
        NewProjectDialog(self)

    def OnExitAplication(self, e):

        result = wx.MessageBox("Desea salir de la aplicación",
                               style=wx.CENTER | wx.ICON_WARNING | wx.YES_NO)
        if result == wx.YES:
            self.Close()

    def OnBarNewProject(self):
        NewProjectDialog(self)
