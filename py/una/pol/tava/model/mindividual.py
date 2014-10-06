'''
Created on 03/07/2014

@author: abrahan
'''
from py.una.pol.tava.dao import dindividual


class IndividualModel(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def getIndividualsByIteracionId(self, id_iteration):
        return dindividual.getIndividualsByIteracionId(id_iteration)

    def getIndividualsByListIterationId(self, list_id_iteration):

        individual = []
        for id_ite in list_id_iteration:
            individual.append(dindividual.getIndividualsByIteracionId(id_ite))
        return individual

    def getIdentifierAndVariableOfIndividual(self, list_id_iteration):

        individual = []
        for id_ite in list_id_iteration:
            individual.\
            append(dindividual.getIdentifierAndVariableOfIndividual(id_ite))
        return individual

    def getIdentifierAndObjectiveOfIndividual(self, list_id_iteration):

        individual = []
        for id_ite in list_id_iteration:
            individual.\
            append(dindividual.getIdentifierAndObjectiveOfIndividual(id_ite))
        return individual

    def getIdentifierObjectiveVariableOfIndividual(self, list_id_iteration):

        individual = []
        for id_ite in list_id_iteration:
            individual.append(dindividual.\
                            getIdentifierObjectiveVariableOfIndividual(id_ite))
        return individual

    def getVarDTLZOfIndividual(self, list_id_iteration):

        individual = []
        for idIte in list_id_iteration:
            individual.append(dindividual.getVarDTLZOfIndividual(idIte))
        return individual
