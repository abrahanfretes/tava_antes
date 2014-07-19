# -*- coding: utf-8 -*-
'''
Created on 27/05/2014

@author: aferreira
'''

import wx
import NuevoProyecto
from wx import GetTranslation as _

TB_EXIT = 1
TB_NEW_PROJECT = 2
TB_NP = "TOOLBAR_PRINCIPAL_NUEVO_PROYECTO"
TB_OP = "TOOLBAR_PRINCIPAL_ABRIR_PROYECTO"
TB_SP = "TOOLBAR_PRINCIPAL_GUARDAR_PROYECTO"
TB_EX = "TOOLBAR_PRINCIPAL_SALIR"


class ToolBarPrincipal(wx.ToolBar):
    '''
    Clase que representa al ToolBar Principal desplegando algunas opciones
    de trabajo que pueden utilizarse dentro del área de trabajo.
    '''

    def __init__(self, parent):
        '''
        Constructor para la clase ToolBarPrincipal
        :param parent: referencia a la clase padre de ToolBarPrincipal.
        '''
        super(ToolBarPrincipal, self).__init__(parent, wx.TB_HORIZONTAL)

        bmp = wx.ArtProvider.GetBitmap("gtk-new", wx.ART_NEW)

        self.AddLabelTool(TB_NEW_PROJECT, '', bmp, shortHelp=_(TB_NP))

        self.Bind(wx.EVT_TOOL, self.OnNuevoProyecto, id=TB_NEW_PROJECT)

#         self.AddSeparator()

        bmp = wx.ArtProvider.GetBitmap("gtk-open", wx.ART_FILE_OPEN)

        self.AddLabelTool(wx.ID_ANY, '', bmp, shortHelp=_(TB_OP))

        bmp = wx.ArtProvider.GetBitmap("gtk-save", wx.ART_FILE_SAVE)

        self.AddLabelTool(wx.ID_ANY, '', bmp, shortHelp=_(TB_SP))

        bmp = wx.ArtProvider.GetBitmap("gtk-quit", wx.ART_QUIT)

        self.AddLabelTool(TB_EXIT, '', bmp, shortHelp=_(TB_EX))

        self.Bind(wx.EVT_TOOL, self.OnQuit, id=TB_EXIT)

        self.Realize()

    def OnNuevoProyecto(self, e):
        '''
        Método que inicializa la clase de creación de un Nuevo Proyecto.
        :param e: evento de selección de ToolBar
        '''
        NuevoProyecto.NuevoProyecto(self.Parent)

    def OnQuit(self, e):
        '''
        Método invocado para cerrar el Frame Principal a través de una
        referencia al padre.
        :param e: evento de selección de ToolBar
        '''
        self.Parent.Close()
