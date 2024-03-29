'''
Created on 06/08/2014

@author: aferreira
'''
from wx.lib.pubsub import Publisher as pub
import topic as T
import py.una.pol.tava.view.vi18n as C
from wx import GetTranslation as _


class ProjectTreeNotebookPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.OnUpdateLabels, T.LANGUAGE_CHANGED)

    def OnUpdateLabels(self, message):
        self.iview .SetPageText(0, _(C.MP_PE))


class AUINotebookPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.AddPage, T.TESTCONFIG_ADD_PAGE)

    def AddPage(self, message):
        tuple_test = message.data
        self.iview.OnAddPage(tuple_test[0], tuple_test[1])
