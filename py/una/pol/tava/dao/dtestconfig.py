# -*- coding: utf-8 -*-
'''
Created on 23/09/2014

@author: abrahan
'''
from py.una.pol.tava.base import base, abm
from py.una.pol.tava.base.entity import TestConfig
session = base.getSession()


# abm for result

def add(test_config):
    '''
    Función que agrega un TestConfig a la base de datos.

    :param test_config: TestConfig, representa el objeto TestConfig a
                        persistir.
    :return: TestConfig.
    '''

    return abm.add(test_config)


def delete(test_config):
    '''
    Función que elimina un TestConfig de la base de datos.

    :param test_config: TestConfig, representa un TestConfig a ser eliminado de
                        la base de datos.
    '''
    abm.delete(test_config)


def upDate(test_config):
    '''
    Función que actualiza un TestConfig de la base de datos.

    :param test_config: TestConfig, representa un TestConfig a ser actualizada
                        en la base de datos.
    :return: TestConfig.
    '''
    return abm.add(test_config)


def getTestConfigByProjectId(project_id):
    return session.query(TestConfig).filter_by(project_id=project_id).all()


def getTestConfigById(test_config_id):
    return session.query(TestConfig).filter_by(id=test_config_id).first()
