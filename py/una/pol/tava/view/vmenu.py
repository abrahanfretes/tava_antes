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
from py.una.pol.tava.presenter.pmenu import AnalysisPackageMenuPresenter
from py.una.pol.tava.presenter.pmenu import AnalysisMenuPresenter
from py.una.pol.tava.presenter.pprojectmenu import ProjectMenuPresenter
from py.una.pol.tava.presenter.pprojectmenu import ResultPackageMenuPresenter
from py.una.pol.tava.presenter.pprojectmenu import\
    MetricsFilesPackageMenuPresenter
from py.una.pol.tava.presenter.pprojectmenu import\
    MetricsViewsPackageMenuPresenter
import vconstants as vc

from py.una.pol.tava.base import tavac as tvc


# ------ menu principal -------------------------------------------------------

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

# --------------------------------------------------------------

# ------ menu llamados desde el arbol (vtree) ---------------------------------


# ------ menu para proyecto ---------------------------------------------------
class ProjectMenu(wx.Menu):
    '''
    Clase Menu que estará contenida en un contextMenu de la entidad proyecto
    '''
    def __init__(self, parent, project):
        super(ProjectMenu, self).__init__()

        # ------ definiciones iniciales ---------------------------------------

        self.project = project
        self.presentermenu = ProjectMenuPresenter(self)

        self.InitUI()
        # ----------------------------------------------------

    def InitUI(self):

        # ------ items del menu ----------------------------------------

        # Opcion de menu agregar archivo
        self.add_file = wx.MenuItem(self, wx.ID_ANY, _(C.PM_NEW))
        self.AppendItem(self.add_file)
        self.Bind(wx.EVT_MENU, self.OnAddFileInProject, self.add_file)

        self.AppendSeparator()

        # Opcion de menu Abrir
        self.open_item = wx.MenuItem(self, wx.ID_ANY, _(C.PM_OPEN))
        self.AppendItem(self.open_item)
        self.Bind(wx.EVT_MENU, self.OnProjectOpen, self.open_item)

        # Opcion de menu Cerrar
        self.closed_item = wx.MenuItem(self, wx.ID_ANY, _(C.PM_CLOSE))
        self.AppendItem(self.closed_item)
        self.Bind(wx.EVT_MENU, self.OnProjectClose, self.closed_item)

        # Opcion de menu Eliminar
        self.delete_item = wx.MenuItem(self, wx.ID_DELETE, _(C.PM_DEL))
        self.AppendItem(self.delete_item)
        self.Bind(wx.EVT_MENU, self.OnProjectDelete, self.delete_item)

        # Opcion de menu Esconder
        self.hide_item = wx.MenuItem(self, wx.ID_ANY, _(C.PM_HIDE))
        self.AppendItem(self.hide_item)
        self.Bind(wx.EVT_MENU, self.OnProjectHide, self.hide_item)

        self.AppendSeparator()

        # Opcion de menu Renombrar
        self.rename_item = wx.MenuItem(self, wx.ID_ANY, _(C.PM_REN))
        self.AppendItem(self.rename_item)
        self.Bind(wx.EVT_MENU, self.OnProjectRename, self.rename_item)

        # Opcion de menu Propiedades
        self.properties_item = wx.MenuItem(self, wx.ID_ANY, _(C.PM_PROP))
        self.AppendItem(self.properties_item)
        self.Bind(wx.EVT_MENU, self.OnProjectProperties, self.properties_item)

        self.presentermenu.InitialEnableItem()
        # ----------------------------------------------------

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

# ---------------------------------------------------


# ----- menu para el paquete de resultado -------------------------------------
class ResultPackageMenu(wx.Menu):
    def __init__(self, parent, project):
        super(ResultPackageMenu, self).__init__()

        # ------ definiciones iniciales ---------------------------------------
        self.project = project
        self.presentermenu = ResultPackageMenuPresenter(self)

        self.InitUI()
        # ----------------------------------------------------

    def InitUI(self):

        # ------ items del menu ----------------------------------------

        # menu agregar archivo
        self.add_file = wx.MenuItem(self, wx.ID_ANY, _(C.PM_NEW))
        self.AppendItem(self.add_file)
        self.Bind(wx.EVT_MENU, self.OnAddFileInProject, self.add_file)

        self.AppendSeparator()
        # ----------------------------------------------------

    def OnAddFileInProject(self, event):
        self.presentermenu.AddFileInProject(self.project)

# ----------------------------------------------------


# ----- menu para el paquete de analisis --------------------------------------
class AnalysisPackageMenu(wx.Menu):
    def __init__(self, parent, analysis_package):
        super(AnalysisPackageMenu, self).__init__()

        self.presentermenu = AnalysisPackageMenuPresenter(self)

        # ------ definiciones iniciales ---------------------------------------

        self.package = analysis_package
        self.InitUI()
        # ----------------------------------------------------

    def InitUI(self):

        # ------ items del menu ----------------------------------------

        # menu agregar analisis a proyecto
        new_analise = wx.MenuItem(self, wx.ID_ANY, 'Nuevo Analisis')
        self.AppendItem(new_analise)
        self.Bind(wx.EVT_MENU, self.OnShowGraphicWizard, new_analise)

    def OnShowGraphicWizard(self, event):
        self.presentermenu.ShowGraphicWizard()
        # ----------------------------------------------------
# ----------------------------------------------------


