'''
Created on 03/07/2014

@author: abrahan
'''
from py.una.pol.tava.model.bd import query


class IndividualModel(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def getIndividualsByIteracionId(self, id_iteration):
        return query.getIndividualsByIteracionId(id_iteration)

    def getIndividualsByIterationId(self, list_id_iteration):

        individual = []
        for id_ite in list_id_iteration:
            individual.append(query.getIndividualsByIteracionId(id_ite))
        return individual

    def getIdentifierAndVariableOfIndividual(self, list_id_iteration):

        individual = []
        for id_ite in list_id_iteration:
            individual.\
            append(query.getIdentifierAndVariableOfIndividual(id_ite))
        return individual

    def getIdentifierAndObjectiveOfIndividual(self, list_id_iteration):

        individual = []
        for id_ite in list_id_iteration:
            individual.\
            append(query.getIdentifierAndObjectiveOfIndividual(id_ite))
        return individual

    def getIdentifierObjectiveVariableOfIndividual(self, list_id_iteration):

        individual = []
        for id_ite in list_id_iteration:
            individual.append(query.\
                            getIdentifierObjectiveVariableOfIndividual(id_ite))
        return individual

    def getVarDTLZOfIndividual(self, list_id_iteration):

        individual = []
        for idIte in list_id_iteration:
            individual.append(query.getVarDTLZOfIndividual(idIte))
        return individual
