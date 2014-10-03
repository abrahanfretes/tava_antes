'''
Created on 06/08/2014

@author: aferreira
'''
from wx.lib.pubsub import Publisher as pub
import topic as T
import py.una.pol.tava.view.vi18n as C
from wx import GetTranslation as _

from py.una.pol.tava.model.mtestdata import TestDataModel as tdm


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

        #test = tm().getTestConfigById(1)
        test_data = []
        datas = {}

        if test != None:
            test_data = tdm().getTestDatasByTestConfig(test)

        for tdata in test_data:
            datas[tdata.id] = (str(tdata.iteration_identifier),
                               tdata.name_result)

        self.iview.OnAddPage(test.name, datas)
