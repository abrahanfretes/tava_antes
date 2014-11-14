'''
Created on 11/10/2014

@author: abrahan
'''

from py.una.pol.tava.model.mresult import ResultModel as rm
from py.una.pol.tava.model.miteration import InterationModel as im
from py.una.pol.tava.model.mindividual import IndividualModel as inm

import os
from pandas import read_csv

ONLY_HEADER_FILE = 'onlyheaderfile.csv'
TEMP_FILE = 'temp'


class WorkingPagePresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test

        #crea un directorio si no existe
        self.test_path = self._createTempDirectoryTest()

        '''
        diccionario que contiene como clave: la letra 'f' concatenado con un
        index y con el nombre de un archivo resultado, y como valor, una tupla
        con los nombres de archivos temporales creados por cada iteracion.
        formato={f_idx-name:(file1name.csv, ...)}
        '''
        self.main_dic = {}

    #---- Funciones Generales -------------------------------------------------

    def  setDicIterationByResult(self):
        '''
        Realiza las siguientes acciones:
        -------------------------------

        Establece el valor de la variable self.main_dic.
        Genera un archivo por iteracion.
        '''

        #se crea el archivo con solo cabecera
        r = rm().getResultById(self.test.test_details[0].result_id)
        line_h = r.name_objectives + ',Name\n'
        #Se crea un nombre por cada resultado
        index_file = 1
        for t_detail in self.test.test_details:
            list_iteraciones = []
            r = rm().getResultById(t_detail.result_id)
            #Se crea un archivo por cada iteracion
            for t_data in t_detail.test_datas:
                i = im().getIterationById(t_data.iteration_id)
                idn = i.identifier
                filename = r.name + '.' + str(idn) + '.csv'
                self._createTempFile(filename, idn, i.id, index_file, line_h)
                list_iteraciones.append(filename)
            key_dic = 'f' + str(index_file) + '-' + r.name
            self.main_dic[key_dic] = tuple(list_iteraciones)
            index_file += 1

        return self.main_dic

    def _createTempFile(self, filename, ite_iden, ite_id, idx_f, line_header):
        line_aux = ',f' + str(idx_f) + '-' + 'i' + str(ite_iden) + '\n'
        filepath = os.path.join(self.test_path, filename)
        f = open(filepath, 'w')
        f.write(line_header)
        individuals = inm().getIndividualsByIteracionId(ite_id)
        for ind in individuals:
            linea = ind.objectives + line_aux
            f.write(linea)
        f.close()
        return filename

    def  _createTempDirectoryTest(self):
        path_base = os.getcwd()
        path_temp = os.path.join(TEMP_FILE, self.test.name)
        path_test = os.path.join(path_base, path_temp)
        if not os.path.isdir(path_test):
            os.makedirs(path_test)
        return path_test

    def getListByDic(self, dic_aux):
        list_aux = []
        for key in sorted(dic_aux.keys()):
            list_aux.append(dic_aux[key])
        return sorted(list_aux)
    #-------------------------------------------------------------------------


#------------------- ParallelDataOptionsPresenter -----------------------------
class ParallelDataOptionsPresenter:
    def __init__(self, iview):
        self.iview = iview


