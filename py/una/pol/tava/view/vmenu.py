# -*- coding: utf-8 -*-
'''
Created on 27/05/2014

@author: aferreira
'''

import wx
from wx import GetTranslation as _
from py.una.pol.tava.view.vabout import AboutDialog
import py.una.pol.tava.view.vi18n as C
from py.una.pol.tava.presenter.pmenu import MainMenuBarPresenter


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

        self.presenter = MainMenuBarPresenter(self)

        # Se inicializa el menu de Archivo
        file_menu = wx.Menu()

        # MenuItem Nuevo Proyecto
        self.new_project_menu_item = wx.MenuItem(file_menu, wx.ID_NEW)
        parent.Bind(wx.EVT_MENU, parent.OnProjectNew, id=wx.ID_NEW)
        file_menu.AppendItem(self.new_project_menu_item)

        # MenuItem Abrir Proyecto
        self.open_menu_item = wx.MenuItem(file_menu, wx.ID_OPEN)
        file_menu.AppendItem(self.open_menu_item)

        # MenuItem Propiedades
        self.properties_item = wx.MenuItem(file_menu, wx.ID_PROPERTIES)
        file_menu.Bind(wx.EVT_MENU, self.OnPropertiesShow,
                  self.properties_item)
        file_menu.AppendItem(self.properties_item)

        # MenuItem Salir de Aplicacion
        self.exit_menu_item = wx.MenuItem(file_menu, wx.ID_EXIT,
                                          '&Quit\tCtrl+Q')
        parent.Bind(wx.EVT_MENU, parent.OnApplicationExit, id=wx.ID_EXIT)
        file_menu.AppendItem(self.exit_menu_item)

        # Menu de Lenguajes
        language_menu = wx.Menu()

        # MenuItem del idioma Ingles
        self.english_language_menu_item = wx.MenuItem(language_menu,
                                                      wx.ID_ANY, " ")
        language_menu.Bind(wx.EVT_MENU, self.OnEnglishLanguageSelect,
                  self.english_language_menu_item)
        language_menu.AppendItem(self.english_language_menu_item)

        # MenuItem del idioma Espanhol
        self.spanish_language_menu_item = wx.MenuItem(language_menu,
                                                 wx.ID_ANY, " ")
        language_menu.Bind(wx.EVT_MENU, self.OnSpanishLanguageSelect,
                  self.spanish_language_menu_item)
        language_menu.AppendItem(self.spanish_language_menu_item)

        # Menu de Ayuda
        help_menu = wx.Menu()

        # MenuItem Acerca De
        self.about_menu_item = wx.MenuItem(help_menu, wx.ID_ABOUT)
        parent.Bind(wx.EVT_MENU, self.OnAboutBox, id=wx.ID_ABOUT)
        help_menu.AppendItem(self.about_menu_item)

        # Se agrega los Menus al MenuBar Principal
        self.Append(file_menu, _(C.MMB_FILE))
        self.Append(language_menu, _(C.MMB_LANGUAGE))
        self.Append(help_menu, _(C.MMB_HELP))

        # Establecemos los labels de los componentes
        self.SetLabels()

    def OnEnglishLanguageSelect(self, e):
        self.presenter.SelectEnglishLanguage()

    def OnSpanishLanguageSelect(self, e):
        self.presenter.SelectSpanishLanguage()

    def OnPropertiesShow(self, e):
        self.presenter.ShowProperties()

    def OnAboutBox(self, e):
        '''
        Método que inicializa la clase que representa al panel "Acerca de".
        :param e: evento de selección de Menú.
        '''
        AboutDialog()

    def SetLabels(self):
        # Menu Archivo y sus items
        self.SetMenuLabel(0, _(C.MMB_FILE))
        self.new_project_menu_item.SetText(_(C.MMB_NP))
        self.open_menu_item.SetText(_(C.MMB_OP))
        key_accelerator = '&' + _(C.MMB_PROP) + '\tAlt+Enter'
        self.properties_item.SetText(key_accelerator)
        self.exit_menu_item.SetText(_(C.MMB_EXIT))

        # Menu Idioma y sus items
        self.SetMenuLabel(1, _(C.MMB_LANGUAGE))
        self.english_language_menu_item.SetText(_(C.MMB_EN_US_LA))
        self.spanish_language_menu_item.SetText(_(C.MMB_ES_PY_LA))

        # Menu Ayuda y sus items
        self.SetMenuLabel(2, _(C.MMB_HELP))
        self.about_menu_item.SetText(_(C.MMB_ABOUT_TAVA))
