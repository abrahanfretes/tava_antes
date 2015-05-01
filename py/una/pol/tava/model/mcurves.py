# -*- coding: utf-8 -*-
'''
Created on 1/5/2015

@author: abrahan
'''
from pandas.tools.plotting import andrews_curves

from py.una.pol.tava.dao import dcurves
from py.una.pol.tava.model.mresult import ResultModel
from py.una.pol.tava.base.entity import AndrewsCurves
from py.una.pol.tava.base import tavac as tvc
from py.una.pol.tava.base.entity import AndrewsGrid

from py.una.pol.tava.model.miteration import InterationModel as itm
from py.una.pol.tava.model.mindividual import IndividualModel as inm



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

    def getCurvesByTestId(self, t_id):
        return dcurves.getCurvesByTestId(t_id)

    # --- en tree -----
    def getFormatTree(self, test):

        to_ret = {}
        for detail in test.test_details:
            r_name = ResultModel().getNameById(detail.result_id)
            ite_list = []
            for data in detail.test_datas:
                identifier = str(itm().getIdentifierById(data.iteration_id))
                ite_list.append((identifier, data.iteration_id))
            to_ret[r_name] = ite_list

        return to_ret

    # --- en figure -----
    def getCurvesAxe(self, iteration, _len, _pos, axe, legend_g, color_g):
        data = inm().getCsv(iteration, mode)

        return andrews_curves(data, 'Name', axe)
