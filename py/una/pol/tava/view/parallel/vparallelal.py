#  -*- coding: utf-8 -*-
'''
Created on 9/4/2015

@author: abrahan
'''

import wx
from wx import GetTranslation as _

from py.una.pol.tava.view import vi18n as C
from py.una.pol.tava.view import vimages as I


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Sección encargada de los componentes Visuales (views) para ParallelTreeAL.
# Maneja los eventos sobre el arbol de iteraciones.
# -> checket
# -> unchecket
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# ------------------- Arbol de Archvivos e Iteraciones ------------------------
# -------------------                                  ------------------------
import wx.lib.agw.customtreectrl as CT

from py.una.pol.tava.presenter.pparallel.pparallelal import ParallelTreeALPresenter


class ParallelTreeAL(CT.CustomTreeCtrl):
    def __init__(self, parent, test):
        CT.CustomTreeCtrl.__init__(self, parent, agwStyle=CT.TR_HIDE_ROOT)

        # ------ self customize ---------------------------------------
        il = wx.ImageList(16, 16)
        il.Add(I.filegraph_png)
        il.Add(I.arrow_bullet_right)
        il.Add(I.arrow_grey_right)
        self.AssignImageList(il)

        # ------ self components --------------------------------------
        self.parent = parent

        self.presenter = ParallelTreeALPresenter(self, test)

        # ------ self inicailes executions ----------------------------
        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnChecked)

    # ------ self controls -------------------------------------------
    def OnChecked(self, event):
        self.presenter.setChecked()
        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        # ------ self inicailes executions ----------------------------
    # ------ self controls --------------------------------------------

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Sección encargada de los componentes Visuales (views) para Figura Coordenadas
# Paralelas:
# -> ParallelFigureAL
# -> TollBarFigure
# -> ButtonsEjecution
# -> ButtonsConfig
# -> ButtonsFilter
# Maneja las acciones de los cuatro componentes que contiene el TollBar
# -> Graficar
# -> Configurar
# -> Actualizar Filtros
# -> Limpiar Filtros
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar


from py.una.pol.tava.presenter.pparallel.pparallelal import ParallelFigureALPresenter
from py.una.pol.tava.presenter.pparallel.pparallelal import ButtonsExecutionPresenter
from py.una.pol.tava.presenter.pparallel.pparallelal import ButtonsConfigPresenter
from py.una.pol.tava.presenter.pparallel.pparallelal import ButtonsFilterPresenter
from py.una.pol.tava.view.parallel.vparallelconal import ConfigurationParallelFigure


# ------------------- Panel Para Grafico De Coordenadas Paralelas -------------
# -------------------                                  ------------------------
class ParallelFigureAL(wx.Panel):
    '''
    Clase Panel que contiene la configuracion para la visualizacion del
    componente de coordenadas paralelas.
    '''
    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        self.parent = parent
        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)

        self.presenter = ParallelFigureALPresenter(self, test)

        self.toolbar.Realize()
        self.button_tolbar = TollBarFigure(self, self.presenter.
                                           getParallelAnalizer())

        self.sizer_toll = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_toll.Add(self.button_tolbar, 4)
        self.sizer_toll.Add(self.toolbar, 1)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer_toll, 0, wx.LEFT | wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

        # ------ self inicailes executions ----------------------------

    # ------ self controls --------------------------------------------
    def showNewFigure(self, ite_list):
        self.presenter.newFigureTest(ite_list)

    def cleanFilter(self):
        self.parent.cleanFilter()


# ------------------- Panel De Control De Configuracion      ------------------
# -------------------                                  ------------------------
class TollBarFigure(wx.Panel):
    def __init__(self, parent, pa):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
        background = pa.colors_backgrounds.split(',')[2]
        self.SetBackgroundColour(background)

        # ------ self components --------------------------------------
        self.parent = parent

        buttons_ejecution = ButtonsEjecution(self, background)
        s_line_update = wx.StaticLine(self, style=wx.LI_VERTICAL)
        buttons_configuration = ButtonsConfiguration(self, pa)
        s_line = wx.StaticLine(self, style=wx.LI_VERTICAL)
        buttons_filter = ButtonsFilter(self, background)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(buttons_ejecution)
        sizer.Add(s_line_update, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=4)
        sizer.Add(buttons_filter)
        sizer.Add(s_line, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=4)
        sizer.Add(buttons_configuration)

        self.SetSizer(sizer)


# ------------------- Clase contenedor de Botones para Ejecución      ---------
# -------------------                                  ------------------------
class ButtonsEjecution(wx.Panel):
    def __init__(self, parent, background):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
        self.SetBackgroundColour(background)

        # ------ self components --------------------------------------
        self.execution = wx.BitmapButton(self, -1, I.graficar_parallel,
                                         style=wx.NO_BORDER)
        self.execution.SetToolTipString(_(C.BTF_UF))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.execution, 1, wx.LEFT, border=10)
        self.SetSizer(sizer)

        self.presenter = ButtonsExecutionPresenter(self)
        # ------ self inicailes executions ----------------------------
        self.Bind(wx.EVT_BUTTON, self.OnClickExecution, self.execution)

    # ------ self controls --------------------------------------------
    def OnClickExecution(self, event):
        self.presenter.verifyTreeCheckeo()

    def enableButtons(self):
        self.execution.Enable()

    def disableButtons(self):
        self.execution.Disable()


