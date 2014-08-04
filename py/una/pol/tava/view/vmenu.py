# -*- coding: utf-8 -*-
'''
Created on 27/05/2014

@author: aferreira
'''

import wx
from wx import GetTranslation as _
from py.una.pol.tava.view.vabout import AboutDialog
import py.una.pol.tava.view.vi18n as C


class MainMenuBar(wx.MenuBar):
    '''
    Clase que representa al Menú Principal desplegando las posibles opciones
    de trabajo que pueden utilizarse dentro del área de trabajo.
    '''
    def __init__(self, parent):
        '''
        Constructor para la clase MainMenuBar
        :param parent: referencia a la clase padre de MainMenuBar.
        '''

        super(MainMenuBar, self).__init__()

        # Se inicializan los Menus con sus respectivos MenuItems
        file_menu = wx.Menu()
        new_project_menu_item = wx.MenuItem(file_menu, wx.ID_NEW, _(C.MMB_NP))
        file_menu.AppendItem(new_project_menu_item)
        open_menu_item = wx.MenuItem(file_menu, wx.ID_OPEN, _(C.MMB_OP))
        file_menu.AppendItem(open_menu_item)
        exit_menu_item = wx.MenuItem(file_menu, wx.ID_EXIT, _(C.MMB_EXIT),
                                     '&Quit\tCtrl+Q')
        file_menu.AppendItem(exit_menu_item)

        language_menu = wx.Menu()
        english_language_menu_item = wx.MenuItem(language_menu, wx.ID_ANY,
                                                 _(C.MMB_EN_US_LA))
        language_menu.AppendItem(english_language_menu_item)
        spanish_language_menu_item = wx.MenuItem(language_menu, wx.ID_ANY,
                                                 _(C.MMB_ES_PY_LA))
        language_menu.AppendItem(spanish_language_menu_item)

        help_menu = wx.Menu()
        about_menu_item = wx.MenuItem(help_menu, wx.ID_ABOUT,
                                      _(C.MMB_ABOUT_TAVA), wx.EmptyString,
                                      wx.ITEM_NORMAL)
        help_menu.AppendItem(about_menu_item)

        # Se agrega los Menus al MenuBar Principal
        self.Append(file_menu, _(C.MMB_FILE))
        self.Append(language_menu, _(C.MMB_LANGUAGE))
        self.Append(help_menu, _(C.MMB_HELP))

        parent.Bind(wx.EVT_MENU, parent.OnNewProject, id=wx.ID_NEW)
        parent.Bind(wx.EVT_MENU, parent.OnExitAplication, id=wx.ID_EXIT)
        parent.Bind(wx.EVT_MENU, self.OnAboutBox, id=wx.ID_ABOUT)

    def OnAboutBox(self, e):
        '''
        Método que inicializa la clase que representa al panel "Acerca de".
        :param e: evento de selección de Menú.
        '''
        AboutDialog()
