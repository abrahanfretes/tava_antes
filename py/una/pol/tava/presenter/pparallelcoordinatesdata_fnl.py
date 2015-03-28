'''
Created on 25/2/2015

@author: abrahan
'''
import wx
from wx.lib.pubsub import Publisher as pub
import topic as T

from py.una.pol.tava.model.mresult import ResultModel as rm
from py.una.pol.tava.model.miteration import InterationModel as im
from py.una.pol.tava.model.mindividual import IndividualModel as inm
from py.una.pol.tava.model.mparallel_analizer import ParallelAnalizerModel


class TopPanelPresenter:
    def __init__(self, iview, test, mode):
        self.iview = iview
        self.test = test
        self.mode = mode
        self.ite_list = []

        pub.subscribe(self.updateFigureForChangeTreePub,
                      T.PARALLEL_UPDATE_FIGURE_FOR_TREE)
        pub.subscribe(self.updateFigureConfigPub,
                      T.PARALLEL_UPDATE_FIGURE_CONFIG)
        pub.subscribe(self.updateListObjectPub,
                      T.PARALLEL_UPDATE_FIGURE_LIST_OBJ)
        pub.subscribe(self.updateFiltersObjectPub,
                      T.PARALLEL_SET_FILTERS_OBJ)

    # ---- Funciones Generales ------------------------------------------------

    def updateFigureForChangeTreePub(self, message):
        ite_tuple = message.data
        self.ite_list = list(ite_tuple)
        ite = self.ite_list[0]
        self.fileDelete(ite)
        self.createFiles(ite)
        # mensaje de actualizacion de figura
        # mensaje de actualizacion de variables
        # mensaje de actualizacion de objetivos
        pub.sendMessage(T.PARALLEL_UPDATE_ALL, self.ite_list)

    def updateFigureConfigPub(self, message):
        # mensaje de actualizacion de figura
        pub.sendMessage(T.PARALLEL_UPDATE_FIGURE_CONFIG_SHOW, self.ite_list)

    def updateListObjectPub(self, message):
        if self.ite_list != []:
            ite = self.ite_list[0]
            self.fileDelete(ite)
            self.createFiles(ite)
            # mensaje de actualizacion de figura
            # mensaje de actualizacion de variables
            # mensaje de actualizacion de objetivos
            pub.sendMessage(T.PARALLEL_UPDATE_ALL, self.ite_list)

    def updateFiltersObjectPub(self, message):
        if self.ite_list != []:
            filter_tuple = message.data

            ite = self.ite_list[0]
            self.fileDelete(ite)
            self.createFiles(ite, filter_tuple[0], filter_tuple[1])
            # mensaje de actualizacion de figura
            # mensaje de actualizacion de variables
            # mensaje de actualizacion de objetivos
            pub.sendMessage(T.PARALLEL_UPDATE_ALL, self.ite_list)

    def fileExists(self, ite):
        return inm().fileExists(ite, self.mode)

    def fileDelete(self, ite):
        return inm().fileDelete(ite, self.mode)

    def createFiles(self, ite, max_objetive=None, min_objetive=None):
        pam = ParallelAnalizerModel()
        p_analizer = pam.getParallelAnalizerByIdTest(self.test.id)
        return inm().createFiles(ite, self.mode, p_analizer.enable_objectives,
                                 p_analizer.order_objective,
                                 p_analizer.order_name_obj,
                                 max_objetive, min_objetive)
    # -------------------------------------------------------------------------


