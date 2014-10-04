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

        self.iview.OnAddPage(test.name, datas)
