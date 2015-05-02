#  -*- coding: utf-8 -*-
'''
Created on 2/5/2015

@author: abrahan
'''
import wx

from py.una.pol.tava.view.curves.treecurves import CurvesTree
from py.una.pol.tava.view.curves.figurecurves import CurvesFigure
from py.una.pol.tava.view.curves.filtercurves import CurvesFilter
from py.una.pol.tava.presenter.pandrews_curves.pwrappercurves\
    import AndrewsCurvesPresenter


# -------------------         Panel Splitter           ------------------------
# -------------------                                  ------------------------
class AndrewsCurves(wx.Panel):
    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        #  ------ self customize ----------------------------------------
        #  ------ self components --------------------------------------
        splitter = wx.SplitterWindow(self)
        v_splitter = wx.SplitterWindow(splitter)

        self.tree_curves = CurvesTree(v_splitter, self, test)
        self.figure_curves = CurvesFigure(v_splitter, self, test)
        v_splitter.SplitVertically(self.tree_curves, self.figure_curves)
        v_splitter.SetSashGravity(0.2)
        v_splitter.SetMinimumPaneSize(8)

        self.filter_curves = CurvesFilter(splitter, self, test)
        splitter.SplitHorizontally(v_splitter, self.filter_curves)
        splitter.SetSashGravity(0.75)
        splitter.SetMinimumPaneSize(8)

        sizer = wx.BoxSizer()
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.presenter = AndrewsCurvesPresenter(self, test)

    # lógica de manejo de botones de Figura
    def enableButtonFigure(self):
        self.figure_curves.enableButtons()

    def disableButtonFigure(self):
        self.figure_curves.disableButtons()

    # lógica para crear archivos y actualizar componetes
    def updateDatas(self):
        'acutulalizacion de datos'
        ite = self.tree_curves.getCurrentSelection()
        self.presenter.createDates(ite)
        # mensaje de actualizacion de figura
        self.figure_curves.presenter.newFigure([ite])
        self.figure_curves.disableButtons()
        self.tree_curves.setAfterExecute()
        # mensaje de actualizacion de variables
        # mensaje de actualizacion de objetivos
        self.filter_curves.presenter.updateValuesList([ite])
        pass

    # lógica de los botones para filtros
    def verificFilter(self):
        if self.filter_curves.presenter.isFilterModified():
            max, min = self.filter_curves.presenter.getListValues()
            self.presenter.updateFilters(max, min)
            self.updateDatas()
            return True
        else:
            return False

    def cleanFilter(self):
        self.presenter.clearFilters()
        self.updateDatas()
