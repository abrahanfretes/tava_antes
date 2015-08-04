#  -*- coding: utf-8 -*-
'''
Created on 24/6/2015

@author: abrahan
'''
import wx
from wx import dataview as dv

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from py.una.pol.tava.presenter.metric.sing.pstatisticssing import\
    StatisticSingPresenter
from docutils.parsers.rst.directives import flag


# ------------------- Arbol de Archvivos e Iteraciones ------------------------
# -------------------                                  ------------------------
class StatiticSing(wx.Panel):
    def __init__(self, parent, page_curves, test):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------

        self.parent = parent
        self.page_curves = page_curves
        # self.p = FigureMetricSingPresenter(self, test)
        self.p = StatisticSingPresenter(self, test)

        # Estadistica

        self.t_table = dv.DataViewListCtrl(self)
        bs_statistic = wx.BoxSizer()
        bs_statistic.Add(self.t_table, 1, wx.EXPAND)

        # Figura
        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()
        bs_figure = wx.BoxSizer(wx.VERTICAL)
        bs_figure.Add(self.toolbar)
        bs_figure.Add(self.canvas)

        # sizers
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(bs_statistic, 1, wx.EXPAND)
        self.sizer.Add(bs_figure, 1, wx.EXPAND)

        self.SetSizer(self.sizer)

    def showFigure(self):
        self.p.initFigure()
