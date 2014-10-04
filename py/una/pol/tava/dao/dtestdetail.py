# -*- coding: utf-8 -*-
'''
Created on 03/10/2014

@author: abrahan
'''

from py.una.pol.tava.base import base, abm
from py.una.pol.tava.base.entity import TestDetail
session = base.getSession()


def add(test_detail):
    '''
    Función que agrega un TestDetail a la base de datos.

    :param test_detail: TestDetail, representa el objeto TestDetail a persistir.
    :return: TestDetail.
    '''

    return abm.add(test_detail)


def delete(test_detail):
    '''
    Función que elimina un TestDetail de la base de datos.

    :param test_detail: TestDetail, representa un TestDetail a ser eliminado de
                        la base de datos.
    '''
    abm.delete(test_detail)


def upDate(test_detail):
    '''
    Función que actualiza un TestDetail de la base de datos.

    :param test_detail: TestDetail, representa un TestDetail a ser actualizada
                        en la base de datos.
    :return: TestDetail.
    '''
    return abm.add(test_detail)


def getTestDetailByTestConfigId(test_config_id):
    return session.query(TestDetail).\
        filter_by(test_config_id=test_config_id).all()