# ------ menu para resultados -------------------------------------------------
class ResultMenu(wx.Menu):
    def __init__(self, parent, result):
        super(ResultMenu, self).__init__()

        # ------ definiciones iniciales ---------------------------------------

        self.result = result
        self.InitUI()
        # ----------------------------------------------------

    def InitUI(self):

        # ------ items del menu ----------------------------------------

        # menu ver archivo
        ver = wx.MenuItem(self, wx.ID_ANY, 'Ver archivo')
        self.AppendItem(ver)
        ver.Enable(False)

        # menu renombrar archivo
        rename = wx.MenuItem(self, wx.ID_ANY, 'Renombrar')
        self.AppendItem(rename)
        rename.Enable(False)

        # menu borrar archivo
        delete = wx.MenuItem(self, wx.ID_DELETE, 'Eliminar')
        self.AppendItem(delete)
        delete.Enable(False)

        self.AppendSeparator()

        # menu propiedad del archivo
        properties = wx.MenuItem(self, wx.ID_ANY, 'Propiedades')
        self.AppendItem(properties)
        properties.Enable(False)
# ----------------------------------------------------


# ----- menu para analisis ----------------------------------------------------
class AnalysisMenu(wx.Menu):
    def __init__(self, parent, test):
        super(AnalysisMenu, self).__init__()

        # ------ definiciones iniciales ---------------------------------------
        self.presenter_menuanalizer = AnalysisMenuPresenter(self)

        self.test = test
        self.InitUI()
        # ----------------------------------------------------

    def InitUI(self):

        # ------ items del menu ----------------------------------------

        som_graphic = wx.MenuItem(self, wx.ID_ANY, 'Self Organizing Maps')
        self.AppendItem(som_graphic)
        som_graphic.Enable(True)
        self.Bind(wx.EVT_MENU, self.OnShowSomGraphic, som_graphic)
        self.AppendSeparator()

        # menu only_graphics resultado
        only_graphics = wx.MenuItem(self, wx.ID_ANY,
                                    'Gráficos de Coordenadas Paralelas')
        self.AppendItem(only_graphics)
        only_graphics.Enable(True)
        self.Bind(wx.EVT_MENU, self.OnShowGraphic, only_graphics)
        self.AppendSeparator()

        graphs_and_data = wx.MenuItem(self, wx.ID_ANY,
                                      'Analisis de Coordenadas Paralelas')
        self.AppendItem(graphs_and_data)
        graphs_and_data.Enable(True)
        self.Bind(wx.EVT_MENU, self.OnShowGraphsAndData, graphs_and_data)
        self.AppendSeparator()

        scatter_matrix_graphic = wx.MenuItem(self, wx.ID_ANY, 'Scatter Matrix')
        self.AppendItem(scatter_matrix_graphic)
        scatter_matrix_graphic.Enable(True)
        self.Bind(wx.EVT_MENU, self.OnShowScatterMatrixGraphic,
                  scatter_matrix_graphic)
        self.AppendSeparator()

        andrews_curves = wx.MenuItem(self, wx.ID_ANY, 'Andrews Curves')
        self.AppendItem(andrews_curves)
        andrews_curves.Enable(True)
        self.Bind(wx.EVT_MENU, self.OnShowAndrewsCurves, andrews_curves)

        box_plot = wx.MenuItem(self, wx.ID_ANY, 'Box Plot')
        self.AppendItem(box_plot)
        box_plot.Enable(True)
        self.Bind(wx.EVT_MENU, self.OnShowBoxPlot, box_plot)

    def OnShowGraphic(self, event):
        self.presenter_menuanalizer.\
            ShowGraphic(tvc.MODE_PARALLEL_COORDINATES_GF)

    def OnShowGraphsAndData(self, event):
        self.presenter_menuanalizer.\
            OnShowGraphsAndData(tvc.MODE_PARALLEL_COORDINATES_AL)

    def OnShowAndrewsCurves(self, event):
        self.presenter_menuanalizer.\
            OnShowGraphsAndData(tvc.MODE_ANDREWS_CURVES)

    def OnShowBoxPlot(self, event):
        self.presenter_menuanalizer.\
            OnShowGraphsAndData(tvc.MODE_BOX_PLOT)

    def OnShowSomGraphic(self, event):
        self.presenter_menuanalizer.ShowGraphic(vc.SOM)

    def OnShowScatterMatrixGraphic(self, event):
        self.presenter_menuanalizer.ShowGraphic(vc.SCATTER_MATRIX)


# ------ menu para el paquete de metricas files -------------------------------
class MetricsFilesPackageMenu(wx.Menu):
    def __init__(self, parent, project):
        super(MetricsFilesPackageMenu, self).__init__()

        self.project = project
        self.presentermenu = MetricsFilesPackageMenuPresenter(self)

        # menu agregar archivo
        self.add_file = wx.MenuItem(self, wx.ID_ANY, _(C.PM_NEW))
        self.AppendItem(self.add_file)
        # self.Bind(wx.EVT_MENU, self.OnAddFileInProject, self.add_file)

        self.AppendSeparator()
        # ----------------------------------------------------

    def OnAddFileInProject(self, event):
        self.presentermenu.AddFileInProject(self.project)


# ----- menu para el paquete de metricas views --------------------------------
class MetricsViewsPackageMenu(wx.Menu):
    def __init__(self, parent, project):
        super(MetricsViewsPackageMenu, self).__init__()

        self.project = project
        self.presentermenu = MetricsViewsPackageMenuPresenter(self)

        # menu agregar archivo
        self.add_file = wx.MenuItem(self, wx.ID_ANY, _(C.PM_NEW))
        self.AppendItem(self.add_file)
        # self.Bind(wx.EVT_MENU, self.OnAddFileInProject, self.add_file)

        self.AppendSeparator()
        # ----------------------------------------------------

    def OnAddFileInProject(self, event):
        self.presentermenu.AddFileInProject(self.project)
