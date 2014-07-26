# -*- coding: utf-8 -*-
'''
Created on 27/06/2014

@author: afretes
'''
from py.una.pol.tava.model.bd.entity import Project
from py.una.pol.tava.model.bd.entity import OPEN
from py.una.pol.tava.model.bd import abm
from py.una.pol.tava.model.bd import query

from datetime import date


class ProjectModel():
    '''
    Clase ProjectModel

    Define todas las funciones para acceder a las entidad Project.

    '''
    def __init__(self):
        pass

    def add(self, name):
        '''
        Función que agrega un Project a la base de datos.

        :param name: String, representa el name de un project.
        :return: Project.
        '''
        project = Project(name, None, OPEN, date.today())
        return abm.add(project)

    def upDate(self, project):
        '''
        Función que actualiza un Project de la base de datos.

        :param project: Project, representa un project en la base de datos.
        :return: Project.
        '''
        return abm.add(project)

    def delete(self, project):
        '''
        Función que elimina un Project de la base de datos.

        :param project: Project, representa un project en la base de datos.
        '''
        abm.delete(project)

    def getAll(self):
        '''
        Función que obtiene todos los projects de la base de datos.
        :return: Lista de projects.
        '''
        return query.getAllProject()

    def getProjectById(self, id_project):
        '''
        Función que retorna un Project cuyo id es pasado como parámetro.

        :param id_project:
        :return: Project
        '''
        return query.getProjectById(id_project)

    def getProjectByResult(self, result):
        '''
        Función que retorna un Project tomando como parámetro un Resultado.

        :param result:
        :return: Project
        '''
        return query.getProjectByResult(result)

    def getNamesProject(self):
        listNames = []
        for name in query.getAllNamesProject():
            listNames.append(list(name).pop())

        return listNames
