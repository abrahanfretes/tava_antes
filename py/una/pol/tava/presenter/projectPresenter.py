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
    def add(self, nombre):
        proyecto = Proyecto(nombre, 0, date.today())
        return abm.add(proyecto)

    def delete(self, proyecto):
        return abm.delete(proyecto)

    def getAll(self):
        return query.getAllProject()

    def getProjectById(self, idProyecto):
        return query.getProjectById(idProyecto)

    def getProjectByResult(self, resultado):
        return query.getProjectByResult(resultado)
