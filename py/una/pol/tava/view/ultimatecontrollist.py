__author__ = 'amfv'
import sys

import wx
import wx.lib.agw.ultimatelistctrl as ULC
from py.una.pol.tava.view import agreggation as ag
import py.una.pol.tava.dao.dmetric as dm

class MyFrame(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, parent, -1, "Metric Config")

        list = ULC.UltimateListCtrl(self, wx.ID_ANY, agwStyle=wx.LC_REPORT | wx.LC_VRULES
            |wx.LC_HRULES | wx.LC_SINGLE_SEL | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)

        list.InsertColumn(0, "Metric", width=150)
        list.InsertColumn(1, "Values")

        list_metrics = dm.getDistinctMetrics(1)

        index = 0
        # list_metrics = {'EpsDOM', 'EpsPreferred', 'FACrisp', 'FAFuzzy', 'Favour', 'NSGAII', 'POGA', 'POGAz'}
        for i, in list_metrics:
            list.InsertStringItem(index, i)
            choice = wx.Choice(list, -1, choices=[ag.MAX, ag.MIN])
            choice.SetSelection(0)
            list.SetItemWindow(index, 1, choice, expand=True)
            index += 1

        a = {}
        count = list.GetItemCount()
        for row in range(count):
            item = list.GetItem(row)
            wnd = list.GetItemWindow(row, col=1)
            print(item.GetText())
            print(wnd.GetStringSelection())
            a[item.GetText()] = wnd.GetStringSelection()

        print a

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(list, 1, wx.EXPAND)
        self.SetSizer(sizer)


# our normal wxApp-derived class, as usual

app = wx.App()

frame = MyFrame(None)
app.SetTopWindow(frame)
frame.SetSize((250, 500))
frame.Centre(wx.BOTH)
frame.Show()
app.MainLoop()