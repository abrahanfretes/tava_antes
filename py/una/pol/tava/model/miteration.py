'''
Created on 04/07/2014

@author: abrahan
'''
from py.una.pol.tava.model.bd import query


class InterationModel(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def getIterationById(self, id_iteration):
        return  query.getIterationWithIndividual(id_iteration)

    def getIterations(self, list_id_iteration):
        iterations = []
        for id_ite in list_id_iteration:
            iterations.append(query.getIterationWithIndividual(id_ite))
        return iterations

    def getIterationWithIndividual(self, id_iteration):
        return query.getIterationWithIndividual(id_iteration)
