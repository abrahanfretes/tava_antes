# -*- coding: utf-8 -*-
'''
Created on 19/2/2015

@author: abrahan
'''
from py.una.pol.tava.dao import dparallel_analizer
from py.una.pol.tava.model.mresult import ResultModel
from py.una.pol.tava.base.entity import ParallelAnalizer


class ParallelAnalizerModel():

    def __init__(self):
        '''
        Constructor
        '''

    def add(self, test):
        '''
        Función que agrega un ParallelAnalizer a la base de datos.

        '''

        r_id = test.test_details[0].result_id
        ner = ResultModel().getNumberObjetivetById(r_id)
        name_obj = ResultModel().getNamesObjetivestById(r_id)

        pa = ParallelAnalizer()
        pa.name_figure = 'Tava'
        pa.legent_figure = True
        pa.color_figure = '#d7c16b'  # '#4ECDC4'
        pa.enable_objectives = ','.join(['1']*ner)
        pa.order_objective = ','.join([str(i) for i in range(ner)])
        pa.order_name_obj = name_obj
        pa.name_objetive = name_obj
        pa.test_config_id = test.id

        return dparallel_analizer.add(pa)

    def upDate(self, parallel_analizer):
        '''
        Función que actualiza un TestConfig de la base de datos.

        '''
        return dparallel_analizer.add(parallel_analizer)

    def restartDefaul(self, parallel_analizer):
        '''
        Función que restablece los valores por defecto.

        '''
        return self.add(parallel_analizer)

    def getParallelAnalizerByIdTest(self, t_id):
        return dparallel_analizer.getParallelAnalizerByIdTest(t_id)

    def updateByFigure(self, pa):
        pa.name_figure = 'Tava'
        pa.legent_figure = True
        pa.color_figure = '#d7c16b'  # '#4ECDC4'
        return dparallel_analizer.add(pa)
