'''
Created on 11/10/2014

@author: abrahan
'''
from py.una.pol.tava.model.mtestdata import TestDataModel as tdm
from py.una.pol.tava.model.mtestdetail import TestDetailModel as tdem
from py.una.pol.tava.model.mresult import ResultModel as rm
from py.una.pol.tava.model.miteration import InterationModel as im
from py.una.pol.tava.model.mindividual import IndividualModel as inm

import os


class WorkingPagePresenter:
    def __init__(self, iview):
        self.iview = iview
        self.test = self.iview.test
        #crea un directorio si no existe
        self.path_test = self.getDirTest()
        self.list_path = []
        #crea los archivos para el test
        #self.createFileForParallel(self.path_test)

    def createFileForParallel(self):

        if self.test != None:
            for test_detail in self.test.test_details:
                result = rm().getResultById(test_detail.result_id)
                file_tets = self.getNameFile(result.name)
                self.list_path.append(file_tets)
                #------------------------------------------
                f = open(file_tets, 'w')
                header = result.name_objectives + ',Name\n'
                f.write(header)
                #------------------------------------------
                for test_data in test_detail.test_datas:
                    itera = im().getIterationById(test_data.iteration_id)
                    #-----------------------------------------
                    individuals = inm().getIndividualsByIteracionId(itera.id)
                    for ind in individuals:
                        linea = self.getLineIndividual(
                                        ind.objectives, str(itera.identifier))
                        f.write(linea)
                    #-----------------------------------------
                #-----------------------------------------
                f.close()
                #-----------------------------------------
        return self.list_path

    def  getLineIndividual(self, objetives, identifier):
        line = objetives + ',iter-' + identifier + '\n'
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


class ParallelDataPresenter:
    def __init__(self, iview):
        self.iview = iview

    def InitializeTree(self, test):
        if test != None:
            test_details = tdem().getTestDetailsByTestConfigId(test.id)
            for td in test_details:
                result = rm().getResultById(td.result_id)
                td_item = self.iview.AddTestDetailNode(td, result.name)
                test_datas = tdm().getTestDatasByTestDetailId(td.id)
                for tdata in test_datas:
                    iteration = im().getIterationById(tdata.iteration_id)
                    self.iview.AddTestDetaNode(td_item,
                                tdata, str(iteration.identifier))


class ParallelFigurePresenter:
    def __init__(self, iview):
        self.iview = iview
        self.test = self.iview.test
        self.list_path = self.iview.list_path

    def  initializeFigure(self):
        #----------
        count_r = len(self.list_path)
        self.c_plot = 100 * count_r + 11

        for i in range(count_r):
            self.iview.ShowParallelCoordinates(
                                    self.list_path[i], self.c_plot)
            self.c_plot += 1
        #----
