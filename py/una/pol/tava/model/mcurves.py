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

from py.una.pol.tava.base.tavac import fileDelete


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

    def fileForDelete(self, iteration):
        filename = str(iteration) + '.mode.' + mode + '.csv'
        return fileDelete(filename)

    # --- en TopPanel -----

    def createDates(self, pa, ite_id):

        # obtengo los objetivos y variables de los individuos de la iteración
        obj_list = []
        var_list = []
        ite = itm().getIterationById(ite_id)
        ident = ite.identifier
        unordered_index = []

        for ind in inm().getIndividualsByIteracionId(ite_id):
            obj_list.append(ind.objectives)
            var_list.append(ind.variables)

        # obtiene los datos filtratdos por objetivos
        # crea lista filtrada de  nombres
        # crea lista filtrada de  objetivos (nueva lista)
        list_obj = pa.enable_objectives.split(',')
        obj_filters = []
        if list_obj.count('0'):
            unordered_index = self._getIndexOnes(list_obj)
            for index in range(len(obj_list)):
                obj_filters.append(self._getLineFilters(obj_list[index],
                                                        unordered_index))
        else:
            obj_filters = obj_list

        # obtiene los datos ordenados
        index_orders_real = [int(i) for i in pa.order_objective.split(',')]

        obj_orders = []
        if self.isOrder(unordered_index, index_orders_real):
            ordered_index = []
            for i in index_orders_real:
                ordered_index.append(unordered_index.index(i))

            for obj in obj_filters:
                obj_orders.append(self._getLineOrders(obj, ordered_index))
        else:
            obj_orders = obj_filters

        # agrego filtros si es distinto a None(debe modifiar todos los archivo)
        # debe modificar tanto los valores objetivos como los de Variables
        obj_order_filter = []
        var_order_filter = []
        obj_order_no_filter = []
        if(not (pa.maxs_objetive is None) and not (pa.mins_objetive is None)):
            max_objetive = [float(i) for i in pa.maxs_objetive.split(',')]
            min_objetive = [float(i) for i in pa.mins_objetive.split(',')]
            for index in range(len(obj_orders)):
                to_write = True
                value = [float(i) for i in obj_orders[index].split(',')]
                for i in range(len(value)):
                    if min_objetive[i] > value[i] or\
                            value[i] > max_objetive[i]:
                        to_write = False
                        break

                if(to_write):
                    obj_order_filter.append(obj_orders[index])
                    var_order_filter.append(var_list[index])
                else:
                    obj_order_no_filter.append(obj_orders[index])
        else:
            obj_order_filter = obj_orders
            var_order_filter = var_list

        # se prepara una lista de valores para el grafico, los objetivos y las
        # las variables
        filename_gra = str(ite_id) + '.mode.' + mode + '.csv'
        filename_var = str(ite_id) + '.mode.' + mode + '.var'
        filename_obj = str(ite_id) + '.mode.' + mode + '.obj'

        list_gra = []
        list_obj = []
        list_var = []

        list_gra.append(pa.order_name_obj + ',Name\n')
        if obj_order_no_filter != []:
            for index in range(len(obj_order_filter)):
                count_var = str(index + 1)
                list_gra.append(obj_order_filter[index] + ', Filtrado\n')
                list_obj.append(count_var + ','
                                + obj_order_filter[index] + '\n')
                list_var.append(count_var + ','
                                + var_order_filter[index] + '\n')

            # valores fuera de filtro
            for index in range(len(obj_order_no_filter)):
                list_gra.append(obj_order_no_filter[index] + ','
                                + str(ident) + '\n')
        else:
            for index in range(len(obj_order_filter)):
                count_var = str(index + 1)
                list_gra.append(obj_order_filter[index]
                                + ',' + str(ident) + '\n')
                list_obj.append(count_var + ','
                                + obj_order_filter[index] + '\n')
                list_var.append(count_var + ','
                                + var_order_filter[index] + '\n')

        tvc.createfileForCurves(list_gra, list_obj, list_var,
                                filename_gra, filename_var, filename_obj)

    def isOrder(self, unordered_index, index_orders_real):
        if unordered_index == sorted(index_orders_real):
            return False
        if len(unordered_index) != len(index_orders_real):
            return False
        return True

    def _getIndexOnes(self, list_obj):
        index_one = []
        for i in range(len(list_obj)):
            if list_obj[i] == '1':
                index_one.append(i)
        return index_one

    def _getLineFilters(self, var, list_obj):
        var_aux = var.split(',')
        to_ret = []
        for i in list_obj:
            to_ret.append(var_aux[i])
        return ','.join(to_ret)

    def _getLineOrders(self, objective, ordered_index):
        objective_aux = objective.split(',')
        to_ret = []
        for i in ordered_index:
            to_ret.append(objective_aux[i])
        return ','.join(to_ret)

    # --- en tab TabVariables ------

    def getListVariables(self, ite):
        filename = str(ite) + '.mode.' + mode + '.' + 'var'
        return tvc.redFileForTab(filename)

    # --- en tab TabObjectives -----
    def getListObjectives(self, ite):
        filename = str(ite) + '.mode.' + mode + '.' + 'obj'
        return tvc.redFileForTab(filename)

    # --- en tab TabFiltros --------
    def getMinMaxObjective(self, ite):
        return inm().getMinMax(ite, mode)
