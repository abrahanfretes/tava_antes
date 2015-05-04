#  -*- coding: utf-8 -*-
'''
Created on 3/5/2015

@author: abrahan
'''
from py.una.pol.tava.base import base, abm
from py.una.pol.tava.base.entity import BoxPlot
session = base.getSession()


def add(parallel_analizer):
    '''
    Función que agrega un TestData a la base de datos.

    :param test_data: TestData, representa el objeto TestData a persistir.
    :return: TestData.
    '''

    return abm.add(parallel_analizer)


def getBoxPlotByTestId(t_id):
    return session.query(BoxPlot).filter_by(test_config_id=t_id).first()


def getBoxPlotById(bp_id):
    return session.query(BoxPlot).filter_by(id=bp_id).first()
