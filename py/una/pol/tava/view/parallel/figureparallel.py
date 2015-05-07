#  -*- coding: utf-8 -*-
'''
Created on 5/5/2015

@author: abrahan
'''
#  -*- coding: utf-8 -*-
'''
Created on 3/5/2015

@author: abrahan
'''

import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from wx import GetTranslation as _

from py.una.pol.tava.view import vi18n as C
from py.una.pol.tava.view import vimages as I
from py.una.pol.tava.presenter.pparallel.pfigureparallel import\
    ParallelFigurePresenter
from py.una.pol.tava.view.parallel.configparallel import ParallelConfig


# ------------------- Panel Para Grafico De Coordenadas Paralelas -------------
# -------------------                                  ------------------------
class ParallelFigure(wx.Panel):
    '''
    Clase Panel que contiene la configuracion para la visualizacion del
    componente de coordenadas paralelas.
    '''
    def __init__(self, parent, page_parallel, test):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        self.parent = parent
        self.page_parallel = page_parallel

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
        s_line_cinfig = wx.StaticLine(self, style=wx.LI_VERTICAL)
        self.config = wx.BitmapButton(self, -1, I.update_config,
                                      style=wx.NO_BORDER)
        self.config.SetToolTipString(_(C.BTF_NC))

        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_button.Add(self.button_execution)
        sizer_button.Add(s_line_update,
                         flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)
        sizer_button.Add(self.update_filters)
        sizer_button.Add(self.clean_filter)
        sizer_button.Add(s_line_cinfig,
                         flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)
        sizer_button.Add(self.config)

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
        self.config.Bind(wx.EVT_BUTTON, self.OnClickConfig)

        self.button_execution.Disable()
        self.update_filters.Disable()
        self.clean_filter.Disable()
        self.config.Disable()
        self.presenter = ParallelFigurePresenter(self, test)

    # ------ self controls --------------------------------------------

    def OnClickExecution(self, event):
        self.page_parallel.updateDatas()
        self.update_filters.Enable()
        self.config.Enable()

    def OnClickFilter(self, event):
        if self.page_parallel.verificFilter():
            self.clean_filter.Enable()

    def OnClickCleanFilter(self, event):
        self.page_parallel.cleanFilter()
        self.clean_filter.Disable()
        self.update_filters.Enable()

    def OnClickConfig(self, event):
        pa = self.presenter.getParalelAnalizer()
        ParallelConfig(self, self.page_parallel, pa)

    def enableButtons(self):
        self.button_execution.Enable()
        self.config.Disable()
        self.update_filters.Disable()
        self.clean_filter.Disable()

    def disableButtons(self):
        self.button_execution.Disable()
        self.config.Enable()
        self.update_filters.Enable()
        if self.presenter.containsFilter():
            self.clean_filter.Enable()
