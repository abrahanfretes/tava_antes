'''
Created on 04/07/2014

@author: abrahan
'''
from py.una.pol.tava.dao import diteration
from py.una.pol.tava.model.mresult import ResultModel as rm


class InterationModel(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def getIterationById(self, id_iteration):
        return  diteration.getIterationWithIndividual(id_iteration)

    def getIterations(self, list_id_iteration):
        iterations = []
        for id_ite in list_id_iteration:
            iterations.append(diteration.getIterationWithIndividual(id_ite))
        return iterations

    def getIterationWithIndividual(self, id_iteration):
        return diteration.getIterationWithIndividual(id_iteration)

    def getIterationsByResult(self, result):
        return self.getIterationsByResultId(result.id)

    def getIterationsByResultId(self, result_id):
        return diteration.getIterationsByResultId(result_id)

    def getIterationsByProjectAndFileName(self, project, file_name):
        return self.getIterationsByProjectIdAndFileName(project.id, file_name)

    def getIterationsByProjectIdAndFileName(self, project_id, file_name):
        result = rm().getResultByProjectIdAndFileName(project_id, file_name)
        return self.getIterationsByResultId(result.id)

    def getIdentifierById(self, id_iteracion):
        return diteration.getIterationById(id_iteracion).identifier
