'''
Created on 18/11/2014

@author: abrahan
'''

from py.una.pol.tava.model.mresult import ResultModel as rm
from py.una.pol.tava.model.miteration import InterationModel as im
from py.una.pol.tava.model.mindividual import IndividualModel as inm

from py.una.pol.tava.presenter.pparallelcoordinates import\
                                                    parallel_coordinatesTava

import os
import tempfile
from pandas import read_csv

TEMP_FILE = 'temp'


class WorkingPageDataPresenter:
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

        self.dictObjetiveMinMax = {}
        self.dictObjetiveMinMaxTem = {}

        self.dictIterationId = {}

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
        lh_obj = r.name_objectives + ',Name\n'
        lh_var = r.name_variables
        #Se crea un nombre por cada resultado
        index_f = 1
        for t_detail in self.test.test_details:
            list_iteraciones = []
            r = rm().getResultById(t_detail.result_id)
            #Se crea un archivo por cada iteracion
            for t_data in t_detail.test_datas:
                i = im().getIterationById(t_data.iteration_id)
                idn = i.identifier
                filename = r.name + '.' + str(idn) + '.csv'
                filename_var = r.name + '.' + str(idn)
                self._createTempFileObj(filename, idn, i.id, index_f, lh_obj)
                self._createTempFileVar(filename_var, i.id, lh_var)
                list_iteraciones.append(filename)
                self.dictIterationId[filename] = i.id
            key_dic = 'f' + str(index_f) + '-' + r.name
            self.main_dic[key_dic] = tuple(list_iteraciones)
            index_f += 1

        return self.main_dic

    def _createTempFileObj(self, filename, ite_iden, ite_id, idx_f, lh_obj):
        line_aux = ',f' + str(idx_f) + '-' + 'i' + str(ite_iden) + '\n'
        filepath = os.path.join(self.test_path, filename)
        f = open(filepath, 'w')
        f.write(lh_obj)
        individuals = inm().getIndividualsByIteracionId(ite_id)

        listMinObjetive = []
        listMaxObjetive = []

        for ind in individuals:
            linea = ind.objectives + line_aux
            f.write(linea)

            #se busca los objetivos minimos y maximos
            if listMinObjetive != []:
                index = 0
                for obj_aux in ind.objectives.split(','):

                    if float(obj_aux) < listMinObjetive[index]:
                        listMinObjetive[index] = float(obj_aux)

                    if float(obj_aux) > listMaxObjetive[index]:
                        listMaxObjetive[index] = float(obj_aux)
                    index += 1
            else:
                for obj_aux in ind.objectives.split(','):
                    listMinObjetive.append(float(obj_aux))
                    listMaxObjetive.append(float(obj_aux))

        f.close()

        listKey = lh_obj.split(',')
        dic_aux = {}
        for index in range(len(listMinObjetive)):
            dic_aux[listKey[index]] = (listMinObjetive[index],
                                                       listMaxObjetive[index])

        self.dictObjetiveMinMax[filename] = dic_aux
        self.dictObjetiveMinMaxTem[filename] = dic_aux
        return filename

    def _createTempFileVar(self, filename, ite_id, lh_var):
        filepath = os.path.join(self.test_path, filename)
        f = open(filepath, 'w')
        #f.write('key,' + lh_var + '\n')
        individuals = inm().getIndividualsByIteracionId(ite_id)
        for ind in individuals:
            linea = str(ind.id) + ',' + ind.variables
            f.write(linea + '\n')
        f.close()
        return filename

    def  _createTempDirectoryTest(self):
        #path_base = os.getcwd()
        path_base = tempfile.gettempdir()
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

    def  getFileForIndividual(self, id_individual):
        name = 'individual.' + str(id_individual) + '.csv'
        name_f = ', o-' + str(id_individual)
        r = rm().getResultById(self.test.test_details[0].result_id)
        header = r.name_objectives + ',Name\n'
        value = inm().getObjectivesIndividualById(id_individual) + name_f
        i_path = os.path.join(self.test_path, name)

        fileopen = open(i_path, 'w')
        fileopen.write(header)
        fileopen.write(value)
        fileopen.close()

        return name

    def getNameVariables(self):
        #se crea el archivo con solo cabecera
        r = rm().getResultById(self.test.test_details[0].result_id)
        name_variables = r.name_variables
        return name_variables
    #-------------------------------------------------------------------------