# ------------------- ParallelDataPresenter -----------------------------------
class ParallelDataTreePresenter:
    def __init__(self, iview, test_details):

        self.iview = iview
        self.root = self.iview.AddRoot("Test Data")
        self.checkeds_last = []

        pub.subscribe(self.verifyChangeChecked, T.PARALLEL_VERIFY_TREE_CHECKEO)

        self.InitUI(test_details)
        # ------------------------------------------------------------

        #  Inicializacion del arbol de proyectos
    def InitUI(self, details):

        # inicializamos el arbol
        for detail in details:
            r_name = rm().getNameById(detail.result_id)
            td_item = self.iview.AppendItem(self.root, r_name)
            self.iview.SetItemPyData(td_item, '')
            self.iview.SetItemImage(td_item, 0, wx.TreeItemIcon_Normal)

            for data in detail.test_datas:
                idn = str(im().getIdentifierById(data.iteration_id))
                tda_item = self.iview.AppendItem(td_item, idn, ct_type=1)
                self.iview.SetItemPyData(tda_item, data.iteration_id)
                self.iview.CheckItem(tda_item, False)

        # ordenamos el arbol
        self.iview.SortChildren(self.root)

        # expandimos el arbol
        for item in self.root.GetChildren():
            self.iview.Expand(item)

        # inicializamos la lista de chequeados
        self.checkeds_last = sorted(self.getListChecked())

    def getListChecked(self, true=True):
        to_dicc = []
        for item_result in self.root.GetChildren():
            for item_ite in item_result.GetChildren():
                if true == self.iview.IsItemChecked(item_ite):
                    to_dicc.append(self.iview.GetItemPyData(item_ite))
        return to_dicc

    def getLenListChecked(self):
        return len(self.getListChecked())

    def isChangeChecked(self):
        aux = sorted(self.getListChecked())
        if self.checkeds_last != aux:
            self.checkeds_last = aux
            return True
        return False

    def setChecked(self):
        pub.sendMessage(T.PARALLEL_TREE_CHECK_FIGURE, self.getOneChecked())

    def getOneChecked(self):
        return 1 == self.getLenListChecked()

    def verifyChangeChecked(self, message):
        if self.isChangeChecked():
            pub.sendMessage(T.PARALLEL_UPDATE_FIGURE_FOR_TREE,
                            tuple(self.getListChecked()))
# ------------------------------------------------------------------------------


class ParallelDataFigurePresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        self.figure_axes = None
        self.title_g = ''

        pub.subscribe(self.newFigureTestPub, T.PARALLEL_UPDATE_ALL)
        pub.subscribe(self.newFigureTestShowPub,
                      T.PARALLEL_UPDATE_FIGURE_CONFIG_SHOW)

    # ---- Funciones Generales ------------------------------------------------
    def newFigureTestPub(self, message):
        ite_list = message.data
        self.newFigureTest(ite_list)

    def newFigureTestShowPub(self, message):
        ite_list = message.data
        self.newFigureTest(ite_list)

    def cleanParallelFigure(self):
        if not(self.figure_axes is None):
            self.iview.figure.delaxes(self.figure_axes)

    def getParallelAnalizer(self):
        pam = ParallelAnalizerModel()
        return pam.getParallelAnalizerByIdTest(self.test.id)
    # -------------------------------------------------------------------------

    # ---- Funciones definidas para ParallelFigure Test -----------------------
    def newFigureTest(self, ite_list, suptitle=''):
        pa = self.getParallelAnalizer()
        self.color_g = (pa.color_figure,)
        self.legend_g = pa.legent_figure
        self.cleanParallelFigure()
        suptitle = self.title_g
        self.figure_axes = self._initFigurePaint(ite_list, suptitle)
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    #     Funciones Bases o comunes para todos los tipos de grafico
    # --------------------------------------------------------------------------
    def _initFigurePaint(self, ite_list, suptitle='', sp_axe=None):
        axe = None
        if sp_axe is None:
            axe = self.iview.figure.gca()
        else:
            axe = self.iview.figure.add_subplot(sp_axe)
        self.iview.figure.suptitle(suptitle)
        axe = self._figurePaint(axe, ite_list)
        return axe

    def _figurePaint(self, axe, ite_list, count_last=0):
        _pos = 0 + count_last
        _len = len(ite_list) + count_last
        for ite in ite_list:

            df = inm().getCsv(ite, self.iview.mode)

            axe = parallel_coordinatesTava(df, 'Name', _len, _pos, axe,
                                           True, self.legend_g,
                                           color=self.color_g)
            axe.grid(b=True)
            self.iview.canvas.draw()
            _pos += 1
        self.iview.canvas.draw()
        return axe
    # --------------------------------------------------------------------------


class ButtonsTollFigurePresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        self.parallel_analizer = None

        pub.subscribe(self.checkedTreePub, T.PARALLEL_TREE_CHECK_FIGURE)

        self.checkedTree(False)

    def checkedTreePub(self, message):
        self.checkedTree(message.data)

    def checkedTree(self, enable):
        if enable:
            self.iview.enableButtons()
        else:
            self.iview.disableButtons()

    def verifyTreeCheckeo(self):
        pub.sendMessage(T.PARALLEL_VERIFY_TREE_CHECKEO)

    def getStatesObjetives(self):
        no = rm().getNamesObjetivestById(self.test.test_details[0].result_id)
        vo = self.getParallelAnalizer().enable_objectives
        return no.split(','), vo.split(',')

    def getParallelAnalizer(self):
        if self.parallel_analizer is None:
            pam = ParallelAnalizerModel()
            self.parallel_analizer = pam.\
                getParallelAnalizerByIdTest(self.test.id)
        return self.parallel_analizer

    def setParallelAnalizer(self, parallel_analizer):
        self.parallel_analizer = parallel_analizer

    def setUpdateListObjetive(self, list_obj):
        parallel_analizer = self.getParallelAnalizer()
        list_obj_less = parallel_analizer.enable_objectives.split(',')

        if not sorted(list_obj) == sorted(list_obj_less):
            parallel_analizer.enable_objectives = ','.join(list_obj)
            names = parallel_analizer.name_objetive.split(',')

            obj_orders_var = []
            obj_orders_name = []
            order_name_obj = []
            for i in range(len(list_obj)):
                if list_obj[i] == '1':
                    obj_orders_var.append(str(i))
                    obj_orders_name.append(names[i])
                    order_name_obj.append(names[i])

            parallel_analizer.order_objective = ','.join(obj_orders_var)
            parallel_analizer.order_name_obj = ','.join(order_name_obj)
            pam = ParallelAnalizerModel()
            self.setParallelAnalizer(pam.upDate(parallel_analizer))
            pub.sendMessage(T.PARALLEL_UPDATE_FIGURE_LIST_OBJ)

    def getUpdateSort(self):
        return self.getParallelAnalizer().order_name_obj.split(',')

    def setUpdateSort(self, order_name_obj):
        parallel_analizer = self.getParallelAnalizer()
        names = parallel_analizer.name_objetive.split(',')
        order_name_obj_less = parallel_analizer.order_name_obj.split(',')

        if self.isListDiferentOrder(order_name_obj, order_name_obj_less):
            obj_orders_var = []
            for obj_name in order_name_obj:
                obj_orders_var.append(str(names.index(obj_name)))

            parallel_analizer.order_objective = ','.join(obj_orders_var)
            parallel_analizer.order_name_obj = ','.join(order_name_obj)
            pam = ParallelAnalizerModel()
            self.setParallelAnalizer(pam.upDate(parallel_analizer))
            pub.sendMessage(T.PARALLEL_UPDATE_FIGURE_SORT_OBJ,
                            tuple(order_name_obj))

    def updateConfigPa(self, legent_figure, color_figure):
        pa = self.getParallelAnalizer()
        pa.legent_figure = legent_figure
        pa.color_figure = color_figure
        pam = ParallelAnalizerModel()
        pam.upDate(pa)
        pub.sendMessage(T.PARALLEL_UPDATE_FIGURE_CONFIG)

    def restartDefaul(self):
        pam = ParallelAnalizerModel()
        pam.updateByFigure(self.getParallelAnalizer())
        pub.sendMessage(T.PARALLEL_UPDATE_FIGURE_CONFIG)

    def isListDiferentOrder(self, now_list, less_list):
        for i in range(len(now_list)):
            if now_list[i] != less_list[i]:
                return True
        return False

    def setFilters(self):
        pub.sendMessage(T.PARALLEL_ON_SET_FILTERS_OBJ)

    def cleanFilter(self):
        pub.sendMessage(T.PARALLEL_ON_CLEAN_FILTERS_OBJ)

    def getNamesObjetives(self):
        pa = self.getParallelAnalizer()
        to_ret = []

        for name in pa.name_objetive.split(','):
            to_ret.append([name, name])

        to_ret1 = []
        for name in pa.name_variable.split(','):
            to_ret1.append([name, name])

        return to_ret, to_ret1

    def setUpdateNamesObjetives(self, new_names, new_name_var):
        pa = self.getParallelAnalizer()
        indexs = [int(i) for i in pa.order_objective.split(',')]
        order_name_obj = []
        for i in indexs:
            order_name_obj.append(new_names[i])
        pa.name_objetive = ','.join(new_names)
        pa.order_name_obj = ','.join(order_name_obj)
        pa.name_variable = ','.join(new_name_var)
        pam = ParallelAnalizerModel()
        pam.upDate(pa)
        self.setParallelAnalizer(pam.upDate(pa))
        pub.sendMessage(T.PARALLEL_UPDATE_FIGURE_RENAME_OBJ)


class ParallelDataVarPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test

        pub.subscribe(self.updateDatasPub, T.PARALLEL_UPDATE_ALL)

        self.InitUI()

    def InitUI(self):
        pa = ParallelAnalizerModel().getParallelAnalizerByIdTest(self.test.id)
        v_names = 'key,' + pa.name_variable
        columns = v_names.split(',')
        self.countColumn = len(columns)
        for name in columns:
            self.iview.dvlc.AppendTextColumn(name, width=110)

    def updateDatasPub(self, message):
        ite_list = list(message.data)
        self.updateDatasVar(ite_list)

    def updateDatasVar(self, ite_list):
        self.iview.dvlc.Destroy()
        self.iview.InitUI()
        self.InitUI()

        for ite in ite_list:
            for var in inm().getVar(ite, self.iview.mode):
                self.iview.dvlc.AppendItem(var)


class ParallelDataObjPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test

        pub.subscribe(self.updateDatasPub, T.PARALLEL_UPDATE_ALL)

        self.InitUI()

    def InitUI(self):
        pa = ParallelAnalizerModel().getParallelAnalizerByIdTest(self.test.id)

        o_names = 'key,' + pa.order_name_obj
        columns = o_names.split(',')
        self.countColumn = len(columns)
        for name in columns:
            self.iview.dvlc.AppendTextColumn(name, width=150)

    def updateDatasPub(self, message):
        ite_list = list(message.data)
        self.updateDatas(ite_list)

    def updateDatas(self, ite_list):
        self.iview.dvlc.Destroy()
        self.iview.InitUI()
        self.InitUI()

        for ite in ite_list:
            for var in inm().getObj(ite, self.iview.mode):
                self.iview.dvlc.AppendItem(var)


class AddFilterObjetivesScrollPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        self.min_before = []
        self.max_before = []
        self.values = []

        pub.subscribe(self.updateDatasPub, T.PARALLEL_UPDATE_ALL)
        pub.subscribe(self.setFiltersNowPub, T.PARALLEL_ON_SET_FILTERS_OBJ)
        pub.subscribe(self.updateSortObjectPub,
                      T.PARALLEL_UPDATE_FIGURE_SORT_OBJ)
        pub.subscribe(self.setFiltersCleanPub, T.PARALLEL_ON_CLEAN_FILTERS_OBJ)
        pub.subscribe(self.updateRenameObjectPub,
                      T.PARALLEL_UPDATE_FIGURE_RENAME_OBJ)

    def updateDatasPub(self, message):
        ite_list = list(message.data)
        self.updateFiltros(ite_list)

    def setFiltersNowPub(self, message):
        if self.isFilterModified():
            pub.sendMessage(T.PARALLEL_SET_FILTERS_OBJ,
                            tuple(self.getListValues()))

    def setFiltersCleanPub(self, message):
        # if self.isFilterModified():
        pub.sendMessage(T.PARALLEL_UPDATE_FIGURE_LIST_OBJ)

    def updateSortObjectPub(self, message):
        tuple_names = message.data
        pub.sendMessage(T.PARALLEL_SET_FILTERS_OBJ,
                        tuple(self.getFiltersByNames(tuple_names)))

    def updateRenameObjectPub(self, message):
        pub.sendMessage(T.PARALLEL_SET_FILTERS_OBJ,
                        tuple(self.getListValues()))

    def updateFiltros(self, ite_list):

        # destruir el anterior
        if self.values != []:
            for aux in range(len(self.values)):
                self.values[aux].Destroy()
            self.values = []

        # filtro las variables correspondientes
        vmin, vmax = inm().getMinMax(ite_list[0], self.iview.mode)

        # obtengo los nombres
        pam = ParallelAnalizerModel()
        pa = pam.getParallelAnalizerByIdTest(self.test.id)
        names = pa.order_name_obj.split(',')

        # creo los filtros
        if len(names) == len(vmin):
            for index in range(len(names)):
                value = self.iview.addItem(vmin[index], vmax[index],
                                           names[index], vmin[index],
                                           vmax[index])
                self.values.append(value)

        # actualizo la vista
        self.iview.addSiserHere()
        self.updateBeforeValues()

    def isFilterModified(self):

        for index in range(len(self.values)):
            if self.values[index].getMinValue() != self.min_before[index]:
                return True
            if self.values[index].getMaxValue() != self.max_before[index]:
                return True
        return False

    def getListValues(self):
        min_list = []
        max_list = []
        for fil in self.values:
            min_list.append(fil.getMinValue())
            max_list.append(fil.getMaxValue())
        return max_list, min_list

    def updateBeforeValues(self):
        self.min_before = []
        self.max_before = []
        for value in self.values:
            self.min_before.append(value.getMinValue())
            self.max_before.append(value.getMaxValue())

    def getFiltersByNames(self, tuple_names):
        min_list = []
        max_list = []
        for name in tuple_names:
            for value in self.values:
                if name == value.name_objetive:
                    min_list.append(value.getMinValue())
                    max_list.append(value.getMaxValue())
                    break
        return max_list, min_list


def parallel_coordinatesTava(frame, class_column, len_color=1, pos_color=0,
                             ax=None, no_seque=True, is_use_legends=True,
                             cols=None, color=None, use_columns=False,
                             xticks=None, colormap=None, **kwds):
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
            raise ValueError('Columns must be numeric to be used as xticks')
        x = df.columns
    elif xticks is not None:
        if not np.all(np.isreal(xticks)):
            raise ValueError('xticks specified must be numeric')
        elif len(xticks) != ncols:
            raise ValueError('Length of xticks must match number of columns')
        x = xticks
    else:
        x = lrange(ncols)

    if ax is None:
        ax = plt.gca()

    color_values = _get_standard_colors(num_colors=len_color,
                                        colormap=colormap, color_type='random',
                                        color=color)

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

    if no_seque:
        for i in x:
            ax.axvline(i, linewidth=0.25, color='black')

    ax.set_xticks(x)
    ax.set_xticklabels(df.columns)
    ax.set_xlim(x[0], x[-1])
    ax.legend(loc='upper right')
    ax.grid()
    return ax
    # ------------------------------------------------------------------