# ------------------- Clase contenedor de Botones para Configuración-----------
# -------------------                                  ------------------------
class ButtonsConfiguration(wx.Panel):
    def __init__(self, parent, pa):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
        self.SetBackgroundColour(pa.colors_backgrounds.split(',')[2])

        # ------ self components --------------------------------------
        self.config = wx.BitmapButton(self, -1, I.update_config,
                                      style=wx.NO_BORDER)
        self.config.SetToolTipString(_(C.BTF_NC))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.config, 1, wx.LEFT, border=10)
        self.SetSizer(sizer)

        self.presenter = ButtonsConfigPresenter(self, pa)

        # ------ self inicailes executions ----------------------------
        self.Bind(wx.EVT_BUTTON, self.OnClickConfiguration, self.config)

    # ------ self controls --------------------------------------------
    def OnClickConfiguration(self, event):
        pa = self.presenter.getParallelAnalizer()
        ConfigurationParallelFigure(self, pa)

    def enableButtons(self):
        self.config.Enable()

    def disableButtons(self):
        self.config.Disable()


# ------------------- Clase contenedor de Botones para Filtros      -----------
# -------------------                                  ------------------------
class ButtonsFilter(wx.Panel):
    def __init__(self, parent, background):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
        self.SetBackgroundColour(background)

        # ------ self components --------------------------------------

        self.update_filters = wx.BitmapButton(self, -1, I.update_figure,
                                              style=wx.NO_BORDER)
        self.update_filters.SetToolTipString(_(C.BTF_ESF))

        self.clean = wx.BitmapButton(self, -1, I.clear_filters,
                                     style=wx.NO_BORDER)
        self.clean.SetToolTipString(_(C.BTF_CF))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.update_filters, 1, wx.LEFT, border=10)
        sizer.Add(self.clean, 1, wx.LEFT, border=10)
        self.SetSizer(sizer)

        self.presenter = ButtonsFilterPresenter(self)

        # ------ self inicailes executions ----------------------------
        self.Bind(wx.EVT_BUTTON, self.OnFilterObjetive, self.update_filters)
        self.Bind(wx.EVT_BUTTON, self.OnCleanFilter, self.clean)

    # ------ self controls --------------------------------------------

    def OnFilterObjetive(self, event):
        self.presenter.setFilters()

    def OnCleanFilter(self, event):
        self.presenter.cleanFilter()

    def enableButtons(self):
        self.update_filters.Enable()
        self.clean.Enable()

    def disableButtons(self):
        self.update_filters.Disable()
        self.clean.Disable()

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Sección encargada de los componentes Visuales (views) para Tab del
# BottomPanel:
# -> TabVariables
# -> TabObjectives
# -> TabFiltros
# -> FilterObjetives

# Maneja los eventos de cambios realizados en el TabFiltros

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
from wx import dataview as dv
from wx.lib.scrolledpanel import ScrolledPanel

from py.una.pol.tava.presenter.pparallel.pparallelal import TabVariablesPresenter
from py.una.pol.tava.presenter.pparallel.pparallelal import TabObjectivesPresenter
from py.una.pol.tava.presenter.pparallel.pparallelal import TabFiltrosPresenter


