'''
Created on 28/06/2014

@author: abrahan
'''
from procesadorResultado import procesarArchivo
from py.una.pol.tava.model import query


class ResultadoPresenter(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def add(self, listPathFile, proyecto):
        procesarArchivo(listPathFile, proyecto)

    def getResultsByProject(self, proyecto):
        return query.getResultsByProject(proyecto)

    def getResultById(self, idResultado):
        return query.getResultById(idResultado)
