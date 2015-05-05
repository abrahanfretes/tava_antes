#  -*- coding: utf-8 -*-
'''
Created on 5/5/2015

@author: abrahan
'''

from py.una.pol.tava.model.mparallel_analizer import\
    ParallelAnalizerModel as pam


class ParallelPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test

    def createDates(self, ite):
        pam().fileForDelete(ite)
        pa = pam().getParallelAnalizerByIdTest(self.test.id)
        return pam().createDates(pa, ite)

    def updateFilters(self, maxs_objetive, mins_objetive):
        pa = pam().getParallelAnalizerByIdTest(self.test.id)
        pa.maxs_objetive = maxs_objetive
        pa.mins_objetive = mins_objetive
        return pam().upDate(pa)

    def clearFilters(self):
        pa = pam().getParallelAnalizerByIdTest(self.test.id)
        pa.maxs_objetive = None
        pa.mins_objetive = None
        return pam().upDate(pa)
