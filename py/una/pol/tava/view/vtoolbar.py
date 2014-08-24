# -*- coding: utf-8 -*-
'''
Created on 27/05/2014

@author: aferreira
'''

import wx
from py.una.pol.tava.presenter.ptoolbar import ToolBarPresenter
from wx import GetTranslation as _
import py.una.pol.tava.view.vi18n as C
import py.una.pol.tava.view.vimages as I


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

        # Creacion del Presenter
        self.presenter = ToolBarPresenter(self)

        # Creacion de los ids de los diferentes tools
        self.SetIdReferences()

        self.SetToolBitmapSize((16, 16))

        # Nuevo Proyecto
        new_bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW)
        self.AddLabelTool(self.ID_NEW_PRO, '', new_bmp)
        self.EnableTool(self.ID_NEW_PRO, True)
        self.Bind(wx.EVT_TOOL, self.OnProjectNew, id=self.ID_NEW_PRO)

        # Abrir Proyecto
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN)
        self.AddLabelTool(self.ID_OPEN_PRO, '', open_bmp)
        self.EnableTool(self.ID_OPEN_PRO, False)
        self.Bind(wx.EVT_TOOL, self.OnProjectOpen, id=self.ID_OPEN_PRO)

        # Cerrar Proyecto
        self.AddLabelTool(self.ID_CLOSE_PRO, '', I.close_png)
        self.EnableTool(self.ID_CLOSE_PRO, False)
        self.Bind(wx.EVT_TOOL, self.OnProjectClose, id=self.ID_CLOSE_PRO)

        # Eliminar Proyecto
        self.AddLabelTool(self.ID_DEL_PRO, '', I.delete_png)
        self.EnableTool(self.ID_DEL_PRO, False)
        self.Bind(wx.EVT_TOOL, self.OnProjectDelete, id=self.ID_DEL_PRO)

        # Blog de Proyecto
        self.AddLabelTool(self.ID_BLOG_PRO, '', I.blog_png)
        self.EnableTool(self.ID_BLOG_PRO, False)

        self.AddSeparator()

        # Desocultar Proyecto
        self.AddLabelTool(self.ID_UNHIDE_PRO, '', I.hide_left_png)
        self.EnableTool(self.ID_UNHIDE_PRO, True)
        self.Bind(wx.EVT_TOOL, self.OnProjectUnHide, id=self.ID_UNHIDE_PRO)

        # Ocultar Proyecto
        self.AddLabelTool(self.ID_HIDE_PRO, '', I.hide_right_png)
        self.EnableTool(self.ID_HIDE_PRO, False)
        self.Bind(wx.EVT_TOOL, self.OnProjectHide, id=self.ID_HIDE_PRO)

        self.AddSeparator()

        # Salir Aplicacion
        exit_bmp = wx.ArtProvider.GetBitmap(wx.ART_QUIT)
        self.AddLabelTool(self.ID_EXIT_PRO, '', exit_bmp)
        self.Bind(wx.EVT_TOOL, parent.OnApplicationExit, id=self.ID_EXIT_PRO)

        # Establecemos los labels
        self.SetLabels()

        # Finalizando la creacion del toolbar
        self.Realize()

    def SetIdReferences(self):
        self.ID_NEW_PRO = wx.NewId()
        self.ID_OPEN_PRO = wx.NewId()
        self.ID_CLOSE_PRO = wx.NewId()
        self.ID_DEL_PRO = wx.NewId()
        self.ID_BLOG_PRO = wx.NewId()
        self.ID_EXIT_PRO = wx.NewId()
        self.ID_HIDE_PRO = wx.NewId()
        self.ID_UNHIDE_PRO = wx.NewId()

    def EnableDisableOpenProject(self):
        self.EnableTool(self.ID_DEL_PRO, True)
        self.EnableTool(self.ID_CLOSE_PRO, True)
        self.EnableTool(self.ID_BLOG_PRO, True)
        self.EnableTool(self.ID_OPEN_PRO, False)
        self.EnableTool(self.ID_HIDE_PRO, False)

    def EnableDisableCloseProject(self):
        self.EnableTool(self.ID_DEL_PRO, True)
        self.EnableTool(self.ID_OPEN_PRO, True)
        self.EnableTool(self.ID_CLOSE_PRO, False)
        self.EnableTool(self.ID_BLOG_PRO, False)
        self.EnableTool(self.ID_HIDE_PRO, True)

    def DisableAllProject(self):
        self.EnableTool(self.ID_DEL_PRO, False)
        self.EnableTool(self.ID_CLOSE_PRO, False)
        self.EnableTool(self.ID_BLOG_PRO, False)
        self.EnableTool(self.ID_OPEN_PRO, False)
        self.EnableTool(self.ID_HIDE_PRO, False)

    def OnProjectClose(self, event):
        self.presenter.CloseProject()

    def OnProjectOpen(self, event):
        self.presenter.OpenProject()

    def OnProjectDelete(self, event):
        self.presenter.DeleteProject()

    def OnProjectNew(self, event):
        self.presenter.NewProject()

    def OnProjectHide(self, event):
        self.presenter.HideProject()

    def OnProjectUnHide(self, event):
        self.presenter.UnHideProject()

    def SetLabels(self):
        self.SetToolShortHelp(self.ID_NEW_PRO, _(C.MTB_NP))
        self.SetToolShortHelp(self.ID_OPEN_PRO, _(C.MTB_OP))
        self.SetToolShortHelp(self.ID_CLOSE_PRO, _(C.MTB_CP))
        self.SetToolShortHelp(self.ID_DEL_PRO, _(C.MTB_DP))
        self.SetToolShortHelp(self.ID_BLOG_PRO, _(C.MTB_BP))
        self.SetToolShortHelp(self.ID_EXIT_PRO, _(C.MTB_EX))
        self.SetToolShortHelp(self.ID_HIDE_PRO, _(C.MTB_HP))
        self.SetToolShortHelp(self.ID_UNHIDE_PRO, _(C.MTB_UHP))
