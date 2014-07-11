'''
Created on 27/06/2014

@author: afretes
'''
from py.una.pol.tava.model.bd.entity import Proyecto
from py.una.pol.tava.model.bd.entity import OPEN
from py.una.pol.tava.model.bd import abm
from py.una.pol.tava.model.bd import query

from datetime import date


class ProyectoPresenter():
    '''
    Clase ProyectoPresenter

    Define todas las funciones para acceder a las entidad Proyecto.

    '''
    def __init__(self):
        '''
        Constructor
        '''

    def add(self, nombre):
        proyecto = Proyecto(nombre, None, OPEN, date.today())
        return abm.add(proyecto)

    def upDate(self, proyecto):
        return abm.add(proyecto)

    def delete(self, proyecto):
        return abm.delete(proyecto)

    def getAll(self):
        return query.getAllProject()

    def getProjectById(self, idProyecto):
        return query.getProjectById(idProyecto)

    def getProjectByResult(self, resultado):
        return query.getProjectByResult(resultado)
