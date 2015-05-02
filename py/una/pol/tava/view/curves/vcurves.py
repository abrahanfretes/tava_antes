#  -*- coding: utf-8 -*-
'''
Created on 1/5/2015

@author: abrahan
'''
import wx
from wx import GetTranslation as _

from py.una.pol.tava.view import vi18n as C
from py.una.pol.tava.view import vimages as I
from py.una.pol.tava.presenter.pandrews_curves.pcurves\
    import CurvesTreePresenter


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


class CurvesTree(CT.CustomTreeCtrl):
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
        self.presenter = CurvesTreePresenter(self, test)
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

from py.una.pol.tava.presenter.pandrews_curves.pcurves\
    import CurvesFigurePresenter
from py.una.pol.tava.presenter.pandrews_curves.pcurves\
    import ButtonsExecutionPresenter


# ------------------- Panel Para Grafico De Coordenadas Paralelas -------------
# -------------------                                  ------------------------
class CurvesFigure(wx.Panel):
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

        self.presenter = CurvesFigurePresenter(self, test)

        self.toolbar.Realize()
        self.button_tolbar = TollBarFigure(self, self.presenter.
                                           getAdrewsCurves())

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

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(buttons_ejecution)
        sizer.Add(s_line_update, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=4)
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
