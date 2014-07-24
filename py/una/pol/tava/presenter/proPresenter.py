# -*- coding: utf-8 -*-
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
        pass

    def add(self, nombre):
        '''
        Función que agrega un Proyecto a la base de datos.

        :param nombre: String, representa el nombre de un proyecto.
        :return: Proyecto.
        '''
        proyecto = Proyecto(nombre, None, OPEN, date.today())
        return abm.add(proyecto)

    def upDate(self, proyecto):
        '''
        Función que actualiza un Proyecto de la base de datos.

        :param proyecto: Proyecto, representa un proyecto en la base de datos.
        :return: Proyecto.
        '''
        return abm.add(proyecto)

    def delete(self, proyecto):
        '''
        Función que elimina un Proyecto de la base de datos.

        :param proyecto: Proyecto, representa un proyecto en la base de datos.
        '''
        abm.delete(proyecto)

    def getAll(self):
        '''
        Función que obtiene todos los Proyectos de la base de datos.
        :return: Lista de Proyectos.
        '''
        return query.getAllProject()

    def getProjectById(self, idProyecto):
        '''
        Función que retorna un Proyecto cuyo id es pasado como parámetro.

        :param idProyecto:
        :return: Proyecto
        '''
        return query.getProjectById(idProyecto)

    def getProjectByResult(self, resultado):
        '''
        Función que retorna un Proyecto tomando como parámetro un Resultado.

        :param resultado:
        :return: Proyecto
        '''
        return query.getProjectByResult(resultado)

    def getNamesProject(self):
        listNames = []
        for name in query.getAllNamesProject():
            listNames.append(list(name).pop())

        return listNames
