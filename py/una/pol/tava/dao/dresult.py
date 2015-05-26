# -*- coding: utf-8 -*-
'''
Created on 26/07/2014

@author: abrahan
'''
from py.una.pol.tava.base import base, abm
from py.una.pol.tava.base.entity import Result
from sqlalchemy.orm import subqueryload
from sqlalchemy import and_
session = base.getSession()


# abm for result

def add(iteration):
    '''
    Función que agrega un iteration a la base de datos.

    :param name: String, representa el name de un iteration.
    :return: iteration.
    '''

    return abm.add(iteration)


def delete(result):
    '''
    Función que elimina un result de la base de datos.

    :param result: result, representa un result en la base de datos.
    '''
    abm.delete(result)


def upDate(result):
    '''
    Función que actualiza un result de la base de datos.

    :param result: result, representa un result en la base de datos.
    :return: result.
    '''
    return abm.add(result)

# Querys para Result


def getAllResult():
    return session.query(Result).order_by(Result.name).all()


def getResultsByProject(project_id):
    return session.query(Result).filter_by(project_id=project_id).all()


def getResultById(id_result):
    return session.query(Result).filter_by(id=id_result).first()


def getResultByName(name_result):
    return session.query(Result).filter_by(name=name_result).first()


def getResultWithIterations(result):
    return session.query(Result).options(subqueryload(Result.iterations)).\
        filter_by(id=result.id).first()


def getNamesResultForProject(project):
    return session.query(Result.name).filter_by(project_id=project.id).all()


def getResultByProjectIdAndFileName(project_id, reult_name):
    return session.query(Result).filter(and_(Result.project_id == project_id,
                                        Result.name == reult_name)).first()
