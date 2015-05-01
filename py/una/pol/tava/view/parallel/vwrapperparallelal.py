#  -*- coding: utf-8 -*-
'''
Created on 28/3/2015

@author: abrahan
'''

import wx
from wx import GetTranslation as _
import wx.lib.agw.aui as aui

from py.una.pol.tava.view import vi18n as C
from py.una.pol.tava.presenter.pparallel.pparallelal import TopPanelPresenter
from py.una.pol.tava.view.parallel.vparallelal import ParallelTreeAL
from py.una.pol.tava.view.parallel.vparallelal import ParallelFigureAL
from py.una.pol.tava.view.parallel.vparallelal import TabVariables
from py.una.pol.tava.view.parallel.vparallelal import TabObjectives
from py.una.pol.tava.view.parallel.vparallelal import TabFilters


# -------------------         Panel Splitter           ------------------------
# -------------------                                  ------------------------
class WorkingPageFL(wx.SplitterWindow):
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
        tree_al = ParallelTreeAL(self, test)
        figure_al = ParallelFigureAL(self, test)
        width = int(round(self.GetParent().GetSize().GetWidth() * 0.50)) * 15
        self.SplitVertically(tree_al, figure_al, width)
        # ------ self inicailes executions -----------------------------
        # ------ self controls -----------------------------------------
        # ------ self controls -----------------------------------------


# -------------------         Panel for botton         ------------------------
# -------------------                                  ------------------------
class BottomPanel(wx.Panel):

    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
        tab_aui = aui.AuiNotebook(self)
        tab_aui.SetAGWWindowStyleFlag(aui.AUI_NB_TOP)

        # ------ self components --------------------------------------
        data_var = TabVariables(tab_aui, test)
        data_obj = TabObjectives(tab_aui, test)
        filters = TabFilters(tab_aui, test)

        # ------ self inicailes executions ----------------------------
        tab_aui.AddPage(data_var, _(C.FAN_V), True)
        tab_aui.AddPage(data_obj, _(C.FAN_O), False)
        tab_aui.AddPage(filters, _(C.FAN_F), False)

        sizer = wx.BoxSizer()
        sizer.Add(tab_aui, 1, wx.EXPAND)
        self.SetSizer(sizer)
    # ------ self controls --------------------------------------------
