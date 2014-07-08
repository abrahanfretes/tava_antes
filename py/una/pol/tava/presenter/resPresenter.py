'''
Created on 28/06/2014

@author: abrahan
'''
from py.una.pol.tava.model.processor import styleVon
from py.una.pol.tava.model.bd import query
from py.una.pol.tava.model.bd import abm


class ResultadoPresenter(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def add(self, listPathFile, proyecto):
        styleVon.procesarArchivo(listPathFile, proyecto)

    def delete(self, resultado):
        abm.delete(resultado)

    def getResultsByProject(self, proyecto):
        return query.getResultsByProject(proyecto)

    def getResultById(self, idResultado):
        return query.getResultById(idResultado)
