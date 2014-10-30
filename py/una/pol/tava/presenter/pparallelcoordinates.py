'''
Created on 11/10/2014

@author: abrahan
'''

from py.una.pol.tava.model.mresult import ResultModel as rm
from py.una.pol.tava.model.miteration import InterationModel as im
from py.una.pol.tava.model.mindividual import IndividualModel as inm

import os

from pandas import read_csv
from pandas.tools.plotting import parallel_coordinates


class WorkingPagePresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test

        #crea un directorio si no existe
        self.path_test = self.getDirTest()

        # diccionario que contiene las iteraciones(id) con sus respectivos
        # path, de todos los resultados que contiene el test
        # {name.id:((id-ite1, path1), (id-ite2, path2), ...)}
        self.dic_path_iteration = {}

        #--- varaibles subplot ----------------------------------

        #contiene los items checkeados de la anterior grafica
        #Se utiliza para construir la lista de path para graficar
        #{u'vonLucken1.2': (24,), u'vonLucken.1': (21,)}
        self.dic_name_ite_checked_last_subplot = None

        #contiene el nombre del archivo a graficar y su path
        #self.dic_name_path_subplot =
        #{vonlucken.id:'/afretes/temp/test/file.csv'}
        self.dic_name_path_subplot = {}

        #--- varaibles figure ----------------------------------

        #contiene los items checkeados de la anterior grafica
        #Se utiliza para construir la lista de path para graficar
        #{u'vonLucken1.2': (24,), u'vonLucken.1': (21,)}
        self.dic_name_ite_checked_last_figure = None

        #contiene el nombre del archivo a graficar y su path
        #self.name_path_figure = '/afretes/temp/test/file.csv'
        self.name_path_figure = None

    #---- Funciones Generales -------------------------------------------------

    def  setDicIterationByResult(self):
        '''
        Establece el valor de la variable self.dic_path_iteration.
        Realiza las siguientes acciones:
        * Crea un archivo por cada iteracion de cada resultado del que se
        compone el test. El nombre de los archivos creados tiene el siguiente
        formato: idResult.nameResult.idIteration
        * genera un diccionario del tipo:
          {name.id:((id-ite1, path1), (id-ite2, path2), ...)}
        '''
        for t_detail in self.test.test_details:
            path_iteraciones = []
            result = rm().getResultById(t_detail.result_id)

            for t_data in t_detail.test_datas:
                itera = im().getIterationById(t_data.iteration_id)
                #-----------------------------------------
                filename = self.getFileNameForIte(
                                            result.id, result.name, itera.id)
                path_Ite = self.createFileIte(filename, itera)
                path_iteraciones.append(tuple([itera.id, path_Ite]))
            key_dic = result.name + '.' + str(result.id)
            self.dic_path_iteration[key_dic] = tuple(path_iteraciones)

    def createFileIte(self, filename, itera):
        f = open(filename, 'w')
        individuals = inm().getIndividualsByIteracionId(itera.id)
        for ind in individuals:
            linea = self.getLineIndividual(
                            ind.objectives, str(itera.identifier))
            f.write(linea)
        f.close()
        return filename

    #-------------------------------------------------------------------------

    #---- Funciones definidas para Parallel SubPlot ---------------------------

    def  updateDicCheckedLastSubplot(self, dic_checked_now):
        modified = dic_checked_now

        if self.dic_name_ite_checked_last_subplot != None:

            keys_less = sorted(self.dic_name_ite_checked_last_subplot.keys())
            keys_now = sorted(dic_checked_now.keys())

            for k_n in keys_now:
                if k_n in keys_less:
                    if self.dic_name_ite_checked_last_subplot[k_n] != \
                                                        dic_checked_now[k_n]:
                        self.dic_name_ite_checked_last_subplot[k_n] = \
                                                        dic_checked_now[k_n]
                    #sino, elimino de donde debo retornar
                    else:
                        del modified[k_n]
                    #si son iguales no se modifico por ende no agrego
                # si no existe lo agrego
                else:
                    #i no existe en el historico, lo actualizo
                    self.dic_name_ite_checked_last_subplot[k_n] = \
                                                        dic_checked_now[k_n]

            for k_l in keys_less:
                #si existe verifico que se haya modificado o no
                if k_l not in keys_now:
                    del self.dic_name_ite_checked_last_subplot[k_l]
        else:
            self.dic_name_ite_checked_last_subplot = modified

        return modified

    def setDicNameIteCheckedLastSubplot(self, dic):
        self.dic_name_ite_checked_last_subplot = dic

    def createFileForSubplot(self, new_items_checked):
        '''
        crea archivos por cada archivo resultado cuyas iteraciones son
        checkeadas
        '''
        dic_path = self.dic_path_iteration
        dir_result = self.path_test
        dic_temp = {}

        for key_name in list(new_items_checked.keys()):

            #crear nombre de archivo
            res = str(key_name).split('.')
            result_name, result_id = res[0], res[1]

            file_path = dir_result + '/' + result_name + '.csv'
            f_graphic = open(file_path, 'w')

            #Se agrega la cabecera
            result = rm().getResultById(result_id)
            line_header = result.name_objectives + ',Name\n'
            f_graphic.write(line_header)

            dic_existing = dict(list(dic_path[key_name]))

            #Se agrega el contenido
            for id_ite in new_items_checked[key_name]:
                ite = open(dic_existing[id_ite])
                f_graphic.write(ite.read())
                ite.close()
            f_graphic.close()

            dic_temp[key_name] = file_path
        self.dic_name_path_subplot = dic_temp

        return self.dic_name_path_subplot

    def  getLineIndividual(self, objetives, identifier):
        line = objetives + ',i-' + identifier + '\n'
        return line

    def  getDirTest(self):
        path_base = os.getcwd()
        path_temp = os.path.join('temp', self.test.name)
        path_test = os.path.join(path_base, path_temp)

        if not os.path.isdir(path_test):
            os.makedirs(path_test)

        return path_test

    def getNameFile(self, result_name):
        return os.path.join(self.path_test, result_name) + '.csv'

    def getFileNameForIte(self, resul_id, result_name, ite_id):
        file_path = str(resul_id) + '.' + result_name + '.' + str(ite_id)
        return os.path.join(self.path_test, file_path)

    #-------------------------------------------------------------------------

    #---- Funciones definidas para ParallelFigure sin SubPlot -----------------

    def  updateDicCheckedLastFigure(self, dic_checked_now):
        modified = dic_checked_now

        if self.dic_name_ite_checked_last_figure != None:

            keys_less = sorted(self.dic_name_ite_checked_last_figure.keys())
            keys_now = sorted(dic_checked_now.keys())

            for k_n in keys_now:
                if k_n in keys_less:
                    if self.dic_name_ite_checked_last_figure[k_n] != \
                                                        dic_checked_now[k_n]:
                        self.dic_name_ite_checked_last_figure[k_n] = \
                                                        dic_checked_now[k_n]
                    #sino, elimino de donde debo retornar
                    else:
                        del modified[k_n]
                    #si son iguales no se modifico por ende no agrego
                # si no existe lo agrego
                else:
                    #i no existe en el historico, lo actualizo
                    self.dic_name_ite_checked_last_figure[k_n] = \
                                                        dic_checked_now[k_n]

            for k_l in keys_less:
                #si existe verifico que se haya modificado o no
                if k_l not in keys_now:
                    del self.dic_name_ite_checked_last_figure[k_l]
        else:
            self.dic_name_ite_checked_last_figure = modified

        return modified

    def  setDicNameIteCheckedLastFigure(self, dic):
        self.dic_name_ite_checked_last_figure = dic

    def createFileForFigure(self, new_items_checked):
        '''
        crea un archivo con todas las iteraciones checkeadas de los diferentes
        archivos resultados, retorna un path del archivo creado.
        '''

        dic_path = self.dic_path_iteration
        dir_result = self.path_test

        file_path = dir_result + '/' + 'parallelfigure' + '.csv'
        f_graphic_parallel = open(file_path, 'w')

        #Se agrega la cabecera
        detail = self.test.test_details[0]
        result = rm().getResultById(detail.result_id)
        line_header = result.name_objectives + ',Name\n'

        f_graphic_parallel.write(line_header)

        for key_name in list(new_items_checked.keys()):

            dic_existing = dict(list(dic_path[key_name]))
            #Se agrega el contenido
            for id_ite in new_items_checked[key_name]:
                ite = open(dic_existing[id_ite])
                ite.readline()
                f_graphic_parallel.write(ite.read())
                ite.close()

        f_graphic_parallel.close()

        self.name_path_figure = file_path
        return file_path
    #------------------------------------------------------------------


