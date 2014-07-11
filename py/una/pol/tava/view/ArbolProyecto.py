'''
Created on 28/05/2014

@author: aferreira
'''

import wx
import os


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
        dicc = self.framePrincipal.cuerpoPrincipal.dictPathProjects
        self._menu = wx.Menu()
        if label in dicc:
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
        itemAddFile = wx.MenuItem(self._menu, wx.ID_EXIT, u"Salir")
        self._menu.AppendItem(itemAddFile)

    def AddFileResult(self, e):
        wildcard = "All files (*)|*"
        dialog = wx.FileDialog(None, "Seleccione los archivos", os.getcwd(),
                               "", wildcard, wx.OPEN | wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            item = self.GetSelection()
            cuerpoPrincipal = self.framePrincipal.cuerpoPrincipal
            path = cuerpoPrincipal.dictPathProjects[self.GetItemText(item)]
            + "/RecursosDeUsuario/Resultados"
#             copyDirOrFile(dialog.GetPaths(), path)

            self.resultados = item
            self.GetResultadosItem(item)
            self.AddNewItemsFiles(self.resultados, dialog.GetFilenames())

        dialog.Destroy()

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

    def OnQuit(self, e):
        self.framePrincipal.Close()


class ArbolProyecto(wx.TreeCtrl, ContextMenu):
    '''
    classdocs
    '''

    def __init__(self, parent):
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

    def setFramePrincipalReference(self, frame):
        self.framePrincipal = frame

    def AddProjectNode(self, parentItem, item):
        newItem = self.AppendItem(parentItem, item)
        self.SetItemPyData(newItem, None)
        self.SetItemImage(newItem, self.fldridx, wx.TreeItemIcon_Normal)
        self.SetItemImage(newItem, self.fldropenidx, wx.TreeItemIcon_Expanded)

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
