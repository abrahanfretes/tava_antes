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

    def guardar(self, listPathFile, proyecto):
        procesarArchivo(listPathFile, proyecto)

    def getResultadoByProyecto(self, proyecto):
        return query.getResultadosByProyecto(proyecto)

    def getResultadoById(self, idResultado):
        return query.getResultadoById(idResultado)
