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
import py.una.pol.tava.view.vimages as I


class ProjectTreeCtrl(CT.CustomTreeCtrl):
    '''
    Clase Arbol que contendra los projectos representados como hijos del arbol
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        super(ProjectTreeCtrl, self).__init__(parent,
                                agwStyle=CT.TR_HAS_BUTTONS | CT.TR_HIDE_ROOT)

        # Definicion del presenter de la clase
        self.presenter = ProjectTreeCtrlPresenter(self)

        # Establecemos el color del fondo del arbol a Blanco
        self.SetBackgroundColour('#FFFFFF')

        # Definicion del listado de imagenes empleadas por el arbol
        il = wx.ImageList(16, 16)
        self.folder_bmp = il.Add(I.folder_png)
        self.folder_open_bmp = il.Add(I.folderOpen_png)
        self.folder_closed_bmp = il.Add(I.folderClosed_png)
        self.file_bmp = il.Add(I.result_png)
        self.AssignImageList(il)

        # Definicion del nodo raiz del arbol
        self.root = self.AddRoot("Projects")

        # Inicializacion del arbol de proyectos
        self.presenter.InitializeTree()

        # Enlace del evento Context a la entidad de Proyecto
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnTreeContextMenu)

        # Enlace del evento de seleccion al metodo OnSelectedItemTree
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectedItemTree)

        # Enlace del evento de expansion de item al metodo OnItemTreeExpanded
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemTreeExpanded)

    def OnSelectedItemTree(self, event):
        self.presenter.SelectedItem()
        #======================================================================
        # item = self.GetSelection()
        # if self.GetItemPyData(item) is not None:
        #     self.presenter.SelectedItem()
        #======================================================================

    def AddProjectOpenNode(self, project):
        project_item = self.AppendItem(self.root, project.name)
        self.SetItemPyData(project_item, project)
        self.SetItemImage(project_item, 0, wx.TreeItemIcon_Normal)
        self.SetItemImage(project_item, 1, wx.TreeItemIcon_Expanded)

        self.SortChildren(self.root)
        return project_item

    def AddProjectCloseNode(self, project):
        project_item = self.AppendItem(self.root, project.name)
        self.SetItemPyData(project_item, project)
        self.SetItemImage(project_item, 2, wx.TreeItemIcon_Normal)
        self.SetItemTextColour(project_item, '#BFBFBF')

        self.SortChildren(self.root)
        return project_item

    # Se reesscribe este metodo
    def OnCompareItems(self, item1, item2):
        return cmp(item1.GetData().state, item2.GetData().state)

    def OnTreeContextMenu(self, event):
        item = self.GetSelection()
        date_item = self.GetItemPyData(item)
        parent_item = self.GetItemParent(item)

        # Verificar si el padre es root
        if(parent_item == self.root):
            menu = ProjectMenu(self, date_item)
        else:
            # Si su padre no es root
            menu = ResultMenu(self, date_item)

        self.PopupMenu(menu)

    def DeleteProjectItem(self, item):
        self.Delete(item)

    def AddResultAProject(self, project_item, result):
        result_item = self.AppendItem(project_item, result.name, ct_type=1)
        self.SetItemPyData(result_item, result)

        self.SortChildren(self.root)

    def OnItemTreeExpanded(self, event):
        item = self.GetSelection()
        date_item = self.GetItemPyData(item)

        if date_item == None:
            return

        if date_item.state == 1:
            self.Collapse(item)


class ProjectMenu(wx.Menu):
    '''
    Clase Menu que estará contenida en un contextMenu de la entidad proyecto
    '''
    def __init__(self, parent, project):
        super(ProjectMenu, self).__init__()

        # Establecemos la referencia al proyecto pasado como parametro
        self.project = project

        # Definicion del presenter de la clase
        self.presentermenu = ProjectMenuPresenter(self)

        # Opcion de menu Nuevo
        new = wx.MenuItem(self, wx.ID_ANY, _(C.PM_NEW))

        # Enlazamos el evento de menu al metodo OnAddFileInProject
        self.Bind(wx.EVT_MENU, self.OnAddFileInProject, new)

        # Agregamos la opcion al arbol
        self.AppendItem(new)
        # Insertamos un separador
        self.AppendSeparator()

        # Opcion de menu Abrir
        open_item = wx.MenuItem(self, wx.ID_ANY, _(C.PM_OPEN))

        # Enlazamos el evento de menu al metodo OnProjectOpen
        self.Bind(wx.EVT_MENU, self.OnProjectOpen, open_item)

        # Agregamos la opcion al arbol
        self.AppendItem(open_item)

        # Opcion de menu Cerrar
        closed_item = wx.MenuItem(self, wx.ID_ANY, _(C.PM_CLOSE))

        # Enlazamos el evento de menu al metodo OnProjectClose
        self.Bind(wx.EVT_MENU, self.OnProjectClose, closed_item)

        # Agregamos la opcion al arbol
        self.AppendItem(closed_item)

        # Opcion de menu Eliminar
        delete_item = wx.MenuItem(self, wx.ID_DELETE, _(C.PM_DEL))

        # Enlazamos el evento de menu al metodo OnProjectDelete
        self.Bind(wx.EVT_MENU, self.OnProjectDelete, delete_item)

        # Agregamos la opcion al arbol
        self.AppendItem(delete_item)

        # Opcion de menu Esconder
        hide_item = wx.MenuItem(self, wx.ID_ANY, _(C.PM_HIDE))

        # Enlazamos el evento de menu al metodo OnProjectHide
        self.Bind(wx.EVT_MENU, self.OnProjectHide, hide_item)

        # Agregamos la opcion al arbol
        self.AppendItem(hide_item)
        # Insertamos un separador
        self.AppendSeparator()

        # Opcion de menu Renombrar
        rename_item = wx.MenuItem(self, wx.ID_ANY, _(C.PM_REN))

        # Enlazamos el evento de menu al metodo OnProjectRename
        self.Bind(wx.EVT_MENU, self.OnProjectRename, rename_item)

        # Insertamos un separador
        self.AppendItem(rename_item)

        # Opcion de menu Propiedades
        properties_item = wx.MenuItem(self, wx.ID_ANY, _(C.PM_PROP))

        # Enlazamos el evento de menu al metodo OnProjectProperties
        self.Bind(wx.EVT_MENU, self.OnProjectProperties, properties_item)

        # Insertamos un separador
        self.AppendItem(properties_item)

        # Si el estado del proyecto es Abierto, se desabilitan las sgtes
        # opciones
        if self.project.state == OPEN:
            open_item.Enable(False)
            hide_item.Enable(False)

        # Si el estado del proyecto es Cerrado, se desabilitan las sgtes
        # opciones
        if self.project.state == CLOSED:
            closed_item.Enable(False)
            rename_item.Enable(False)
            properties_item.Enable(False)

    def OnAddFileInProject(self, event):
        self.presentermenu.AddFileInProject(self.project)

    def OnProjectRename(self, event):
        self.presentermenu.RenameProject(self.project)

    def OnProjectOpen(self, event):
        self.presentermenu.OpenProject()

    def OnProjectClose(self, event):
        self.presentermenu.CloseProject()

    def OnProjectDelete(self, event):
        self.presentermenu.DeleteProject()

    def OnProjectProperties(self, event):
        self.presentermenu.ShowProperties()

    def OnProjectHide(self, event):
        self.presentermenu.HideProject()


class ResultMenu(wx.Menu):
    def __init__(self, parent, result):
        super(ResultMenu, self).__init__()

        self.result = result

        # Definicion de la opcion Graficar
        graficar = wx.MenuItem(self, wx.ID_ANY, 'Graficar')
        # Agregamos la opcion al menu
        self.AppendItem(graficar)
        # Desabilitamos la opcion de menu
        graficar.Enable(False)

        # Agregamos un separador
        self.AppendSeparator()

        # Definicion de la opcion Ver archivo
        ver = wx.MenuItem(self, wx.ID_ANY, 'Ver archivo')
        # Agregamos la opcion al menu
        self.AppendItem(ver)
        # Desabilitamos la opcion de menu
        ver.Enable(False)

        # Definicion de la opcion Renombrar
        rename = wx.MenuItem(self, wx.ID_ANY, 'Renombrar')
        # Agregamos la opcion al menu
        self.AppendItem(rename)
        # Desabilitamos la opcion de menu
        rename.Enable(False)

        # Definicion de la opcion Eliminar
        delete = wx.MenuItem(self, wx.ID_DELETE, 'Eliminar')
        # Agregamos la opcion al menu
        self.AppendItem(delete)
        # Desabilitamos la opcion de menu
        delete.Enable(False)

        # Agregamos un separador
        self.AppendSeparator()

        # Definicion de la opcion Propiedades
        properties = wx.MenuItem(self, wx.ID_ANY, 'Propiedades')
        # Agregamos la opcion al menu
        self.AppendItem(properties)
        # Desabilitamos la opcion de menu
        properties.Enable(False)
