# -*- coding: utf-8 -*-
'''
Created on 27/05/2014

@author: aferreira
'''

import wx
from wx import GetTranslation as _

ID_EXIT_PRO = wx.NewId()
ID_NEW_PRO = wx.NewId()
ID_OPEN_PRO = wx.NewId()
ID_SAVE_PRO = wx.NewId()
ID_BLOG_PRO = wx.NewId()

TB_NP = "TOOLBAR_PRINCIPAL_NUEVO_PROYECTO"
TB_OP = "TOOLBAR_PRINCIPAL_ABRIR_PROYECTO"
TB_SP = "TOOLBAR_PRINCIPAL_GUARDAR_PROYECTO"
TB_EX = "TOOLBAR_PRINCIPAL_SALIR"

TB_BP = 'Blog del Proyecto'
TB_CP = 'Cerrar Proyecto'
TB_DP = 'Eliminar Proyecto'


class MainToolBar(wx.ToolBar):
    '''
    Clase que representa al ToolBar Principal desplegando algunas opciones
    de trabajo que pueden utilizarse dentro del área de trabajo.
    '''

    def __init__(self, parent):
        '''
        Constructor para la clase MainToolBar
        :param parent: referencia a la clase padre de MainToolBar.
        '''
        super(MainToolBar, self).__init__(parent, wx.TB_HORIZONTAL)

        # iconos para los proyectos
        new_bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN)
        close_bmp = wx.Bitmap('icons/close.png')
        delete_bmp = wx.Bitmap('icons/delete.png')
        blog_bmp = wx.Bitmap('icons/blog.png')

        self.AddLabelTool(wx.ID_NEW, '', new_bmp, shortHelp=_(TB_NP))
        self.AddLabelTool(wx.ID_OPEN, '', open_bmp, shortHelp=_(TB_OP))
        self.AddLabelTool(wx.ID_SAVE, '', close_bmp, shortHelp=_(TB_CP))
        self.AddLabelTool(wx.ID_DELETE, '', delete_bmp, shortHelp=_(TB_DP))
        self.AddLabelTool(wx.ID_EDIT, '', blog_bmp, shortHelp=TB_BP)

        self.EnableToolNew()
        self.DisableToolOpen()
        self.DisableToolClose()
        self.DisableToolDelete()
        self.DisableToolEdit()

        self.Bind(wx.EVT_TOOL, parent.OnNewProject, id=wx.ID_NEW)

        self.AddSeparator()

        # iconos para el sistema
        exit_bmp = wx.ArtProvider.GetBitmap(wx.ART_QUIT)

        self.AddLabelTool(wx.ID_EXIT, '', exit_bmp, shortHelp=_(TB_EX))

        self.Bind(wx.EVT_TOOL, parent.OnExitAplication, id=wx.ID_EXIT)

        self.Realize()

    def EnableToolNew(self):
        self.EnableTool(wx.ID_NEW, True)

    def DisableToolNew(self):
        self.EnableTool(wx.ID_NEW, False)

    def EnableToolOpen(self):
        self.EnableTool(wx.ID_OPEN, True)

    def DisableToolOpen(self):
        self.EnableTool(wx.ID_OPEN, False)

    def EnableToolClose(self):
        self.EnableTool(wx.ID_SAVE, True)

    def DisableToolClose(self):
        self.EnableTool(wx.ID_SAVE, False)

    def EnableToolDelete(self):
        self.EnableTool(wx.ID_DELETE, True)

    def DisableToolDelete(self):
        self.EnableTool(wx.ID_DELETE, False)

    def EnableToolEdit(self):
        self.EnableTool(wx.ID_EDIT, True)

    def DisableToolEdit(self):
        self.EnableTool(wx.ID_EDIT, False)