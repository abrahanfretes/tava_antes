# -*- coding: utf-8 -*-
'''
Created on 1/5/2015

@author: abrahan
'''
from py.una.pol.tava.base import base, abm
from py.una.pol.tava.base.entity import AndrewsCurves
session = base.getSession()


def add(parallel_analizer):
    '''
    Función que agrega un TestData a la base de datos.

    :param test_data: TestData, representa el objeto TestData a persistir.
    :return: TestData.
    '''

    return abm.add(parallel_analizer)


def getParallelAnalizerByIdTest(t_id):
    return session.query(AndrewsCurves).filter_by(test_config_id=t_id)\
        .first()


def getParallelAnalizerById(ac_id):
    return session.query(AndrewsCurves).filter_by(id=ac_id).first()
