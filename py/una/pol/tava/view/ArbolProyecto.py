# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''

import wx
import os
from py.una.pol.tava.presenter.proPresenter import ProyectoPresenter
from py.una.pol.tava.presenter.proPresenter import ProyectoPresenter as pro


class ContextMenu(object):
    def __init__(self):
        super(ContextMenu, self).__init__()
        self._menu = None
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)

    def OnContextMenu(self, event):
        if self._menu is not None:
            self._menu.Destroy()
        item = self.GetSelection()
        label = self.GetItemText(item)
        projects = self.getNamesProjects()
        self._menu = wx.Menu()
        if label in projects:
            self.CreateContextMenuProject(self._menu)
            self.PopupMenu(self._menu)
        elif wx.TreeItemIcon_Expanded == self.GetItemImage(item):
            self.CreateContextMenuGraphics(self._menu)
            self.PopupMenu(self._menu)

    def CreateContextMenuGraphics(self, menu):
        listGraphItems = wx.Menu()
        itemParallelCoord = wx.MenuItem(self._menu, wx.ID_ANY,
                                        u"Coordenadas Paralelas")
        self.Bind(wx.EVT_MENU, self.ShowPlot, itemParallelCoord)
        listGraphItems.AppendItem(itemParallelCoord)
        listGraphItems.Append(wx.ID_ANY, u"Scatter Plot")
        listGraphItems.Append(wx.ID_ANY, u"Heatmap")

        self._menu.AppendMenu(wx.ID_ANY, 'Graficar', listGraphItems)

    def ShowPlot(self, e):
        self.framePrincipal.cuerpoPrincipal.rightPanel.plot()

    def CreateContextMenuProject(self, menu):
        listAddItems = wx.Menu()
        fileResult = wx.MenuItem(self._menu, wx.ID_ANY, u"Archivo Resultado")
        self.Bind(wx.EVT_MENU, self.AddFileResult, fileResult)
        listAddItems.AppendItem(fileResult)

        self._menu.AppendMenu(wx.ID_ANY, 'Agregar', listAddItems)

        itemDelPro = wx.MenuItem(self._menu, wx.ID_ANY, u"Eliminar")
        self.Bind(wx.EVT_MENU, self.DeleteProject, itemDelPro)
        self._menu.AppendItem(itemDelPro)

        itemAddFile = wx.MenuItem(self._menu, wx.ID_EXIT, u"Salir")
        self._menu.AppendItem(itemAddFile)

    def AddFileResult(self, e):
        wildcard = "All files (*)|*"
        dialog = wx.FileDialog(None, "Seleccione los archivos", os.getcwd(),
                               "", wildcard, wx.OPEN | wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            item = self.GetSelection()
#==============================================================================
#             cuerpoPrincipal = self.framePrincipal.cuerpoPrincipal
#             path = cuerpoPrincipal.dictPathProjects[self.GetItemText(item)]
#             + "/RecursosDeUsuario/Resultados"
# #             copyDirOrFile(dialog.GetPaths(), path)
#==============================================================================

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
            idProyecto = self.GetItemPyData(item)
            proPresenter = ProyectoPresenter()
            proyecto = proPresenter.getProjectById(idProyecto)
            projects = self.getNamesProjects()
            del projects[projects.index(proyecto.nombre)]
            proPresenter.delete(proyecto)
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
            newItem = self.AppendItem(parentItem, item.encode('utf8'))
            self.SetItemPyData(newItem, None)
            self.SetItemImage(newItem, self.fileidx, wx.TreeItemIcon_Normal)

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
        self.framePrincipal.Close()


class ArbolProyecto(wx.TreeCtrl, ContextMenu):
    '''
    classdocs
    '''

    def __init__(self, parent, framePrincipal):
        '''
        Constructor
        '''

        super(ArbolProyecto, self).__init__(parent, style=wx.TR_DEFAULT_STYLE |
                                            wx.TR_HIDE_ROOT)
        ContextMenu.__init__(self)

        il = wx.ImageList(16, 16)
        self.fldridx = il.Add(bitmap=wx.Bitmap('icons/folder.png'))
        self.fldropenidx = il.Add(bitmap=wx.Bitmap('icons/folderOpen.png'))
        self.fileidx = il.Add(bitmap=wx.Bitmap('icons/result.png'))

        self.AssignImageList(il)
        self.root = self.AddRoot("Proyectos")
        self.framePrincipal = framePrincipal
        self.OnInitializetree()

    #def AddProjectNode(self, item, idProject):proyecto
    def AddProjectNode(self, proyecto):
        newItem = self.AppendItem(self.root, proyecto.nombre)
        self.SetItemPyData(newItem, proyecto.id)
        self.SetItemImage(newItem, self.fldridx, wx.TreeItemIcon_Normal)
        self.SetItemImage(newItem, self.fldropenidx, wx.TreeItemIcon_Expanded)

        self.SortChildren(self.root)

    def AddTreeNodes(self, parentItem, items):
        for item in items:
            if type(item) == str or type(item) == unicode:
                newItem = self.AppendItem(parentItem, item)
                self.SetItemPyData(newItem, None)
                self.SetItemImage(newItem, self.fileidx,
                                  wx.TreeItemIcon_Normal)
            else:
                newItem = self.AppendItem(parentItem, item[0])
                self.SetItemPyData(newItem, None)
                self.SetItemImage(newItem, self.fldridx,
                                  wx.TreeItemIcon_Normal)
                self.SetItemImage(newItem, self.fldropenidx,
                                  wx.TreeItemIcon_Expanded)

                self.AddTreeNodes(newItem, item[1])

    def OnInitializetree(self):

        proPresenter = ProyectoPresenter()
        for proyecto in proPresenter.getAll():
            self.AddProjectNode(proyecto)
