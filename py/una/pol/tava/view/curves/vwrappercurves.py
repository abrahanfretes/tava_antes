#  -*- coding: utf-8 -*-
'''
Created on 1/5/2015

@author: abrahan
'''

import wx


# -------------------         Panel Splitter           ------------------------
# -------------------                                  ------------------------
class PageAndrewsCurves(wx.SplitterWindow):
    def __init__(self, parent, test):
        wx.SplitterWindow.__init__(self, parent)

        #  ------ self customize ----------------------------------------
        self.SetMinimumPaneSize(3)
        self.SetBorderSize(1)

        #  ------ self components --------------------------------------
        self.top_panel = TopPanel(self, test)
        self.footer = BottomPanel(self, test)
        high = int(round(self.GetParent().GetSize().GetWidth() * 0.50))
        self.SplitHorizontally(self.top_panel, self.footer, high)
        # ------ self controls -----------------------------------------


from py.una.pol.tava.view.curves.vcurves import CurvesTree
from py.una.pol.tava.view.curves.vcurves import CurvesFigure
from py.una.pol.tava.presenter.pandrews_curves.pcurves import TopPanelPresenter


# -------------------         Panel for top            ------------------------
# -------------------                                  ------------------------
class TopPanel(wx.SplitterWindow):
    def __init__(self, parent, test):
        wx.SplitterWindow.__init__(self, parent)

        # ------ self customize ----------------------------------------
        self.SetMinimumPaneSize(3)
        # ------ self components --------------------------------------
        self.parent = parent
        self.presenter = TopPanelPresenter(self, test)

        curves_tree = CurvesTree(self, test)
        curves_figure = CurvesFigure(self, test)

        width = int(round(self.GetParent().GetSize().GetWidth() * 0.50)) * 15
        self.SplitVertically(curves_tree, curves_figure, width)
        # ------ self inicailes executions -----------------------------
        # ------ self controls -----------------------------------------
        # ------ self controls -----------------------------------------


# -------------------         Panel for botton         ------------------------
# -------------------                                  ------------------------
class BottomPanel(wx.Panel):

    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
    # ------ self controls --------------------------------------------
