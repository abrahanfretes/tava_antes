# -*- coding: utf-8 -*-
'''
Created on 26/07/2014

@author: abrahan
'''
from py.una.pol.tava.base import base, abm
from py.una.pol.tava.base.entity import Iteration
from sqlalchemy.orm import subqueryload

session = base.getSession()


# abm for result

def add(iteration):
    '''
    Función que agrega un iteration a la base de datos.

    :param name: String, representa el name de un iteration.
    :return: iteration.
    '''

    return abm.add(iteration)

#Querys para Iteration


def getIterationsByResult(result):
    return session.query(Iteration).order_by(Iteration.id).\
                        filter_by(id=result.id).all()


def getIterationsByIdResult(id_result):
    return session.query(Iteration).order_by(Iteration.id).\
                        filter_by(id=id_result).all()


def getIterationById(id_iteration):
    return session.query(Iteration).filter_by(id=id_iteration).first()


def getIterationWithIndividual(id_iteration):
    return session.query(Iteration).options(
            subqueryload(Iteration.individuals)).\
            filter_by(id=id_iteration).first()
