'''
Created on 27/06/2014

@author: afretes
'''
from py.una.pol.tava.model.entity import Proyecto
from py.una.pol.tava.model import abm
from py.una.pol.tava.model import query

from datetime import date


class ProyectoPresenter():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    def guardar(self, nombre):
        proyecto = Proyecto(nombre, 0, date.today())
        abm.add(proyecto)

    def getProyectos(self):
        return query.getProyectos()

    def getProyectoById(self, idProyecto):
        return query.getProyectoById(idProyecto)

    def getProyectoByResultado(self, resultado):
        return query.getProyectoByResultado(resultado)
