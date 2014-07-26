# -*- coding: utf-8 -*-
'''
Created on 26/07/2014

@author: abrahan
'''
from py.una.pol.tava.base import base, abm
from py.una.pol.tava.base.entity import Project
from sqlalchemy.orm import subqueryload

session = base.getSession()


# abm for project

def add(project):
    '''
    Función que agrega un Project a la base de datos.

    :param name: String, representa el name de un project.
    :return: Project.
    '''

    return abm.add(project)


def delete(project):
    '''
    Función que elimina un Project de la base de datos.

    :param project: Project, representa un project en la base de datos.
    '''
    abm.delete(project)


def upDate(project):
    '''
    Función que actualiza un Project de la base de datos.

    :param project: Project, representa un project en la base de datos.
    :return: Project.
    '''
    return abm.add(project)

#Querys para Proyectos


def getAllProject():
    return session.query(Project).order_by(Project.creation_date,
                                           Project.state)


def getAllProjectWithResults():
    return session.query(Project).options(subqueryload(Project.results))


def getProjectWithResults(project):

    return session.query(Project).options(subqueryload(Project.results)).\
            filter_by(id=project.id).first()


def getProjectById(id_project):
    return session.query(Project).filter_by(id=id_project).first()


def getProjectByResult(result):
    return session.query(Project).filter_by(id=result.proyecto_id).first()


def getAllNamesProject():
    return session.query(Project.name).order_by(Project.name).all()
