# -*- coding: utf-8 -*-
'''
Created on 2/6/2015

@author: abrahan
'''
from py.una.pol.tava.model.mmetric import MetricModel as mm
from py.una.pol.tava.base.entity import TestMetric


class TestMetricDialogPresenter():
    def __init__(self, iview,  project):
        self.iview = iview
        self.name = project.name
        self.id = project.id
        self.results = self.getResults(self.id)

    def getResults(self, project_id):
        return mm().getResultMetricByProjectId(project_id)

    def getNamesResults(self):
        ret = []
        for mr in self.results:
            ret.append(mr.filename)
        return ret

    def getNamesMetric(self):
        return mm().getNamesTestMetric(self.id)

    def addTest(self, name, index):
        test_metric = TestMetric()
        test_metric.name = name
        test_metric.project_id = self.id
        test_metric.result_metric_id = self.results[index].id
        mm().addTestMetric(test_metric)
        self.iview.Close()