#------------------- ParallelDataFigurePresenter ------------------------------
    def updateForFilters(self, filtros, filename):

        #ordenar la lista de acuerdo al archivo
        filepath = os.path.join(self.test_path, filename)
        filepath_var = os.path.join(self.test_path, filename[:-4])

        f = open(filepath)
        header = f.readline()
        line_aux = ',' + f.readline().split(',')[-1]
        f.close()

        min_o = []
        max_o = []
        listMinObjetive = []
        listMaxObjetive = []

        for key in header.split(',')[:-1]:
            t_values = filtros[key]
            min_o.append(t_values[0])
            max_o.append(t_values[1])
            listMinObjetive.append(t_values[0])
            listMaxObjetive.append(t_values[1])

        #obtener los individuos a filtrar

        f = open(filepath, 'w')
        f.write(header)
        f_var = open(filepath_var, 'w')

        ite_id = self.dictIterationId[filename]
        individuals = inm().getIndividualsByIteracionId(ite_id)

        key_id = 0
        for ind in individuals:

            #objetivos filtrados
            c_obj = ind.objectives.split(',')
            to_write = True
            for i in range(len(c_obj)):

                if float(c_obj[i]) < min_o[i] or float(c_obj[i]) > max_o[i]:
                    to_write = False
                    break
            if(to_write):

                linea = ind.objectives + line_aux
                f.write(linea)
                linea_var = str(ind.id) + ',' + ind.variables + '\n'
                f_var.write(linea_var)
                key_id += 1

                #se busca los objetivos minimos y maximos
                if listMinObjetive != []:
                    index = 0
                    for obj_aux in ind.objectives.split(','):
                        if float(obj_aux) < listMinObjetive[index]:
                            listMinObjetive[index] = float(obj_aux)
                        if float(obj_aux) >= listMaxObjetive[index]:
                            listMaxObjetive[index] = float(obj_aux)
                        index += 1
            else:
                to_write = True

        f.close()
        f_var.close()

        #actualizacion de filtros
        key_list = header.split(',')[:-1]
        dic_aux = {}
        for index in range(len(listMinObjetive)):
            dic_aux[key_list[index]] = (listMinObjetive[index],
                                                       listMaxObjetive[index])

        f.close()
        #self.dictObjetiveMinMax[filename] = filtros
        self.dictObjetiveMinMaxTem[filename] = dic_aux


class ParallelDataFigurePresenter:
    def __init__(self, iview, dir_path):
        self.iview = iview

        self.dir_path = dir_path
        self.figure_axes = None
        self.individual_axes = None

    #---- Funciones Generales -------------------------------------------------
    def cleanParallelFigure(self):
        if self.figure_axes != None:
            self.iview.figure.delaxes(self.figure_axes)
            self.figure_axes = None
        if self.individual_axes != None:
            self.iview.figure.delaxes(self.individual_axes)
            self.individual_axes = None

        self.iview.canvas.draw()
        self.iview.figure.clear()

    #-------------------------------------------------------------------------

    #---- Funciones definidas para ParallelFigure Test ------------------------
    def newFigureTest(self, list_plot, suptitle=''):
        self.figure_axes = self._initFigurePaint(list_plot, suptitle, 211)

    #--------------------------------------------------------------------------

    #---- Funciones definidas para ParallelFigure Individual ------------------
    def newFigureIndividual(self, filename, suptitle=''):
        if self.individual_axes != None:
            self.iview.figure.delaxes(self.individual_axes)
        self.individual_axes = self._initFigurePaint([filename], suptitle, 212)
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
    #--------------------------------------------------------------------------
