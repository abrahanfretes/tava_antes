'''
Created on 28/06/2014

@author: abrahan
'''
from py.una.pol.tava.model import abm
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

    def guardar(self, listFile, proyecto):

        for path in listFile:
            resultado = procesarArchivo(path)
            proyecto.resultados.append(resultado)
        abm.add(proyecto)

    def getResultadoByProyecto(self, proyecto):
        return query.getResultadosByProyecto(proyecto)

    def getResultadoById(self, idResultado):
        return query.getResultadoById(idResultado)
