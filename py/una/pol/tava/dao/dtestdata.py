# -*- coding: utf-8 -*-
'''
Created on 23/09/2014

@author: abrahan
'''
from py.una.pol.tava.base import base, abm
from py.una.pol.tava.base.entity import TestData
session = base.getSession()


def add(test_data):
    '''
    Función que agrega un TestData a la base de datos.

    :param test_data: TestData, representa el objeto TestData a persistir.
    :return: TestData.
    '''

    return abm.add(test_data)


def delete(test_data):
    '''
    Función que elimina un TestData de la base de datos.

    :param test_data: TestData, representa un TestData a ser eliminado de
                        la base de datos.
    '''
    abm.delete(test_data)


def upDate(test_data):
    '''
    Función que actualiza un TestData de la base de datos.

    :param test_data: TestData, representa un TestData a ser actualizada
                        en la base de datos.
    :return: TestData.
    '''
    return abm.add(test_data)


def getTestDatasByTestConfigId(test_config_id):
    return session.query(TestData).\
        filter_by(test_config_id=test_config_id).all()
