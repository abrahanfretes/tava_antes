#  -*- coding: utf-8 -*-
'''
Created on 3/5/2015

@author: abrahan
'''

import wx
import wx.lib.agw.customtreectrl as CT

from py.una.pol.tava.view import vimages as I
from py.una.pol.tava.presenter.pboxplot.ptreeboxplot\
    import BoxPlotTreePresenter


# ------------------- Arbol de Archvivos e Iteraciones ------------------------
# -------------------                                  ------------------------
class BoxPlotTree(CT.CustomTreeCtrl):
    def __init__(self, parent, page_boxplot, test):
        CT.CustomTreeCtrl.__init__(self, parent, style=CT.TR_SINGLE,
                                   agwStyle=CT.TR_HIDE_ROOT)

        # ------ self customize ---------------------------------------
        il = wx.ImageList(16, 16)
        il.Add(I.filegraph_png)
        il.Add(I.arrow_bullet_right)
        il.Add(I.arrow_grey_right)
        self.AssignImageList(il)

        # ------ self components --------------------------------------
        self.page_boxplot = page_boxplot
        self.root = self.AddRoot("Box Plot")
        self.presenter = BoxPlotTreePresenter(self, test)

        # ------ self inicailes executions ----------------------------
        self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnChecked)

    # ------ self controls -------------------------------------------
    def OnChecked(self, event):
        item = event.GetItem()
        self.presenter.current_item = item
        if self.presenter.isValidItem():
            self.page_boxplot.enableButtonFigure()
        else:
            self.page_boxplot.disableButtonFigure()

    def getCurrentSelection(self):
        return self.GetPyData(self.presenter.current_item)

    def setAfterExecute(self):

        if self.presenter.old_item is not None:
            self.SetItemImage(self.presenter.old_item, 2)
            self.SetItemBold(self.presenter.old_item, False)
            self.SetItemItalic(self.presenter.old_item, False)

        item = self.presenter.current_item
        self.presenter.old_item = item
        self.SetItemBold(item, True)
        self.SetItemItalic(item, True)
        self.SetItemImage(item, 2)
        self.SetItemImage(item, 1)
