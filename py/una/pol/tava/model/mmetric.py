'''
Created on 14/5/2015

@author: abrahan
'''
from py.una.pol.tava.base.tavac import vonlucken
from py.una.pol.tava.model.processor import styleVon
from py.una.pol.tava.dao import dmetric


class MetricModel(object):
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

    def getResultMetricByProjectId(self, project_id):
        return dmetric.getResultMetricByProjectId(project_id)
