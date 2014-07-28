# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''

import wx
import os
from py.una.pol.tava.model.mproject import ProjectModel
from py.una.pol.tava.model.mproject import ProjectModel as pro


class ProjectTreeContextMenu(object):
    def __init__(self):
        super(ProjectTreeContextMenu, self).__init__()
        self.project_menu = None
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnProjectTreeContextMenu)

    def OnProjectTreeContextMenu(self, event):
        if self.project_menu is not None:
            self.project_menu.Destroy()
        item = self.GetSelection()
        label = self.GetItemText(item)
        projects = self.getNamesProjects()
        self.project_menu = wx.Menu()
        if label in projects:
            self.CreateProjectTreeContextMenu(self.project_menu)
            self.PopupMenu(self.project_menu)
        elif wx.TreeItemIcon_Expanded == self.GetItemImage(item):
            self.CreateContextMenuGraphics(self.project_menu)
            self.PopupMenu(self.project_menu)

    def CreateContextMenuGraphics(self, menu):
        listGraphItems = wx.Menu()
        itemParallelCoord = wx.MenuItem(self.project_menu, wx.ID_ANY,
                                        u"Coordenadas Paralelas")
        self.Bind(wx.EVT_MENU, self.ShowPlot, itemParallelCoord)
        listGraphItems.AppendItem(itemParallelCoord)
        listGraphItems.Append(wx.ID_ANY, u"Scatter Plot")
        listGraphItems.Append(wx.ID_ANY, u"Heatmap")

        self.project_menu.AppendMenu(wx.ID_ANY, 'Graficar', listGraphItems)

    def ShowPlot(self, e):
        self.main_frame.cuerpoPrincipal.rightPanel.plot()

    def CreateProjectTreeContextMenu(self, menu):
        delete_project_item = wx.MenuItem(self.project_menu, wx.ID_ANY,
                                          u"Eliminar")
        self.Bind(wx.EVT_MENU, self.DeleteProject, delete_project_item)
        self.project_menu.AppendItem(delete_project_item)

        exit_item = wx.MenuItem(self.project_menu, wx.ID_EXIT, u"Salir")
        self.project_menu.AppendItem(exit_item)

    def AddFileResult(self, e):
        wildcard = "All files (*)|*"
        dialog = wx.FileDialog(None, "Seleccione los archivos", os.getcwd(),
                               "", wildcard, wx.OPEN | wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            item = self.GetSelection()
            self.resultados = item
            self.GetResultadosItem(item)
            self.AddNewItemsFiles(self.resultados, dialog.GetFilenames())

        dialog.Destroy()

    def DeleteProject(self, e):
        result = wx.MessageBox("Está seguro que desea eliminar este Proyecto?",
                               "Eliminar Proyecto", style=wx.CENTER |
                               wx.ICON_WARNING | wx.YES_NO)
        if result == wx.YES:
            item = self.GetSelection()
            id_project = self.GetItemPyData(item)
            proPresenter = ProjectModel()
            project = proPresenter.getProjectById(id_project)
            projects = self.getNamesProjects()
            del projects[projects.index(project.nombre)]
            proPresenter.delete(project)
            self.Delete(item)
            if self.root:
                self.SortChildren(self.root)

    def AddNewItemsFiles(self, parentItem, items):
        '''

        :param parentItem:
        :type parentItem:
        :param items:
        :type items:
        '''
        for item in items:
            new_item = self.AppendItem(parentItem, item.encode('utf8'))
            self.SetItemPyData(new_item, None)
            self.SetItemImage(new_item, self.file_bmp, wx.TreeItemIcon_Normal)

    def GetResultadosItem(self, parent, indent=0):
        text = self.GetItemText(parent)
        if text.encode('utf8') == "Resultados":
            self.SetResultadosItem(parent)
        indent += 4
        item, cookie = self.GetFirstChild(parent)
        while item:
            if self.ItemHasChildren(item):
                self.GetResultadosItem(item, indent)
            else:
                text = self.GetItemText(item)
                if text.encode('utf8') == "Resultados":
                    self.SetResultadosItem(item)
            item, cookie = self.GetNextChild(parent, cookie)

    def SetResultadosItem(self, item):
        self.resultados = item

    def getNamesProjects(self):
        return pro().getNamesProject()

    def OnQuit(self, e):
        self.main_frame.Close()


class ProjectTreeCtrl(wx.TreeCtrl, ProjectTreeContextMenu):
    '''
    classdocs
    '''

    def __init__(self, parent, main_frame):
        '''
        Constructor
        '''

        super(ProjectTreeCtrl, self).__init__(parent,
                                style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        ProjectTreeContextMenu.__init__(self)

        il = wx.ImageList(16, 16)
        self.folder_bmp = il.Add(bitmap=wx.Bitmap('icons/folder.png'))
        self.folder_open_bmp = il.Add(bitmap=wx.Bitmap('icons/folderOpen.png'))
        self.file_bmp = il.Add(bitmap=wx.Bitmap('icons/result.png'))

        self.AssignImageList(il)
        self.root = self.AddRoot("Proyectos")
        self.main_frame = main_frame
        self.OnInitializeTree()

    def AddProjectNode(self, project):
        project_item = self.AppendItem(self.root, project.name)
        self.SetItemPyData(project_item, project.id)
        self.SetItemImage(project_item, self.folder_bmp,
                          wx.TreeItemIcon_Normal)
        self.SetItemImage(project_item, self.folder_open_bmp,
                          wx.TreeItemIcon_Expanded)
        self.SortChildren(self.root)

    def AddTreeNodes(self, parentItem, items):
        for item in items:
            if type(item) == str or type(item) == unicode:
                new_item = self.AppendItem(parentItem, item)
                self.SetItemPyData(new_item, None)
                self.SetItemImage(new_item, self.file_bmp,
                                  wx.TreeItemIcon_Normal)
            else:
                new_item = self.AppendItem(parentItem, item[0])
                self.SetItemPyData(new_item, None)
                self.SetItemImage(new_item, self.folder_bmp,
                                  wx.TreeItemIcon_Normal)
                self.SetItemImage(new_item, self.folder_open_bmp,
                                  wx.TreeItemIcon_Expanded)

                self.AddTreeNodes(new_item, item[1])

    def OnInitializeTree(self):
        proPresenter = ProjectModel()
        for project in proPresenter.getAll():
            self.AddProjectNode(project)
