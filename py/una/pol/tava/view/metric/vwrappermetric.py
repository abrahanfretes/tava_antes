#  -*- coding: utf-8 -*-
'''
Created on 7/6/2015

@author: abrahan
'''
import wx

from py.una.pol.tava.view.metric.vconfigmetric import ConfigMetric
from py.una.pol.tava.view.metric.vfiguremetric import FigureMetric


# -------------------         Panel Splitter           ------------------------
# -------------------                                  ------------------------
class WrapperMetric(wx.Panel):
    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        #  ------ self customize ----------------------------------------
        #  ------ self components --------------------------------------
        splitter = wx.SplitterWindow(self)

        self.f_metric = FigureMetric(splitter, self, test)
        self.c_metric = ConfigMetric(splitter, self, self.f_metric, test)
        splitter.SplitVertically(self.c_metric, self.f_metric)
        splitter.SetSashGravity(0.4)
        splitter.SetMinimumPaneSize(8)

        sizer = wx.BoxSizer()
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        #=======================================================================
        # self.presenter = BoxPlotPresenter(self, test)
        #=======================================================================

    # lógica para crear archivos y actualizar componetes
    #===========================================================================
    # def updateDatas(self):
    #     print'entro al pa'
    #     population = self.c_metric.presenter.population
    #     self.f_metric.showFigure()
    #===========================================================================