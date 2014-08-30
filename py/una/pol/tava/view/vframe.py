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
from py.una.pol.tava.view.vproject import RenameProjectDialog
from py.una.pol.tava.view.vproject import DeleteProjectDialog
from py.una.pol.tava.view.vproject import PropertiesProjectDialog
from py.una.pol.tava.view.vproject import UnHideProjectDialog
from py.una.pol.tava.view.vresult import AddFileDialog
from py.una.pol.tava.presenter.pframe import FramePresenter
from wx import GetTranslation as _
import py.una.pol.tava.view.vi18n as C


class MainFrame(wx.Frame):
    '''
    Clase que representa al Frame raíz que contendrá a los demás componentes.
    '''

    def __init__(self, parent):
        '''
        :param parent: referencia a la clase padre del Frame Principal.
        '''
        super(MainFrame, self).__init__(parent, title='TAVA',
                                             size=wx.Size(800, 400),
                                             style=wx.DEFAULT_FRAME_STYLE |
                                             wx.TAB_TRAVERSAL)
        #se agrega el presenter
        self.presenter = FramePresenter(self)

        self.SetI18n()
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.InitUI()
        self.Centre(wx.BOTH)
#         self.Maximize()
        self.Show(True)

    def SetI18n(self):
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
        MainPanel(self)

    def OnProjectNew(self, e):
        '''
        Método que inicializa la clase de creación de un Nuevo Proyecto.
        :param e: evento de selección de Menú.
        '''
        self.ShowNewProjectDialog()

    def ShowNewProjectDialog(self):
        NewProjectDialog(self)

    def ShowProjectProperties(self, project):
        PropertiesProjectDialog(self, project)

    def ShowRenameProjectDialog(self, project):
        RenameProjectDialog(self, project)

    def ShowDeleteProjectDialog(self):
        DeleteProjectDialog()

    def ShowUnHideProjectDialog(self):
        UnHideProjectDialog(self)

    def ShowAddFileInProjectDialog(self, project):
        AddFileDialog(self, project)

    def OnApplicationExit(self, e):

        result = wx.MessageBox(_(C.MF_EAM), _(C.MF_EAT),
                               style=wx.YES_NO | wx.NO_DEFAULT | wx.CENTER |
                               wx.ICON_QUESTION)
        if result == wx.YES:
            self.Close(True)
