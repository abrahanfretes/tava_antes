# -*- coding: utf-8 -*-
'''
Created on 27/05/2014

@author: aferreira
'''

import wx
from py.una.pol.tava.presenter.ptoolbar import ToolBarPresenter
from wx import GetTranslation as _
import py.una.pol.tava.view.vi18n as C

ID_NEW_PRO = wx.NewId()
ID_UNHIDE_PRO = wx.NewId()
ID_HIDE_PRO = wx.NewId()
ID_OPEN_PRO = wx.NewId()
ID_CLOSE_PRO = wx.NewId()
ID_DEL_PRO = wx.NewId()
ID_BLOG_PRO = wx.NewId()
ID_EXIT_PRO = wx.NewId()


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
        unhide_bmp = wx.Bitmap('view/icons/hide-left.png')

        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN)
        close_bmp = wx.Bitmap('view/icons/close.png')
        delete_bmp = wx.Bitmap('view/icons/delete.png')
        hide_bmp = wx.Bitmap('view/icons/hide-right.png')
        blog_bmp = wx.Bitmap('view/icons/blog.png')

        self.AddLabelTool(ID_NEW_PRO, '', new_bmp, shortHelp=_(C.MTB_NP))
        self.AddLabelTool(ID_UNHIDE_PRO, '', unhide_bmp, shortHelp=_(C.MTB_UHP))

        self.AddSeparator()

        self.AddLabelTool(ID_BLOG_PRO, '', blog_bmp, shortHelp=_(C.MTB_BP))
        self.AddLabelTool(ID_CLOSE_PRO, '', close_bmp, shortHelp=_(C.MTB_CP))
        self.AddLabelTool(ID_DEL_PRO, '', delete_bmp, shortHelp=_(C.MTB_DP))
        self.AddLabelTool(ID_OPEN_PRO, '', open_bmp, shortHelp=_(C.MTB_OP))
        self.AddLabelTool(ID_HIDE_PRO, '', hide_bmp, shortHelp=_(C.MTB_HP))

        self.EnableTool(ID_NEW_PRO, True)
        self.EnableTool(ID_UNHIDE_PRO, True)
        self.EnableTool(ID_OPEN_PRO, False)
        self.EnableTool(ID_CLOSE_PRO, False)
        self.EnableTool(ID_DEL_PRO, False)
        self.EnableTool(ID_BLOG_PRO, False)
        self.EnableTool(ID_HIDE_PRO, False)

        self.Bind(wx.EVT_TOOL, self.OnNewProjectView, id=ID_NEW_PRO)
        self.Bind(wx.EVT_TOOL, self.OnCloseProjectView, id=ID_CLOSE_PRO)
        self.Bind(wx.EVT_TOOL, self.OnOpenProjectView, id=ID_OPEN_PRO)
        self.Bind(wx.EVT_TOOL, self.OnDeleteProjectView, id=ID_DEL_PRO)
        self.Bind(wx.EVT_TOOL, self.OnHideProjectView, id=ID_HIDE_PRO)

        self.AddSeparator()

        # iconos para el sistema
        exit_bmp = wx.ArtProvider.GetBitmap(wx.ART_QUIT)

        self.AddLabelTool(ID_EXIT_PRO, '', exit_bmp, shortHelp=_(C.MTB_EX))

        self.Bind(wx.EVT_TOOL, parent.OnExitAplication, id=ID_EXIT_PRO)

        self.SetReferences()

        self.Realize()

    def SetReferences(self):
        self.ID_NEW_PRO = ID_NEW_PRO
        self.ID_OPEN_PRO = ID_OPEN_PRO
        self.ID_CLOSE_PRO = ID_CLOSE_PRO
        self.ID_DEL_PRO = ID_DEL_PRO
        self.ID_BLOG_PRO = ID_BLOG_PRO
        self.ID_EXIT_PRO = ID_EXIT_PRO
        self.ID_HIDE_PRO = ID_HIDE_PRO
        self.ID_UNHIDE_PRO = ID_UNHIDE_PRO

    def OnOpenDisable(self):
        self.EnableTool(ID_DEL_PRO, True)
        self.EnableTool(ID_CLOSE_PRO, True)
        self.EnableTool(ID_BLOG_PRO, True)
        self.EnableTool(ID_OPEN_PRO, False)
        self.EnableTool(ID_HIDE_PRO, False)

    def OnCloseDisable(self):
        self.EnableTool(ID_DEL_PRO, True)
        self.EnableTool(ID_OPEN_PRO, True)
        self.EnableTool(ID_CLOSE_PRO, False)
        self.EnableTool(ID_BLOG_PRO, False)
        self.EnableTool(ID_HIDE_PRO, True)

    def OnAllDisable(self):
        self.EnableTool(ID_DEL_PRO, False)
        self.EnableTool(ID_CLOSE_PRO, False)
        self.EnableTool(ID_BLOG_PRO, False)
        self.EnableTool(ID_OPEN_PRO, False)
        self.EnableTool(ID_HIDE_PRO, False)

    def OnCloseProjectView(self, event):
        self.presenter.OnCloseProjectSend()

    def OnOpenProjectView(self, event):
        self.presenter.OnOpenProject()

    def OnDeleteProjectView(self, event):
        self.presenter.OnDeleteProject()

    def OnNewProjectView(self, event):
        self.presenter.OnNewProject()

    def OnHideProjectView(self, event):
        self.presenter.OnHideProject()
