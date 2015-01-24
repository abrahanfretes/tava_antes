'''
Created on 09/12/2014

@author: arsenioferreira
'''
from py.una.pol.tava.base import base, abm
from py.una.pol.tava.base.entity import SomConfig
session = base.getSession()


def add(som):
    '''
    Funcion que agrega un Som a la base de datos.

    :param som: Som, representa el objeto Som a
                        persistir.
    :return: Som.
    '''

    return abm.add(som)


def getSomById(id_som):
    return session.query(SomConfig).filter_by(id=id_som).first()
