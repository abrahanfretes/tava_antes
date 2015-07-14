#  -*- coding: utf-8 -*-
'''
Created on 24/6/2015

@author: abrahan
'''
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from py.una.pol.tava.presenter.metric.sing.pstatisticssing import\
    StatisticSingPresenter


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

        self.figure = Figure(figsize=(8, 4), dpi=120)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.toolbar)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def showFigure(self):
        self.p.initFigure()
