# -*- coding: utf-8 -*-
'''
Created on 26/07/2014

@author: abrahan
'''
from py.una.pol.tava.base import base
from py.una.pol.tava.base.entity import Individual

session = base.getSession()

#Querys para Individual


def getIndividuosByIteracion(iteration):
    return session.query(Individual).order_by(Individual.identifier).\
                            filter_by(iteracion_id=iteration.id).all()


def getIndividualsByIteracionId(iteration_id):
    return session.query(Individual).order_by(Individual.identifier).\
                            filter_by(iteration_id=iteration_id).all()


def getIdentifierAndVariableOfIndividual(id_iteration):
    return session.query(Individual.identifier, Individual.variables).\
                            order_by(Individual.identifier).\
                            filter_by(iteracion_id=id_iteration).all()


def getIdentifierAndObjectiveOfIndividual(id_iteration):
    return session.query(Individual.identifier, Individual.objectives).\
                            order_by(Individual.identifier).\
                            filter_by(iteracion_id=id_iteration).all()


def getIdenObjOfIndividuoByIteracion(iteration):
    return session.query(Individual.identifier, Individual.objectives).\
                            order_by(Individual.identifier).\
                            filter_by(iteracion_id=iteration.id).all()


def getIdentifierObjectiveVariableOfIndividual(id_iteration):
    return session.query(Individual.identifier, Individual.objectives,
                    Individual.variables).order_by(Individual.identifier).\
                            filter_by(iteracion_id=id_iteration).all()


def getVarDTLZOfIndividual(id_iteration):
    return session.query(Individual.identifier, Individual.varDTLZ).\
                            rder_by(Individual.identifier).\
                            filter_by(iteracion_id=id_iteration).all()