class ParallelFigurePresenter:
    def __init__(self, iview):
        self.iview = iview

        #{nombre.id:cplot}
        self.dic_plot = {}
        #{nombre.id:axe}
        self.dic_axes = {}

    #---- Funciones Generales -------------------------------------------------
    def cleanParallelFigure(self):
        for axe in self.iview.figure.get_axes():
            print 'eliminando axes'
            self.iview.figure.delaxes(axe)

        self.dic_axes = {}
        self.iview.figure.clear()
        self.iview.canvas.draw()

    def  updateShowedFigure(self, value):
        self.showed_figure = value
    #-------------------------------------------------------------------------

    def createKeysForSubPlot(self, keys_result):
        print 'Entro en creacion de subplot'
        count_r = len(keys_result)
        print  'count: ', count_r
        c_plot = 100 * count_r + 11

        for key_name in keys_result:
            self.dic_plot[key_name] = c_plot
            c_plot += 1

        print  self.dic_plot

    # recibe del tipo {name.id: /algo/algo/algo.csv}
    def showSubplots(self, dic_for_plot):
        print dic_for_plot
        print  self.dic_plot
        keys_result = sorted(dic_for_plot.keys())

        for key_name in keys_result:
            df = read_csv(dic_for_plot[key_name])
            c_plot = self.dic_plot[key_name]
            axe = self.iview.figure.add_subplot(c_plot)
            axe = parallel_coordinates(df, 'Name', None, axe)
            self.dic_axes[key_name] = axe
            self.iview.canvas.draw()

    # recibe del tipo {name.id: /algo/algo/algo.csv}
    def  updateSubplots(self, dic_for_plot):

        keys_result_new = sorted(dic_for_plot.keys())
        keys_result_axe = sorted(self.dic_axes.keys())

        for key_name in keys_result_new:
            if key_name in keys_result_axe:
                axe_less = self.dic_axes[key_name]
                self.iview.figure.delaxes(axe_less)
                c_plot = self.dic_plot[key_name]
                axe = self.iview.figure.add_subplot(c_plot)

                df = read_csv(dic_for_plot[key_name])
                axe_new = parallel_coordinates(df, 'Name', None, axe)
                self.iview.canvas.draw()

                self.dic_axes[key_name] = axe_new
            else:
                df = read_csv(dic_for_plot[key_name])
                c_plot = self.dic_plot[key_name]
                axe = self.iview.figure.add_subplot(c_plot)
                axe = parallel_coordinates(df, 'Name', None, axe)
                self.dic_axes[key_name] = axe
                self.iview.canvas.draw()

    #---- Funciones definidas para ParallelFigure sin SubPlot -----------------

    def showParallelFigureUpdate(self, path_plot):

        if len(self.iview.figure.get_axes()):
            axe = self.iview.figure.get_axes()[0]
            self.iview.figure.delaxes(axe)
        self.showForParallelFigure(path_plot)

    def showForParallelFigure(self, path_plot):
        print 'in showForParallelFigure'
        df = read_csv(path_plot)
        axe = self.iview.figure.gca()
        axe = parallel_coordinates(df, 'Name', None, axe)
        self.iview.figure.suptitle('Hola Mundo')
        self.iview.canvas.draw()

    #------------------------------------------------------------------