#------------------- ParallelFigurePresenter ----------------------------------
class ParallelFigurePresenter:
    def __init__(self, iview, dir_path):
        self.iview = iview

        self.dir_path = dir_path
        self.axe_test = None
        self.axe_result = {}
        self.splot_result = {}

    #---- Funciones Generales -------------------------------------------------
    def cleanParallelFigure(self):
        for axe in self.iview.figure.get_axes():
            self.iview.figure.delaxes(axe)

        self.axe_result = {}
        self.axe_iteration = {}
        self.iview.figure.clear()
        self.iview.canvas.draw()

    def initializeFigureResult(self, keys_result):
        count_r = len(keys_result)
        c_plot = 100 * count_r + 11

        for key_name in keys_result:
            self.splot_result[key_name] = c_plot
            self.axe_result[key_name] = None
            c_plot += 1
    #-------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    #    Funciones especificas para cada tipo de grafico
    #--------------------------------------------------------------------------

    #---- Funciones definidas para ParallelFigure Test ------------------------
    def newFigureTest(self, list_plot, suptitle=''):
        self.axe_test = self._initFigurePaint(list_plot, suptitle)

    def updateFigureTest(self, current_plot, last_plot):
        axe = self.axe_test
        self.axe_test = self._updateFigurePaint(current_plot, last_plot, axe)

    #---- Funciones definidas para ParallelFigure Result ----------------------
    def newFigureResult(self, dic_plot):
        keys_result = sorted(dic_plot.keys())

        for key_r in keys_result:
            list_plot = list(dic_plot[key_r])
            sp_axe = self.splot_result[key_r]
            axe = self._initFigurePaint(list_plot, 'suptitle', sp_axe)
            self.axe_result[key_r] = axe

    def  updateFigureResult(self, current_plot, last_plot):

        for key_r in list(sorted(current_plot.keys())):
            axe = self.axe_result[key_r]
            if axe != None:
                li_plot = list(current_plot[key_r])
                la_plot = list(last_plot[key_r])
                sp_axe = self.splot_result[key_r]
                axe = self._updateFigurePaint(li_plot, la_plot, axe, sp_axe)
            else:
                list_plot = list(current_plot[key_r])
                sp_axe = self.splot_result[key_r]
                axe = self._initFigurePaint(list_plot, 'suptitle', sp_axe)
            self.axe_result[key_r] = axe

    #---- Funciones definidas para ParallelFigure Iteration -----------------
    def newFigureIteration(self, list_plot):
        count_r = len(list_plot)
        c_plot = 100 * count_r + 11

        for name_i in list_plot:
            sp_axe = c_plot
            self._initFigurePaint([name_i], 'suptitle', sp_axe)
            c_plot += 1

    #---- Funciones definidas para ParallelFigure Sequential -----------------
    def newFigureSequential(self, i_name):

        self.cleanParallelFigure()
        i_path = os.path.join(self.dir_path, i_name[0])
        axe = self.iview.figure.gca()
        self.iview.figure.suptitle('Hola Mundo')

        fileopen = open(i_path)
        cabecera = fileopen.readline()
        line = fileopen.readline()
        name_auxf = 'parallelSec1.csv'

        if line != '':
            file_aux = open(name_auxf, 'w')
            file_aux.write(cabecera)
            file_aux.write(line)
            file_aux.close()

            df = read_csv(name_auxf)
            axe = parallel_coordinatesTava(df, 'Name', 1, 0, axe)
            self.iview.canvas.draw()
            line = fileopen.readline()

        while line != '':

            file_aux = open(name_auxf, 'w')
            file_aux.write(cabecera)
            file_aux.write(line)
            file_aux.close()

            df = read_csv(name_auxf)
            axe = parallel_coordinatesTava(df, 'Name', 1, 0, axe, False, False)

            axe.grid(b=True)
            self.iview.canvas.draw()
            line = fileopen.readline()
        fileopen.close()

        if os.path.isfile(name_auxf):
            os.remove(name_auxf)
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    #    Funciones Bases o comunes para todos los tipos de grafico
    #--------------------------------------------------------------------------
    def _initFigurePaint(self, list_plot, suptitle='', sp_axe=None):
        axe = None
        if sp_axe == None:
            axe = self.iview.figure.gca()
        else:
            axe = self.iview.figure.add_subplot(sp_axe)
        self.iview.figure.suptitle(suptitle)
        axe = self._figurePaint(axe, list_plot)
        return axe

    def _updateFigurePaint(self, current_plot, last_plot, axe, sp_axe=None):
        if self._isOnlyAdd(current_plot, last_plot):
            list_plot = []
            for c_ite in current_plot:
                if not (c_ite in last_plot):
                    list_plot.append(c_ite)
            axe = self._figurePaint(axe, list_plot, len(last_plot))
        else:
            self.iview.figure.delaxes(axe)
            axe = self._initFigurePaint(current_plot, sp_axe=sp_axe)
        return axe

    def _figurePaint(self, axe, list_plot, count_last=0):
        _pos = 0 + count_last
        _len = len(list_plot) + count_last
        for i_name in list_plot:
            i_path = os.path.join(self.dir_path, i_name)
            df = read_csv(i_path)
            axe = parallel_coordinatesTava(df, 'Name', _len, _pos, axe)
            axe.grid(b=True)
            self.iview.canvas.draw()
            _pos += 1
        self.iview.canvas.draw()
        return axe

    def  _isOnlyAdd(self, current_plot, last_plot):
        for l_ite in last_plot:
            if not (l_ite in current_plot):
                return False
        return True
    #--------------------------------------------------------------------------


def parallel_coordinatesTava(frame, class_column, len_color=1, pos_color=0,
    ax=None, no_seque=True, is_use_legends=True, cols=None, color=None,
                use_columns=False, xticks=None, colormap=None, **kwds):
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
    #------------------------------------------------------------------


#------------------- ParallelDataPresenter -----------------------------------
class ParallelDataPresenter:
    def __init__(self, iview):
        self.iview = iview

    def InitializeTree(self, main_dic):

        for r_name in sorted(main_dic.keys()):
            r_item = self.iview.AddTestDetailNode('', r_name)
            for i_name in main_dic[r_name]:
                idn = i_name.split('.')[-2]
                self.iview.AddTestDataNode(r_item, i_name, idn, True)

        self.iview.SortChildren(self.iview.root)

    def expandItemTree(self):
        for item in self.iview.root.GetChildren():
            self.iview.Expand(item)

    def getGraphedList(self):
        to_ret = []
        for item_result in self.iview.root.GetChildren():
            for item_ite in item_result.GetChildren():
                if self.iview.IsItemChecked(item_ite):
                    to_ret.append(self.iview.GetItemPyData(item_ite))

        return sorted(to_ret)

    def getCurrentListChecked(self, true):
        to_dicc = []
        for item_result in self.iview.root.GetChildren():
            for item_ite in item_result.GetChildren():
                if true == self.iview.IsItemChecked(item_ite):
                    to_dicc.append(self.iview.GetItemPyData(item_ite))
        return to_dicc

    def getCurrentDicChecked(self, true):
        to_ret = {}
        for item_result in self.iview.root.GetChildren():
            to_dicc = []
            for item_ite in item_result.GetChildren():
                if true == self.iview.IsItemChecked(item_ite):
                    to_dicc.append(self.iview.GetItemPyData(item_ite))
            key_dic = self.iview.GetItemText(item_result)
            to_ret[key_dic] = tuple(sorted(to_dicc))
        return to_ret
#------------------------------------------------------------------------------
