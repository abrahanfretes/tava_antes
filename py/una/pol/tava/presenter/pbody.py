'''
Created on 06/08/2014

@author: aferreira
'''
from wx.lib.pubsub import Publisher as pub
import topic as T
import py.una.pol.tava.view.vi18n as C
from wx import GetTranslation as _

from py.una.pol.tava.model.mtestdata import TestDataModel as tdm
from py.una.pol.tava.model.mtestdetail import TestDetailModel as tdem
from py.una.pol.tava.model.mresult import ResultModel as rm
from py.una.pol.tava.model.miteration import InterationModel as im
from py.una.pol.tava.model.mindividual import IndividualModel as inm

import os


class ProjectTreeNotebookPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.OnUpdateLabels, T.LANGUAGE_CHANGED)

    def OnUpdateLabels(self, message):
        self.iview .SetPageText(0, _(C.MP_PE))


class WorkingPagePresenter:
    def __init__(self, iview):
        self.iview = iview


class AUINotebookPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.AddPage, T.TESTCONFIG_ADD_PAGE)

    def AddPage(self, message):
        test = message.data
        files_path = self.createFileTest(test)

        #-----------------------------------------------------
        #Obtner Datos a partir de un TestConfig, y
        #Creacion del Formato que recibe un DataViewCtrl.
        #-----------------------------------------------------

        datas = {}
        if test != None:
            test_details = tdem().getTestDetailsByTestConfigId(test.id)
            for td in test_details:
                result = rm().getResultById(td.result_id)
                test_datas = tdm().getTestDatasByTestDetailId(td.id)
                for tdata in test_datas:
                    iteration = im().getIterationById(tdata.iteration_id)
                    datas[tdata.id] = (str(iteration.identifier), result.name)

        self.iview.OnAddPage(test.name, datas, files_path)

    def createFileTest(self, test):
        #--- creacion de archivos, un archivo por resultado

        #crea un directorio si no existe
        directory_temp = os.path.join(os.getcwd(), 'temp')
        if not os.path.isdir(directory_temp):
            os.mkdir(directory_temp)

        file_1 = directory_temp + '/vonLucken.csv'
        file_2 = directory_temp + '/vonLucken1.csv'
        files_path = []
        files_path_r = []
        files_path.append(file_1)
        files_path.append(file_2)
        files_path_r.append(file_1)
        files_path_r.append(file_2)

        #---------------------------------------------------
        #-----------------------------------------------------
        #Creacion de Test
        #-----------------------------------------------------

        if test != None:
            test_details = tdem().getTestDetailsByTestConfigId(test.id)
            for td in test_details:
                result = rm().getResultById(td.result_id)
                #-----------------------------------------
                f = open(files_path.pop(), 'w')
                header = result.name_objectives + ',Name\n'
                f.write(header)
                #-----------------------------------------
                test_datas = tdm().getTestDatasByTestDetailId(td.id)
                for tdata in test_datas:
                    itera = im().getIterationById(tdata.iteration_id)
                    #-----------------------------------------
                    individuals = inm().getIndividualsByIteracionId(itera.id)
                    for ind in individuals:
                        linea = ind.objectives +\
                            ',iter-' + str(itera.identifier) + '\n'
                        f.write(linea)
                    #-----------------------------------------
                #-----------------------------------------
                f.close()
                #-----------------------------------------
        return files_path_r
