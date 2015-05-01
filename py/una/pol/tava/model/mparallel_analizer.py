# -*- coding: utf-8 -*-
'''
Created on 19/2/2015

@author: abrahan
'''
from py.una.pol.tava.dao import dparallel_analizer
from py.una.pol.tava.model.mresult import ResultModel
from py.una.pol.tava.model.miteration import InterationModel as itm
from py.una.pol.tava.model.mindividual import IndividualModel as inm
from py.una.pol.tava.base.entity import ParallelAnalizer
from py.una.pol.tava.base import tavac as tvc
from py.una.pol.tava.base.entity import FigureGrid


from py.una.pol.tava.base.tavac import fileDelete

mode = str(tvc.MODE_PARALLEL_COORDINATES_AL)


class ParallelAnalizerModel():

    def __init__(self):
        '''
        Constructor
        '''

    def add(self, test):
        '''
        Función que agrega un ParallelAnalizer a la base de datos.

        '''
        figure_grid = FigureGrid()
        figure_grid.grid = True
        figure_grid.orientation = 0
        figure_grid.red_color = '#BFBFBF'
        figure_grid.red_width = 1
        figure_grid.red_style = 0

        r_id = test.test_details[0].result_id
        re = ResultModel().getResultById(r_id)
        ner = re.number_objectives

        pa = ParallelAnalizer()
        pa.name_figure = 'Tava'
        pa.legent = True
        pa.color_lines = '#d7c16b'  # '#4ECDC4'
        pa.enable_objectives = ','.join(['1'] * ner)
        pa.order_objective = ','.join([str(i) for i in range(ner)])
        pa.order_name_obj = re.name_objectives
        pa.name_objetive = re.name_objectives
        pa.test_config_id = test.id
        pa.name_variable = re.name_variables
        pa.maxs_objetive = None
        pa.mins_objetive = None
        pa.colors_backgrounds = tvc.TREE_BACKGROUND_AL + ',' + \
            tvc.FIGURE_BACKGROUND_AL + ',' + tvc.T_FIGURE_BACKGROUND_AL
        pa.figure_grid = figure_grid

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

    def getParallelAnalizerById(self, pa_id):
        return dparallel_analizer.getParallelAnalizerById(pa_id)

    def updateByFigure(self, pa):
        pa.name_figure = 'Tava'
        pa.legent = True
        pa.color_lines = '#d7c16b'  # '#4ECDC4'
        return dparallel_analizer.add(pa)

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
        for index in range(len(obj_order_filter)):
            count_var = str(index + 1)
            list_gra.append(obj_order_filter[index] + ',' + str(ident) + '\n')
            list_obj.append(count_var + ',' + obj_order_filter[index] + '\n')
            list_var.append(count_var + ',' + var_order_filter[index] + '\n')

        tvc.createfileForParallel(list_gra, list_obj, list_var,
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

    def fileForDelete(self, iteration):
        filename = str(iteration) + '.mode.' + mode + '.csv'
        return fileDelete(filename)

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
    def getParallelAxe(self, iteration, _len, _pos, axe, legend_g, color_g):
        df = inm().getCsv(iteration, mode)

        axe = self._parallel_coordinatesTava(df, 'Name', _len, _pos, axe,
                                             True, legend_g,
                                             color=color_g)
        return axe

    # --- en tab TabVariables ------
    def getVar(self, ite):
        filename = str(ite) + '.mode.' + mode + '.' + 'var'
        return tvc.redFileForTab(filename)

    def getVariablesForTab(self, iteration):
        return self.getVar(iteration)

    # --- en tab TabObjectives -----
    def getObjectivesForTab(self, iteration):
        return self.getObj(iteration)

    def getObj(self, ite):
        filename = str(ite) + '.mode.' + mode + '.' + 'obj'
        return tvc.redFileForTab(filename)

    # --- en tab TabFiltros --------
    def getMinMaxForTabFilter(self, iteration):
        return inm().getMinMax(iteration, mode)

    def _parallel_coordinatesTava(self, frame, class_column, len_color=1,
                                  pos_color=0, ax=None, no_seque=True,
                                  is_use_legends=True, cols=None, color=None,
                                  use_columns=False, xticks=None,
                                  colormap=None, **kwds):
        """Parallel coordinates plotting.

        Parameters
        ----------
        frame: DataFrame
        class_column: str
            Column name containing class names
        len_color: int,, default 1
            Color amount taken into account
        pos_color: int, default 0
            Position of the color to be used
        ax: matplotlib.axis, optional
            matplotlib axis object
        no_seque: boolean, default True
            Indicates type of graph
        is_use_legends: boolean, default True
            To use for show legend.
        cols: list, optional
            A list of column names to use
        color: list or tuple, optional
            Colors to use for the different classes
        use_columns: bool, optional
            If true, columns will be used as xticks
        xticks: list or tuple, optional
            A list of values to use for xticks
        colormap: str or matplotlib colormap, default None
            Colormap to use for line colors.
        kwds: keywords
            Options to pass to matplotlib plotting method

        Returns
        -------
        ax: matplotlib axis object

        Examples
        --------
        >>> from pandas import read_csv
        >>> from pandas.tools.plotting import parallel_coordinates
        >>> from matplotlib import pyplot as plt
        >>> df = read_csv(\
          'https://raw.github.com/pydata/pandas/master/pandas/tests/data/iris.csv')
        >>> parallel_coordinates(\
                        df, 'Name', color=('#556270', '#4ECDC4', '#C7F464'))
        >>> plt.show()
        """
        import matplotlib.pyplot as plt
        import numpy as np
        from pandas.compat import lrange
        import pandas.core.common as com
        from pandas.tools.plotting import _get_standard_colors

        n = len(frame)
        classes = frame[class_column].drop_duplicates()
        class_col = frame[class_column]

        if cols is None:
            df = frame.drop(class_column, axis=1)
        else:
            df = frame[cols]

        used_legends = set([])
        ncols = len(df.columns)

        # determine values to use for xticks
        if use_columns is True:
            if not np.all(np.isreal(list(df.columns))):
                raise ValueError('Columns must \
                be numeric to be used as xticks')
            x = df.columns
        elif xticks is not None:
            if not np.all(np.isreal(xticks)):
                raise ValueError('xticks specified must be numeric')
            elif len(xticks) != ncols:
                raise ValueError('Length of\
                xticks must match number of columns')
            x = xticks
        else:
            x = lrange(ncols)

        if ax is None:
            ax = plt.gca()

        color_values = _get_standard_colors(num_colors=len_color,
                                            colormap=colormap,
                                            color_type='random', color=color)

        colors = dict(zip(classes, [color_values[pos_color]]))

        for i in range(n):
            y = df.iloc[i].values
            kls = class_col.iat[i]
            label = com.pprint_thing(kls)
            if label not in used_legends and is_use_legends:
                used_legends.add(label)
                ax.plot(x, y, color=colors[kls], label=label, **kwds)
            else:
                ax.plot(x, y, color=colors[kls], **kwds)

        ax.set_xticks(x)
        ax.set_xticklabels(df.columns)
        ax.set_xlim(x[0], x[-1])
        ax.legend(loc='upper right')

        return ax
    # ------------------------------------------------------------------
