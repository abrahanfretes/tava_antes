#  -*- coding: utf-8 -*-
'''
Created on 2/5/2015

@author: abrahan
'''
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from wx import GetTranslation as _

from py.una.pol.tava.view import vi18n as C
from py.una.pol.tava.view import vimages as I
from py.una.pol.tava.presenter.pandrews_curves.pfigurecurves\
    import CurvesFigurePresenter


# ------------------- Panel Para Grafico De Coordenadas Paralelas -------------
# -------------------                                  ------------------------
class CurvesFigure(wx.Panel):
    '''
    Clase Panel que contiene la configuracion para la visualizacion del
    componente de coordenadas paralelas.
    '''
    def __init__(self, parent, page_curves, test):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        self.parent = parent
        self.page_curves = page_curves

        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()

        self.button_execution = wx.BitmapButton(self, -1, I.graficar_parallel,
                                                style=wx.NO_BORDER)
        self.button_execution.SetToolTipString(_(C.BTF_UF))
        s_line_update = wx.StaticLine(self, style=wx.LI_VERTICAL)
        self.update_filters = wx.BitmapButton(self, -1, I.update_figure,
                                              style=wx.NO_BORDER)
        self.update_filters.SetToolTipString(_(C.BTF_ESF))
        self.clean_filter = wx.BitmapButton(self, -1, I.clear_filters,
                                            style=wx.NO_BORDER)
        self.clean_filter.SetToolTipString(_(C.BTF_CF))

        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_button.Add(self.button_execution)
        sizer_button.Add(s_line_update,
                         flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)
        sizer_button.Add(self.update_filters)
        sizer_button.Add(self.clean_filter)

        self.sizer_toll = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_toll.Add(sizer_button, 4)
        self.sizer_toll.Add(self.toolbar, 1)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer_toll, 0, wx.LEFT | wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

        # ------ self inicailes executions ----------------------------
        self.button_execution.Bind(wx.EVT_BUTTON, self.OnClickExecution)
        self.update_filters.Bind(wx.EVT_BUTTON, self.OnClickFilter)
        self.clean_filter.Bind(wx.EVT_BUTTON, self.OnClickCleanFilter)

        self.button_execution.Disable()
        self.update_filters.Disable()
        self.clean_filter.Disable()
        self.presenter = CurvesFigurePresenter(self, test)

    # ------ self controls --------------------------------------------

    def OnClickExecution(self, event):
        self.page_curves.updateDatas()
        self.update_filters.Enable()

    def OnClickFilter(self, event):
        if self.page_curves.verificFilter():
            self.clean_filter.Enable()

    def OnClickCleanFilter(self, event):
        self.page_curves.cleanFilter()
        self.clean_filter.Disable()
        self.update_filters.Enable()

    def enableButtons(self):
        self.button_execution.Enable()
        if self.presenter.containsFilter():
            self.clean_filter.Enable()

    def disableButtons(self):
        self.button_execution.Disable()
