'''
Created on 04/07/2014

@author: abrahan
'''
from py.una.pol.tava.model.bd import query


class IteracionPresenter(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def getIterationById(self, idIteracion):
        return  query.getIterationWithIndividuo(idIteracion)

    def getIterations(self, listId):
        iteraciones = []
        for ite in listId:
            iteraciones.append(query.getIterationWithIndividuo(ite))
        return iteraciones

    def getIterationWithIndividuo(self, idIteracion):
        return query.getIterationWithIndividuo(idIteracion)
