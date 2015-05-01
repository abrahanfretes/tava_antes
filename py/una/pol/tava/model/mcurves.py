# -*- coding: utf-8 -*-
'''
Created on 1/5/2015

@author: abrahan
'''
from py.una.pol.tava.dao import dcurves
from py.una.pol.tava.model.mresult import ResultModel
from py.una.pol.tava.base.entity import AndrewsCurves
from py.una.pol.tava.base import tavac as tvc
from py.una.pol.tava.base.entity import AndrewsGrid


mode = str(tvc.MODE_ANDREWS_CURVES)


class AndrewsCurvesModel():

    def __init__(self):
        '''
        Constructor
        '''

    def add(self, test):
        '''
        Función que agrega un ParallelAnalizer a la base de datos.

        '''
        andrews_grid = AndrewsGrid()
        andrews_grid.grid = True
        andrews_grid.orientation = 0
        andrews_grid.red_color = '#BFBFBF'
        andrews_grid.red_width = 1
        andrews_grid.red_style = 0

        r_id = test.test_details[0].result_id
        re = ResultModel().getResultById(r_id)
        ner = re.number_objectives

        ac = AndrewsCurves()
        ac.name_figure = 'Andrews Cuves'
        ac.legent = True
        ac.color_lines = '#d7c16b'  # '#4ECDC4'
        ac.enable_objectives = ','.join(['1'] * ner)
        ac.order_objective = ','.join([str(i) for i in range(ner)])
        ac.order_name_obj = re.name_objectives
        ac.name_objetive = re.name_objectives
        ac.test_config_id = test.id
        ac.name_variable = re.name_variables
        ac.maxs_objetive = None
        ac.mins_objetive = None

        ac.colors_backgrounds = tvc.TREE_BACKGROUND_AC + ',' + \
            tvc.FIGURE_BACKGROUND_AC + ',' + tvc.T_FIGURE_BACKGROUND_AC
        ac.andrews_grid = andrews_grid

        return dcurves.add(ac)

    def upDate(self, ac):
        '''
        Función que actualiza un TestConfig de la base de datos.

        '''
        return dcurves.add(ac)