# ------------------- Clase contenedor para Tab de Variables  -----------------
# -------------------                                  ------------------------
class TabVariables(ScrolledPanel):
    def __init__(self, parent, test):
        ScrolledPanel.__init__(self, parent, -1)

        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        self.parent = parent
        self.InitUI()
        self.presenter = TabVariablesPresenter(self, test)

    def InitUI(self):

        l_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dvlc = dv.DataViewListCtrl(self)
        l_sizer.Add(self.dvlc, 1, flag=wx.EXPAND)

        self.SetSizer(l_sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        # ------ self inicailes executions ----------------------------
    # ------ self controls --------------------------------------------


# ------------------- Clase contenedor para Tab de Objetivos  -----------------
# -------------------                                  ------------------------
class TabObjectives(ScrolledPanel):
    def __init__(self, parent, test):
        ScrolledPanel.__init__(self, parent, -1)

        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        self.parent = parent
        self.InitUI()
        self.presenter = TabObjectivesPresenter(self, test)

    def InitUI(self):
        l_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dvlc = dv.DataViewListCtrl(self)
        l_sizer.Add(self.dvlc, 1, flag=wx.EXPAND)

        self.SetSizer(l_sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        # ------ self inicailes executions ----------------------------
    # ------ self controls --------------------------------------------


# ------------------- Clase contenedor para Tab de Filtros  -------------------
# -------------------                                  ------------------------
class TabFilters(ScrolledPanel):
    def __init__(self, parent, test):
        ScrolledPanel.__init__(self, parent, -1)

        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        self.parent = parent
        self.presenter = TabFiltrosPresenter(self, test)

        # toll = ButtonsFilter(self)

        self.sizer_f = wx.BoxSizer(wx.HORIZONTAL)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        # self.sizer.Add(toll, 1, wx.ALIGN_LEFT)
        self.sizer.Add(self.sizer_f, 1, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

        # ------ self inicailes executions ----------------------------

    # ------ self controls --------------------------------------------
    def addItem(self, vmin, vmax, nobj, min_v_r, max_v_r):
        value = FilterObjetives(self, vmin, vmax, nobj, min_v_r, max_v_r)
        self.sizer_f.Add(value, 1, flag=wx.EXPAND)
        return value

    def addSiserHere(self):
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        # self.parent.SetAutoLayout(1)


# ------------------- Clase para Filtros  Individual   ------------------------
# -------------------                                  ------------------------
class FilterObjetives(wx.Panel):
    def __init__(self, parent, vmin, vmax, nobj, min_v_r, max_v_r):
        wx.Panel.__init__(self, parent=parent)

        # ------ self customize ---------------------------------------

        # ------ self components --------------------------------------
        self.parent = parent
        self.min_value_r = float(min_v_r)
        self.max_value_r = float(max_v_r)
        self.min_value = float(vmin)
        self.max_value = float(vmax)
        self.name_objetive = nobj
        self.len_digits = self.__getLengDigits()

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        s_line = wx.StaticLine(self)
        font_title = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font_title.SetPointSize(10)
        title = wx.StaticText(self, label=self.name_objetive, style=2)
        title.SetFont(font_title)

        line = wx.StaticLine(self)

        sizer_value_absolute = wx.BoxSizer(wx.VERTICAL)
        min_value = wx.StaticText(self, label='min: ' + str(self.min_value_r))
        sizer_value_absolute.Add(min_value, 1, flag=wx.EXPAND)
        max_value = wx.StaticText(self, label='max: ' + str(self.max_value_r))
        sizer_value_absolute.Add(max_value, 1, flag=wx.EXPAND)
        line_s = wx.StaticLine(self)
        sizer_value_absolute.Add(line_s, 1, flag=wx.EXPAND)

        sizer_in_min = wx.BoxSizer(wx.VERTICAL)

        self.min_spin = wx.SpinCtrlDouble(self, initial=self.min_value,
                                          min=self.min_value_r,
                                          max=self.max_value_r, size=(30, -1),
                                          inc=0.01)
        self.min_spin.SetDigits(self.len_digits)

        sizer_in_min.Add(self.min_spin, 1, flag=wx.EXPAND)

        sizer_in_max = wx.BoxSizer(wx.VERTICAL)

        self.max_spin = wx.SpinCtrlDouble(self, initial=self.max_value,
                                          min=self.min_value_r,
                                          max=self.max_value_r, size=(30, -1),
                                          inc=0.01)
        self.max_spin.SetDigits(self.len_digits)

        sizer_in_max.Add(self.max_spin, 1, flag=wx.EXPAND)

        sizer.Add(s_line, 0.5, flag=wx.EXPAND | wx.TOP, border=5)
        sizer.Add(title, 0.5, flag=wx.ALIGN_CENTER)
        sizer.Add(line, 0.5, flag=wx.EXPAND)

        sizer.Add(sizer_in_min, 1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
                  border=5)
        sizer.Add(sizer_in_max, 1, flag=wx.EXPAND | wx.BOTTOM, border=10)
        sizer.Add(sizer_value_absolute, 0.5, flag=wx.EXPAND)

        line_ver1 = wx.StaticLine(self, style=wx.LI_VERTICAL)
        sizer_main.Add(line_ver1, 0.1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
                       border=5)
        sizer_main.Add(sizer, 1, flag=wx.EXPAND)
        line_ver = wx.StaticLine(self, style=wx.LI_VERTICAL)
        sizer_main.Add(line_ver, 0.1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
                       border=5)

        self.SetSizer(sizer_main)

        # ------ self inicailes executions ----------------------------

    # ------ self controls --------------------------------------------
    def __getLengDigits(self):
        if len(str(self.min_value_r)) > len(str(self.max_value_r)):
            return len(str(self.min_value_r)) - 2
        return len(str(self.max_value_r)) - 2

    def getObjectValues(self):
        return [self.min_spin.GetValue(), self.max_spin.GetValue()]

    def getMinValue(self):
        return self.min_spin.GetValue()

    def getMaxValue(self):
        return self.max_spin.GetValue()

    def getLengDigits(self, min_v, max_v):
        if len(str(min_v)) > len(str(max_v)):
            return len(str(min)) - 2
        return len(str(max)) - 2

    def setValues(self, vmin, vmax):
        self.min_spin.SetValue(float(vmin))
        self.max_spin.SetValue(float(vmax))
