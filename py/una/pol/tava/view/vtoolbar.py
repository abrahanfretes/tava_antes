# -*- coding: utf-8 -*-
'''
Created on 27/05/2014

@author: aferreira
'''

import wx
from py.una.pol.tava.presenter.ptoolbar import ToolBarPresenter
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

        #El Presenter
        self.presenter = ToolBarPresenter(self)
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

        self.EnableTool(wx.ID_NEW, True)
        self.EnableTool(wx.ID_OPEN, False)
        self.EnableTool(wx.ID_SAVE, False)
        self.EnableTool(wx.ID_DELETE, False)
        self.EnableTool(wx.ID_EDIT, False)

        self.Bind(wx.EVT_TOOL, self.OnNewProjectView, id=wx.ID_NEW)
        self.Bind(wx.EVT_TOOL, self.OnCloseProjectView, id=wx.ID_SAVE)
        self.Bind(wx.EVT_TOOL, self.OnOpenProjectView, id=wx.ID_OPEN)
        self.Bind(wx.EVT_TOOL, self.OnDeleteProjectView, id=wx.ID_DELETE)

        self.AddSeparator()

        # iconos para el sistema
        exit_bmp = wx.ArtProvider.GetBitmap(wx.ART_QUIT)

        self.AddLabelTool(wx.ID_EXIT, '', exit_bmp, shortHelp=_(TB_EX))

        self.Bind(wx.EVT_TOOL, parent.OnExitAplication, id=wx.ID_EXIT)

        self.Realize()

    def OnOpenDisable(self):
        self.EnableTool(wx.ID_DELETE, True)
        self.EnableTool(wx.ID_SAVE, True)
        self.EnableTool(wx.ID_EDIT, True)
        self.EnableTool(wx.ID_OPEN, False)

    def OnCloseDisable(self):
        self.EnableTool(wx.ID_DELETE, True)
        self.EnableTool(wx.ID_OPEN, True)
        self.EnableTool(wx.ID_SAVE, False)
        self.EnableTool(wx.ID_EDIT, False)

    def OnAllDisable(self):
        self.EnableTool(wx.ID_DELETE, False)
        self.EnableTool(wx.ID_SAVE, False)
        self.EnableTool(wx.ID_EDIT, False)
        self.EnableTool(wx.ID_OPEN, False)

    def OnCloseProjectView(self, event):
        self.presenter.OnCloseProject()

    def OnOpenProjectView(self, event):
        self.presenter.OnOpenProject()

    def OnDeleteProjectView(self, event):
        self.presenter.OnDeleteProject()

    def OnNewProjectView(self, event):
        self.presenter.OnNewProject()
