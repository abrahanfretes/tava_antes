#  -*- coding: utf-8 -*-
'''
Created on 7/6/2015

@author: abrahan
'''
import wx

from py.una.pol.tava.view.metric.sing.vconfigmetricsing import ConfigMetricSing
from py.una.pol.tava.view.metric.sing.vstatisticsing import StatiticSing


# -------------------         Panel Splitter           ------------------------
# -------------------                                  ------------------------
class WrapperMetricSing(wx.Panel):
    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        #  ------ self customize ----------------------------------------
        #  ------ self components --------------------------------------
        splitter = wx.SplitterWindow(self)

        # self.f_statistic = FigureMetricSing(splitter, self, test)
        self.f_statistic = StatiticSing(splitter, self, test)
        self.c_metric = ConfigMetricSing(splitter, self,
                                         self.f_statistic, test)
        splitter.SplitVertically(self.c_metric, self.f_statistic)
        splitter.SetSashGravity(0.4)
        splitter.SetMinimumPaneSize(8)

        sizer = wx.BoxSizer()
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
