# -*- coding: utf-8 -*-
'''
Created on 27/05/2014

@author: aferreira
'''

import wx
import AcercaDe
import NuevoProyecto
from wx import GetTranslation as _

MP_ABOUT = 1
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

        self.archivo = wx.Menu()

        self.nuevoProyecto = wx.MenuItem(self.archivo, wx.ID_NEW,
                                         _(MP_NP))
        parent.Bind(wx.EVT_MENU, self.OnNuevoProyecto, id=wx.ID_NEW)
        self.archivo.AppendItem(self.nuevoProyecto)

        self.abrir = wx.MenuItem(self.archivo, wx.ID_OPEN, _(MP_AP))
        self.archivo.AppendItem(self.abrir)

        self.salir = wx.MenuItem(self.archivo, wx.ID_EXIT, _(MP_EXIT),
                                 '&Quit\tCtrl+Q')
        self.archivo.AppendItem(self.salir)

        parent.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)

        self.Append(self.archivo, _(MP_FILE))

        self.ayuda = wx.Menu()
        self.about = wx.MenuItem(self.ayuda, MP_ABOUT, _(MP_ABOUT_TAVA),
                                 wx.EmptyString, wx.ITEM_NORMAL)
        parent.Bind(wx.EVT_MENU, self.OnAboutBox, id=MP_ABOUT)
        self.ayuda.AppendItem(self.about)

        self.Append(self.ayuda, _(MP_HELP))

    def OnAboutBox(self, e):
        '''
        Método que inicializa la clase que representa al panel "Acerca de".
        :param e: evento de selección de Menú.
        '''
        AcercaDe.AcercaDe()

    def OnNuevoProyecto(self, e):
        '''
        Método que inicializa la clase de creación de un Nuevo Proyecto.
        :param e: evento de selección de Menú.
        '''
        NuevoProyecto.NuevoProyecto(self.Parent)

    def OnQuit(self, e):
        '''
        Método invocado para cerrar el Frame Principal a través de una
        referencia al padre.
        :param e: evento de selección de Menú.
        '''
        self.Parent.Close()
