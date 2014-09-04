# -*- coding: utf-8 -*-
'''
Created on 27/06/2014

@author: afretes
'''
from py.una.pol.tava.base.entity import Project
from py.una.pol.tava.base.entity import OPEN
from py.una.pol.tava.dao import dproject

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
        return dproject.add(project)

    def upDate(self, project):
        '''
        Función que actualiza un Project de la base de datos.

        :param project: Project, representa un project en la base de datos.
        :return: Project.
        '''
        return dproject.add(project)

    def delete(self, project):
        '''
        Función que elimina un Project de la base de datos.

        :param project: Project, representa un project en la base de datos.
        '''
        dproject.delete(project)

    def getAll(self):
        '''
        Función que obtiene todos los projects de la base de datos.
        :return: Lista de projects.
        '''
        return dproject.getAllProject()

    def getProjectById(self, id_project):
        '''
        Función que retorna un Project cuyo id es pasado como parámetro.

        :param id_project:
        :return: Project
        '''
        return dproject.getProjectById(id_project)

    def getProjectByResult(self, result):
        '''
        Función que retorna un Project tomando como parámetro un Resultado.

        :param result:
        :return: Project
        '''
        return dproject.getProjectByResult(result)

    def getNamesProject(self):
        listNames = []
        for name in dproject.getAllNamesProject():
            listNames.append(list(name).pop())

        return listNames

    def getNamesHideProject(self):
        listNames = []
        for name in dproject.getAllNamesHideProject():
            listNames.append(list(name).pop())

        return listNames

    def getHideProject(self):

        return list(dproject.getAllHideProject())

    def getProjectForName(self, name_project):
        return dproject.getProjectByName(name_project)
