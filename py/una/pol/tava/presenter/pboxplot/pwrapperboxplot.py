#  -*- coding: utf-8 -*-
'''
Created on 3/5/2015

@author: abrahan
'''

from py.una.pol.tava.model.mboxplot import BoxPlotModel as bpm


class BoxPlotPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test

    def createDates(self, ite):
        bpm().fileForDelete(ite)
        bp = bpm().getBoxPlotByTestId(self.test.id)
        return bpm().createDates(bp, ite)

    def updateFilters(self, maxs_objetive, mins_objetive):
        bp = bpm().getBoxPlotByTestId(self.test.id)
        bp.maxs_objetive = maxs_objetive
        bp.mins_objetive = mins_objetive
        return bpm().upDate(bp)

    def clearFilters(self):
        bp = bpm().getBoxPlotByTestId(self.test.id)
        bp.maxs_objetive = None
        bp.mins_objetive = None
        return bpm().upDate(bp)
