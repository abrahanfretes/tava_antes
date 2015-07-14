'''
Created on 05/08/2014

@author: aferreira
'''
from wx.lib.pubsub import Publisher as pub
import topic as T


class MainMenuBarPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.UpdateLabelsPub, T.LANGUAGE_CHANGED)

    def SelectEnglishLanguage(self):
        pub.sendMessage(T.ENGLISH_SELECTED)

    def SelectSpanishLanguage(self):
        pub.sendMessage(T.SPANISH_SELECTED)

    def ShowProperties(self):
        pub.sendMessage(T.PROJECT_PROPERTIES)

    def UpdateLabelsPub(self, message):
        self.iview.SetLabels()


class AnalysisPackageMenuPresenter:
    def __init__(self, iview):
        self.iview = iview

    def ShowGraphicWizard(self):
        pub.sendMessage(T.GRAPHIC_WIZARD)


class AnalysisMenuPresenter:
    def __init__(self, iview):
        self.iview = iview

    def ShowGraphic(self, type_g):
        test = self.iview.test
        pub.sendMessage(T.TESTCONFIG_ADD_PAGE, (test, type_g))

    def OnShowGraphsAndData(self, type_g):
        test = self.iview.test
        pub.sendMessage(T.TESTCONFIG_ADD_PAGE, (test, type_g))


class MetricTestPackageMenuPresenter:
    def __init__(self, iview):
        self.iview = iview

    def ShowGraphicWizard(self):
        pub.sendMessage(T.METRIC_WIZARD)


class TestMetricMenuPresenter:
    def __init__(self, iview):
        self.iview = iview

    def Show(self, type_g):
        test = self.iview.test
        pub.sendMessage(T.TESTCONFIG_ADD_PAGE, (test, type_g))

    def ShowSing(self, type_g):
        test = self.iview.test
        pub.sendMessage(T.TESTCONFIG_ADD_PAGE, (test, type_g))
