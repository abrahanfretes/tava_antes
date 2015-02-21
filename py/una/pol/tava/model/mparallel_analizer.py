# -*- coding: utf-8 -*-
'''
Created on 19/2/2015

@author: abrahan
'''
from py.una.pol.tava.dao import dparallel_analizer


class ParallelAnalizerModel():

    def __init__(self):
        '''
        Constructor
        '''

    def add(self, parallel_analizer):
        '''
        Función que agrega un ParallelAnalizer a la base de datos.

        '''
        parallel_analizer.name_figure = 'Tava'
        parallel_analizer.legent_figure = True
        # '#4ECDC4'
        parallel_analizer.color_figure = '#d7c16b'
        return dparallel_analizer.add(parallel_analizer)

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
