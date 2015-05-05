#  -*- coding: utf-8 -*-
'''
Created on 5/5/2015

@author: abrahan
'''

import wx

from py.una.pol.tava.view.parallel.treeparallel import ParallelTree
from py.una.pol.tava.view.parallel.figureparallel import ParallelFigure
from py.una.pol.tava.view.parallel.filterparallel import ParallelFilter
from py.una.pol.tava.presenter.pparallel.pwrapperparallel import\
    ParallelPresenter


# -------------------         Panel Splitter           ------------------------
# -------------------                                  ------------------------
class ParrallelCoordenates(wx.Panel):
    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        #  ------ self customize ----------------------------------------
        #  ------ self components --------------------------------------
        splitter = wx.SplitterWindow(self)
        v_splitter = wx.SplitterWindow(splitter)

        self.tree_parallel = ParallelTree(v_splitter, self, test)
        self.figure_parallel = ParallelFigure(v_splitter, self, test)
        v_splitter.SplitVertically(self.tree_parallel, self.figure_parallel)
        v_splitter.SetSashGravity(0.2)
        v_splitter.SetMinimumPaneSize(8)

        self.filter_parallel = ParallelFilter(splitter, self, test)
        splitter.SplitHorizontally(v_splitter, self.filter_parallel)
        splitter.SetSashGravity(0.75)
        splitter.SetMinimumPaneSize(8)

        sizer = wx.BoxSizer()
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.presenter = ParallelPresenter(self, test)

    # lógica de manejo de botones de Figura
    def enableButtonFigure(self):
        self.figure_parallel.enableButtons()

    def disableButtonFigure(self):
        self.figure_parallel.disableButtons()

    # lógica para crear archivos y actualizar componetes
    def updateDatas(self):
        'acutulalizacion de datos'
        ite = self.tree_parallel.getCurrentSelection()
        self.presenter.createDates(ite)
        # mensaje de actualizacion de figura
        self.figure_parallel.presenter.newFigure([ite])
        self.figure_parallel.disableButtons()
        self.tree_parallel.setAfterExecute()
        # mensaje de actualizacion de variables
        # mensaje de actualizacion de objetivos
        self.filter_parallel.presenter.updateValuesList([ite])
        pass

    # lógica de los botones para filtros
    def verificFilter(self):
        if self.filter_parallel.presenter.isFilterModified():
            max, min = self.filter_parallel.presenter.getListValues()
            self.presenter.updateFilters(max, min)
            self.updateDatas()
            return True
        else:
            return False

    def cleanFilter(self):
        self.presenter.clearFilters()
        self.updateDatas()