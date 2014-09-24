'''
Created on 23/09/2014

@author: abrahan
'''
from py.una.pol.tava.base import base, abm
from py.una.pol.tava.base.entity import TestGraphic
session = base.getSession()


# abm for result

def add(test_graphic):
    '''
    Función que agrega un TestGraphic a la base de datos.

    :param test_graphic: TestGraphic, representa el objeto TestGraphic a
                        persistir.
    :return: TestGraphic.
    '''

    return abm.add(test_graphic)


def delete(test_graphic):
    '''
    Función que elimina un TestGraphic de la base de datos.

    :param test_graphic: TestGraphic, representa un TestGraphic a ser eliminado
                        de la base de datos.
    '''
    abm.delete(test_graphic)


def upDate(test_graphic):
    '''
    Función que actualiza un TestGraphic de la base de datos.

    :param test_graphic: TestGraphic, representa un TestGraphic a ser
                        actualizada en la base de datos.
    :return: TestGraphic.
    '''
    return abm.add(test_graphic)


def getTestGraphicByTestConfigId(test_config_id):
    return session.query(TestGraphic).\
        filter_by(test_config_id=test_config_id).all()