#------------------- ParallelDataPresenter -----------------------------------
class ParallelDataPresenter:
    def __init__(self, iview):
        self.iview = iview

    def InitializeTree(self, test):
        if test != None:
            for t_detail in test.test_details:
                result = rm().getResultById(t_detail.result_id)
                td_item = self.iview.AddTestDetailNode(result.id, result.name)
                aux = t_detail.test_datas[-1]
                check = False
                for t_data in t_detail.test_datas:
                    if t_data == aux:
                        check = True
                    iteration = im().getIterationById(t_data.iteration_id)
                    self.iview.AddTestDataNode(td_item,
                                iteration.id, str(iteration.identifier), check)
                    check = False
            self.iview.SortChildren(self.iview.root)

    def expandItemTree(self):
        for item in self.iview.root.GetChildren():
            self.iview.Expand(item)

    def setGraphedList(self):
        to_ret = []
        for item_result in self.iview.root.GetChildren():
            for item_ite in item_result.GetChildren():
                if self.iview.IsItemChecked(item_ite):
                    to_ret.append(self.iview.GetItemPyData(item_ite))

        return sorted(to_ret)

    def getGraphedDictionary(self):
        to_ret = {}
        for item_result in self.iview.root.GetChildren():
            to_dicc = []
            for item_ite in item_result.GetChildren():
                if self.iview.IsItemChecked(item_ite):
                    to_dicc.append(self.iview.GetItemPyData(item_ite))
            key_dic = self.iview.GetItemText(item_result)\
                        + '.' + str(self.iview.GetItemPyData(item_result))
            to_ret[key_dic] = tuple(sorted(to_dicc))
        return to_ret
#------------------------------------------------------------------------------
