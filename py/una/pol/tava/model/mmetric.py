'''
Created on 14/5/2015

@author: abrahan
'''
from py.una.pol.tava.base.tavac import vonlucken
from py.una.pol.tava.model.processor import styleVon
from py.una.pol.tava.dao import dmetric


class MetricModel():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def add(self, paths, project, style):

        if style == vonlucken:
            return styleVon.processMetricsFile(paths, project)

        # aca se debe agregar las funciones para otros estilos
        # if style == otro:
        # otro.procesarArchivo(list_path_file, project)
        pass

    def quickCheckStyle(self, path, style):
        if style == vonlucken:
            return styleVon.quickCheckStyleMetric(path)

    def getFilesNames(self, project):
        listNames = []
        print dmetric.getFilesNamesResultMetricByProject(project)
        for name in dmetric.getFilesNamesResultMetricByProject(project):
            listNames.append(list(name).pop())

        return listNames

    # Funciones Para ResultMetric
    def getResultMetricByProjectId(self, project_id):
        return dmetric.getResultMetricByProjectId(project_id)

    def getNamesMetricResults(self, project_id):
        to_ret = []
        for mr in self.getResultMetricByProjectId(project_id):
            to_ret.append(mr.filename)
        return to_ret

        # Funciones Para TestMetric
    def getTestMetricByProjectId(self, project_id):
        return dmetric.getTestMetrics(project_id)

    def getNamesTestMetric(self, project_id):
        to_ret = []
        for tm in self.getTestMetricByProjectId(project_id):
            to_ret.append(tm.name)
        print to_ret
        return to_ret

    def addTestMetric(self, test_metric):
        dmetric.add(test_metric)
