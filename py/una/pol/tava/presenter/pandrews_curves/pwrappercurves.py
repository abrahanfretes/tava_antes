#  -*- coding: utf-8 -*-
'''
Created on 1/5/2015

@author: abrahan
'''


from py.una.pol.tava.model.mcurves import AndrewsCurvesModel as acm


class AndrewsCurvesPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test

    def createDates(self, ite):
        acm().fileForDelete(ite)
        ac = acm().getCurvesByTestId(self.test.id)
        return acm().createDates(ac, ite)

    def updateFilters(self, maxs_objetive, mins_objetive):
        ac = acm().getCurvesByTestId(self.test.id)
        ac.maxs_objetive = maxs_objetive
        ac.mins_objetive = mins_objetive
        acm().upDate(ac)

    def clearFilters(self):
        ac = acm().getCurvesByTestId(self.test.id)
        ac.maxs_objetive = None
        ac.mins_objetive = None
        acm().upDate(ac)
