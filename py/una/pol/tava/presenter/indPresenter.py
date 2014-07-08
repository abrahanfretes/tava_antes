'''
Created on 03/07/2014

@author: abrahan
'''
from py.una.pol.tava.model.bd import query


class IndividuoPresenter(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def getIndividuosByIteracionId(self, idIteracion):
        return query.getIndividuosByIteracionId(idIteracion)

    def getIndividuosByIteracionesId(self, listIdIteracion):

        individuos = []
        for idIte in listIdIteracion:
            individuos.append(query.getIndividuosByIteracionId(idIte))
        return individuos

    def getIdenVarOfIndividuo(self, listIdIteracion):

        individuos = []
        for idIte in listIdIteracion:
            individuos.append(query.getIdenVarOfIndividuo(idIte))
        return individuos

    def getIdenObjOfIndividuo(self, listIdIteracion):

        individuos = []
        for idIte in listIdIteracion:
            individuos.append(query.getIdenObjOfIndividuo(idIte))
        return individuos

    def getIdenObjVarOfIndividuo(self, listIdIteracion):

        individuos = []
        for idIte in listIdIteracion:
            individuos.append(query.getIdenObjVarOfIndividuo(idIte))
        return individuos

    def getVarDTLZOfIndividuo(self, listIdIteracion):

        individuos = []
        for idIte in listIdIteracion:
            individuos.append(query.getVarDTLZOfIndividuo(idIte))
        return individuos
