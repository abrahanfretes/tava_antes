# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''

import wx
from py.una.pol.tava.presenter.ptree import ProjectTreeCtrlPresenter
from py.una.pol.tava.presenter.pprojectmenu import ProjectMenuPresenter
from py.una.pol.tava.base.entity import OPEN
from py.una.pol.tava.base.entity import CLOSED


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
        self.folder_closed_bmp = il.\
        Add(bitmap=wx.Bitmap('icons/folderClosed.png'))
        self.file_bmp = il.Add(bitmap=wx.Bitmap('icons/result.png'))
        self.AssignImageList(il)

        self.root = self.AddRoot("Proyectos")

        #defino el presenter que manejara a la vista
        self.presenter = ProjectTreeCtrlPresenter(self)
        self.presenter.OnInitializeTree()

        #menu del contexto de Proyecto
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnTreeContextMenu)
        self.Bind(wx.EVT_LEFT_UP, self.OnSelectedItemTree)

    def OnSelectedItemTree(self, event):
        item = self.GetSelection()
        project = self.GetItemPyData(item)
        self.presenter.OnSelectedProject(project, item)

    def AddProjectNode(self, project):
        project_item = self.AppendItem(self.root, project.name)
        self.SetItemPyData(project_item, project)
        if project.state == OPEN:
            self.SetItemImage(project_item, self.folder_bmp,
                              wx.TreeItemIcon_Normal)
            self.SetItemImage(project_item, self.folder_open_bmp,
                              wx.TreeItemIcon_Expanded)
        else:
            self.SetItemImage(project_item, self.folder_closed_bmp,
                              wx.TreeItemIcon_Normal)
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

        self.project = project_selected
        self.item = item
        self.presentermenu = ProjectMenuPresenter(self)

        new = wx.MenuItem(self, wx.ID_ANY, u"New")

        open_item = wx.MenuItem(self, wx.ID_ANY, u"Open")
        closed_item = wx.MenuItem(self, wx.ID_ANY, u"Close")
        delete_item = wx.MenuItem(self, wx.ID_DELETE, u"Delete")

        rename = wx.MenuItem(self, wx.ID_ANY, u"Rename")
        properties = wx.MenuItem(self, wx.ID_ANY, u"Properties")

        self.AppendItem(new)

        self.AppendSeparator()
        self.AppendItem(open_item)
        self.AppendItem(closed_item)
        self.AppendItem(delete_item)

        self.AppendSeparator()
        self.AppendItem(rename)
        self.AppendItem(properties)

        if self.project.state == OPEN:
            open_item.Enable(False)

        if self.project.state == CLOSED:
            closed_item.Enable(False)

        self.Bind(wx.EVT_MENU, self.OpenProject, open_item)
        self.Bind(wx.EVT_MENU, self.CloseProject, closed_item)
        self.Bind(wx.EVT_MENU, self.DeleteProject, delete_item)

    def OpenProject(self, event):

        self.presentermenu.OnOpen(self.project, self.item)

    def CloseProject(self, event):

        self.presentermenu.OnClose(self.project, self.item)

    def DeleteProject(self, event):
        result = self.GetDialog()
        if result == wx.YES:
            self.presentermenu.OnDelete(self.project, self.item)

    def  GetDialog(self):
        return wx.MessageBox("Está seguro que desea eliminar este Proyecto?",
                               "Eliminar Proyecto", style=wx.CENTER |
                               wx.ICON_WARNING | wx.YES_NO)
