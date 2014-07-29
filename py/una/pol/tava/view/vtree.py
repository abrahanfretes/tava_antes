# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''

import wx
#import oss
from py.una.pol.tava.presenter.ptree import ProjectTreeCtrlPresenter
from py.una.pol.tava.presenter.pprojectmenu import ProjectMenuPresenter


class ProjectTreeCtrl(wx.TreeCtrl):
    '''
    classdocs
    '''

    def __init__(self, parent, main_frame):
        '''
        Constructor
        '''
        super(ProjectTreeCtrl, self).__init__(parent,
                                style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)

        il = wx.ImageList(16, 16)
        self.folder_bmp = il.Add(bitmap=wx.Bitmap('icons/folder.png'))
        self.folder_open_bmp = il.Add(bitmap=wx.Bitmap('icons/folderOpen.png'))
        self.file_bmp = il.Add(bitmap=wx.Bitmap('icons/result.png'))
        self.AssignImageList(il)

        self.root = self.AddRoot("Proyectos")

        #defino el presenter que manejara a la vista
        self.presenter = ProjectTreeCtrlPresenter(self)
        self.presenter.OnInitializeTree()

        #menu del contexto de Proyecto
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnTreeContextMenu)

    def AddProjectNode(self, project):
        project_item = self.AppendItem(self.root, project.name)
        self.SetItemPyData(project_item, project)
        self.SetItemImage(project_item, self.folder_bmp,
                          wx.TreeItemIcon_Normal)
        self.SetItemImage(project_item, self.folder_open_bmp,
                          wx.TreeItemIcon_Expanded)
        self.SortChildren(self.root)

    def OnInitializeTree(self, list_project):
        for project in list_project:
            self.AddProjectNode(project)

    def OnTreeContextMenu(self, event):
        item = self.GetSelection()
        project = self.GetItemPyData(item)
        project_menu = ProjectMenu(self, project, item)
        self.PopupMenu(project_menu)

    def OnDeleteItem(self, item):
        self.Delete(item)


class ProjectMenu(wx.Menu):
    def __init__(self, parent, project_selected, item):
        super(ProjectMenu, self).__init__()

        # en este caso el id del proyecto
        self.project_selected = project_selected
        self.item = item
        self.presenter = ProjectMenuPresenter(self)

        new = wx.MenuItem(self, wx.ID_ANY, u"New")
        rename = wx.MenuItem(self, wx.ID_ANY, u"Rename")
        delete = wx.MenuItem(self, wx.ID_ANY, u"Delete")
        properties = wx.MenuItem(self, wx.ID_ANY, u"Properties")

        self.AppendItem(new)
        self.AppendSeparator()
        self.AppendItem(rename)
        self.AppendItem(properties)
        self.AppendItem(delete)

        self.Bind(wx.EVT_MENU, self.DeleteProject, delete)

    def DeleteProject(self, e):
        result = wx.MessageBox("Está seguro que desea eliminar este Proyecto?",
                               "Eliminar Proyecto", style=wx.CENTER |
                               wx.ICON_WARNING | wx.YES_NO)
        if result == wx.YES:
            self.presenter.OnDelete(self.project_selected, self.item)

