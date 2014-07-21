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

        # iconos para los proyectos
        bmpNew = wx.ArtProvider.GetBitmap("gtk-new", wx.ART_NEW)
        bmpOpen = wx.ArtProvider.GetBitmap("gtk-open", wx.ART_FILE_OPEN)
        bmpClose = wx.Bitmap('icons/close.png')
        bmpDelete = wx.Bitmap('icons/delete.png')
        bmpBlog = wx.Bitmap('icons/blog.png')
        ##bmpSave = wx.ArtProvider.GetBitmap("gtk-save", wx.ART_FILE_SAVE)

        self.AddLabelTool(wx.ID_NEW, '', bmpNew, shortHelp=_(TB_NP))
        self.AddLabelTool(wx.ID_OPEN, '', bmpOpen, shortHelp=_(TB_OP))
        self.AddLabelTool(wx.ID_SAVE, '', bmpClose, shortHelp=_(TB_CP))
        self.AddLabelTool(wx.ID_DELETE, '', bmpDelete, shortHelp=_(TB_DP))
        self.AddLabelTool(wx.ID_EDIT, '', bmpBlog, shortHelp=TB_BP)
        ###self.AddLabelTool(wx.ID_SAVE, '', bmpSave, shortHelp=_(TB_SP))

        self.EnableToolNew()
        self.DisableToolOpen()
        self.DisableToolClose()
        self.DisableToolDelete()
        self.DisableToolEdit()

        self.Bind(wx.EVT_TOOL, parent.OnNuevoProyecto, id=wx.ID_NEW)
        #self.Bind(wx.EVT_TOOL, parent.OnOpenProyecto, id=wx.ID_OPEN)
        #self.Bind(wx.EVT_TOOL, parent.OnOpenProyecto, id=wx.ID_SAVE)
        #self.Bind(wx.EVT_TOOL, parent.OnDeleteProyecto, id=wx.ID_DELETE)
        #self.Bind(wx.EVT_TOOL, parent.OnEditProyecto, id=wx.ID_EDIT)
        ##self.Bind(wx.EVT_TOOL, parent.OnSaveProyecto, id=wx.ID_SAVE)

        self.AddSeparator()

        # iconos para el sistema
        bmp = wx.ArtProvider.GetBitmap("gtk-quit", wx.ART_QUIT)

        self.AddLabelTool(wx.ID_EXIT, '', bmp, shortHelp=_(TB_EX))

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
