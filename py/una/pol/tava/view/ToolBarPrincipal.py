# -*- coding: utf-8 -*-
'''
Created on 27/05/2014

@author: aferreira
'''

import wx
import NuevoProyecto

TB_EXIT = 1
TB_NEW_PROJECT = 2


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

        self.AddLabelTool(TB_NEW_PROJECT, '', bmp, shortHelp="Nuevo Proyecto")

        self.Bind(wx.EVT_TOOL, self.OnNuevoProyecto, id=TB_NEW_PROJECT)

#         self.AddSeparator()

        bmp = wx.ArtProvider.GetBitmap("gtk-open", wx.ART_FILE_OPEN)

        self.AddLabelTool(wx.ID_ANY, '', bmp, shortHelp="Abrir Proyecto")

        bmp = wx.ArtProvider.GetBitmap("gtk-save", wx.ART_FILE_SAVE)

        self.AddLabelTool(wx.ID_ANY, '', bmp, shortHelp="Guardar")

        bmp = wx.ArtProvider.GetBitmap("gtk-quit", wx.ART_QUIT)

        self.AddLabelTool(TB_EXIT, '', bmp, shortHelp="Salir")

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
