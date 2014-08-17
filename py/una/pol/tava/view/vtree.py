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
from wx import GetTranslation as _
import py.una.pol.tava.view.vi18n as C
import wx.lib.agw.customtreectrl as CT


class ProjectTreeCtrl(CT.CustomTreeCtrl):
    '''
    classdocs
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        super(ProjectTreeCtrl, self).__init__(parent,
                                agwStyle=CT.TR_HAS_BUTTONS | CT.TR_HIDE_ROOT)

        self.SetBackgroundColour('#D9F0F8')

        il = wx.ImageList(16, 16)
        self.folder_bmp = il.Add(bitmap=wx.Bitmap('view/icons/folder.png'))
        self.folder_open_bmp = il.Add(
                            bitmap=wx.Bitmap('view/icons/folderOpen.png'))
        self.folder_closed_bmp = il.\
        Add(bitmap=wx.Bitmap('view/icons/folderClosed.png'))
        self.file_bmp = il.Add(bitmap=wx.Bitmap('view/icons/result.png'))
        self.AssignImageList(il)

        self.root = self.AddRoot("Proyectos")

        #defino el presenter que manejara a la vista
        self.presenter = ProjectTreeCtrlPresenter(self)
        self.presenter.OnInitializeTree()

        #menu del contexto de Proyecto
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnTreeContextMenu)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectedItemTree)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemTreeExpanded)

    def OnSelectedItemTree(self, event):
        item = self.GetSelection()
        if self.GetItemPyData(item) is not None:
            self.presenter.OnSelectedProjectSend()

    def AddProjectNode(self, project):
        project_item = self.AppendItem(self.root, project.name)
        self.SetItemPyData(project_item, project)
        self.SetItemImage(project_item, 0, wx.TreeItemIcon_Normal)
        self.SetItemImage(project_item, 1, wx.TreeItemIcon_Expanded)

        if project.state == CLOSED:
            self.SetItemImage(project_item, 2, wx.TreeItemIcon_Normal)
            self.SetItemTextColour(project_item, '#BFBFBF')
        else:
            #compelmentos prueba
            self.GetFiles(project_item)

        #ordenamiento personalizado
        self.SortItemChildren(self.root)

    def SortItemChildren(self, item_parent):
        self.SortChildren(item_parent)

    #se reesscribe este metodo
    def OnCompareItems(self, item1, item2):
        return cmp(item1.GetData().state, item2.GetData().state)

    def OnInitializeTree(self, list_project):
        for project in list_project:
            self.AddProjectNode(project)

    def OnTreeContextMenu(self, event):
        item = self.GetSelection()
        date_item = self.GetItemPyData(item)
        parent_item = self.GetItemParent(item)

        #verificar si el padre es root
        if(parent_item == self.root):
            menu = ProjectMenu(self, date_item)
        else:
            #si su padre no es root
            menu = ResultMenu(self, date_item)

        self.PopupMenu(menu)

    def OnDeleteItem(self, item):
        self.Delete(item)

    def GetFiles(self, parent):
        for z in range(3):
            if z == 0:
                item = self.AppendItem(parent,  "item %d" % z)
                self.SetItemHyperText(item, True)

            elif z == 1:
                item = self.AppendItem(parent,  "item %d" % z, ct_type=2)
            elif z == 2:
                item = self.AppendItem(parent,  "item %d" % z, ct_type=1)

            self.SetPyData(item, None)
            self.SetItemImage(item, 3, CT.TreeItemIcon_Normal)
            if z == 1:
                self.AppendSeparator(parent)

    def OnItemTreeExpanded(self, e):
        item = self.GetSelection()
        date_item = self.GetItemPyData(item)

        if date_item == None:
            return

        if date_item.state == 1:
            self.Collapse(item)


class ProjectMenu(wx.Menu):
    def __init__(self, parent, project):
        super(ProjectMenu, self).__init__()

        self.project = project
        self.presentermenu = ProjectMenuPresenter(self)

        new = wx.MenuItem(self, wx.ID_ANY, _(C.PM_NEW))

        open_item = wx.MenuItem(self, wx.ID_ANY, _(C.PM_OPEN))
        closed_item = wx.MenuItem(self, wx.ID_ANY, _(C.PM_CLOSE))
        delete_item = wx.MenuItem(self, wx.ID_DELETE, _(C.PM_DEL))
        hide_item = wx.MenuItem(self, wx.ID_ANY, _(C.PM_HIDE))

        rename_item = wx.MenuItem(self, wx.ID_ANY, _(C.PM_REN))
        properties_item = wx.MenuItem(self, wx.ID_ANY, _(C.PM_PROP))

        self.AppendItem(new)

        self.AppendSeparator()
        self.AppendItem(open_item)
        self.AppendItem(closed_item)
        self.AppendItem(delete_item)
        self.AppendItem(hide_item)

        self.AppendSeparator()
        self.AppendItem(rename_item)
        self.AppendItem(properties_item)

        if self.project.state == OPEN:
            open_item.Enable(False)
            hide_item.Enable(False)

        if self.project.state == CLOSED:
            closed_item.Enable(False)
            rename_item.Enable(False)
            properties_item.Enable(False)

        self.Bind(wx.EVT_MENU, self.OpenProject, open_item)
        self.Bind(wx.EVT_MENU, self.CloseProject, closed_item)
        self.Bind(wx.EVT_MENU, self.DeleteProject, delete_item)
        self.Bind(wx.EVT_MENU, self.HideProject, hide_item)
        self.Bind(wx.EVT_MENU, self.RenameProject, rename_item)
        self.Bind(wx.EVT_MENU, self.PropertiesProject, properties_item)

    def RenameProject(self, event):
        self.presentermenu.OnRename(self.project)

    def OpenProject(self, event):
        self.presentermenu.OnOpen()

    def CloseProject(self, event):
        self.presentermenu.OnClose()

    def DeleteProject(self, event):
        self.presentermenu.OnDelete()

    def PropertiesProject(self, event):
        self.presentermenu.ShowProperties()

    def HideProject(self, event):
        self.presentermenu.Hide()


class ResultMenu(wx.Menu):
    def __init__(self, parent, result):
        super(ResultMenu, self).__init__()

        self.result = result
        #self.presentermenu = ProjectMenuPresenter(self)

        graficar = wx.MenuItem(self, wx.ID_ANY, 'Graficar')
        ver = wx.MenuItem(self, wx.ID_ANY, 'Ver archivo')
        rename = wx.MenuItem(self, wx.ID_ANY, 'Renombrar')
        delete = wx.MenuItem(self, wx.ID_DELETE, 'Eliminar')
        properties = wx.MenuItem(self, wx.ID_ANY, 'Propiedades')

        self.AppendItem(graficar)

        self.AppendSeparator()
        self.AppendItem(ver)
        self.AppendItem(rename)
        self.AppendItem(delete)

        self.AppendSeparator()
        self.AppendItem(properties)

        graficar.Enable(False)
        ver.Enable(False)
        rename.Enable(False)
        delete.Enable(False)
        properties.Enable(False)
