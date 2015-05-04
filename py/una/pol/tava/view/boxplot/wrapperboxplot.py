#  -*- coding: utf-8 -*-
'''
Created on 3/5/2015

@author: abrahan
'''
import wx

from py.una.pol.tava.view.boxplot.treeboxplot import BoxPlotTree
from py.una.pol.tava.view.boxplot.figureboxplot import BoxPlotFigure
from py.una.pol.tava.view.boxplot.filterboxplot import BoxPlotFilter
from py.una.pol.tava.presenter.pboxplot.pwrapperboxplot import BoxPlotPresenter


# -------------------         Panel Splitter           ------------------------
# -------------------                                  ------------------------
class BoxPlot(wx.Panel):
    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        #  ------ self customize ----------------------------------------
        #  ------ self components --------------------------------------
        splitter = wx.SplitterWindow(self)
        v_splitter = wx.SplitterWindow(splitter)

        self.tree_curves = BoxPlotTree(v_splitter, self, test)
        self.figure_curves = BoxPlotFigure(v_splitter, self, test)
        v_splitter.SplitVertically(self.tree_curves, self.figure_curves)
        v_splitter.SetSashGravity(0.2)
        v_splitter.SetMinimumPaneSize(8)

        self.filter_curves = BoxPlotFilter(splitter, self, test)
        splitter.SplitHorizontally(v_splitter, self.filter_curves)
        splitter.SetSashGravity(0.75)
        splitter.SetMinimumPaneSize(8)

        sizer = wx.BoxSizer()
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.presenter = BoxPlotPresenter(self, test)

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