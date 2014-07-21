# -*- coding: utf-8 -*-
'''
Created on 27/05/2014

@author: aferreira
'''

import wx
from wx import GetTranslation as _
import AcercaDe

MP_NP = "MENU_PRINCIPAL_NUEVO_PROYECTO"
MP_AP = "MENU_PRINCIPAL_ABRIR_PROYECTO"
MP_EXIT = "MENU_PRINCIPAL_SALIR"
MP_FILE = "MENU_PRINCIPAL_ARCHIVO"
MP_ABOUT_TAVA = "MENU_PRINCIPAL_ACERCA_TAVA"
MP_HELP = "MENU_PRINCIPAL_AYUDA"


class MenuPrincipal(wx.MenuBar):
    '''
    Clase que representa al Menú Principal desplegando las posibles opciones
    de trabajo que pueden utilizarse dentro del área de trabajo.
    '''
    def __init__(self, parent):
        '''
        Constructor para la clase MenuPrincipal
        :param parent: referencia a la clase padre de MenuPrincipal.
        '''

        super(MenuPrincipal, self).__init__()

        # Se inicializan los Menus con sus respectivos MenuItems
        archivo = wx.Menu()
        nuevoProyecto = wx.MenuItem(archivo, wx.ID_NEW, _(MP_NP))
        archivo.AppendItem(nuevoProyecto)
        abrir = wx.MenuItem(archivo, wx.ID_OPEN, _(MP_AP))
        archivo.AppendItem(abrir)
        salir = wx.MenuItem(archivo, wx.ID_EXIT, _(MP_EXIT), '&Quit\tCtrl+Q')
        archivo.AppendItem(salir)

        ayuda = wx.Menu()
        about = wx.MenuItem(ayuda, wx.ID_ABOUT, _(MP_ABOUT_TAVA),
        wx.EmptyString, wx.ITEM_NORMAL)
        ayuda.AppendItem(about)

        # Se agrega los Menus al MenuBar Principal
        self.Append(archivo, _(MP_FILE))
        self.Append(ayuda, _(MP_HELP))

        self.Bind(wx.EVT_MENU, parent.OnNuevoProyecto, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, parent.OnExitAplication, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAboutBox, id=wx.ID_ABOUT)

    def OnAboutBox(self, e):
        '''
        Método que inicializa la clase que representa al panel "Acerca de".
        :param e: evento de selección de Menú.
        '''
        AcercaDe.AcercaDe()
