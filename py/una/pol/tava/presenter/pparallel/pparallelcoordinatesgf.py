'''
Created on 17/3/2015

@author: abrahan
'''
import wx
from wx.lib.pubsub import Publisher as pub
import topic as T

from py.una.pol.tava.model.mresult import ResultModel as rm
from py.una.pol.tava.model.miteration import InterationModel as itm
from py.una.pol.tava.model.mindividual import IndividualModel as inm

TYPE_TEST = 0
TYPE_RESULT = 1
TYPE_ITERATION = 2


class WorkingPageParallelGFPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.prepareFileForTestFigurePub,
                      T.PARALLEL_FIGURE_FILE_TEST_GRAFIC_GF)

        pub.subscribe(self.prepareFileForResultFigurePub,
                      T.PARALLEL_FIGURE_FILE_RESU_GRAFIC_GF)

        pub.subscribe(self.prepareFileForIterationFigurePub,
                      T.PARALLEL_FIGURE_FILE_ITER_GRAFIC_GF)

    def prepareFileForTestFigurePub(self, message):
        self.createFileForTest(message.data)
        pub.sendMessage(T.PARALLEL_FIGURE_VIEW_TEST_GRAFIC_GF, message.data)

    def prepareFileForResultFigurePub(self, message):
        self.createFileForResult(message.data)
        pub.sendMessage(T.PARALLEL_FIGURE_VIEW_RESULT_GRAFIC_GF, message.data)

    def prepareFileForIterationFigurePub(self, message):
        self.createFileForIteration(message.data)
        pub.sendMessage(T.PARALLEL_FIGURE_VIEW_ITERA_GRAFIC_GF, message.data)

    def createFileForTest(self, ite_list):
        inm().createFileTestGF(ite_list)

    def createFileForResult(self, ite_list):
        inm().createFileResultGF(ite_list)

    def createFileForIteration(self, ite_list):
        inm().createFileIterationtGF(ite_list)


class ParallelTreeGFPresenter:
    def __init__(self, iview, test):

        self.iview = iview
        self.test = test
        self.root = self.iview.AddRoot("Test Data")
        self.checkeds_last = []
        self.less_type_gf = None

        pub.subscribe(self.prepareTestFigurePub,
                      T.PARALLEL_FIGURE_BUTTON_TEST_GRAFIC_GF)
        pub.subscribe(self.prepareResultFigurePub,
                      T.PARALLEL_FIGURE_BUTTON_RESU_GRAFIC_GF)
        pub.subscribe(self.prepareIteraFigurePub,
                      T.PARALLEL_FIGURE_BUTTON_ITER_GRAFIC_GF)

        # inicializamos el arbol
        for detail in test.test_details:
            r_name = rm().getNameById(detail.result_id)
            td_item = self.iview.AppendItem(self.root, r_name)
            self.iview.SetItemPyData(td_item, '')
            self.iview.SetItemImage(td_item, 0, wx.TreeItemIcon_Normal)

            for data in detail.test_datas:
                idn = str(itm().getIdentifierById(data.iteration_id))
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

    def isChangeChecked(self):
        aux = sorted(self.getListChecked())
        if self.checkeds_last != aux:
            self.checkeds_last = aux
            return True
        return False

    def getListChecked(self, true=True):
        to_dicc = []
        for item_result in self.root.GetChildren():
            for item_ite in item_result.GetChildren():
                if true == self.iview.IsItemChecked(item_ite):
                    to_dicc.append(self.iview.GetItemPyData(item_ite))
        return to_dicc

    def getListCheckedForResult(self, true=True):
        r_list = []
        for item_result in self.root.GetChildren():
            i_list = []
            for item_ite in item_result.GetChildren():
                if true == self.iview.IsItemChecked(item_ite):
                    i_list.append(self.iview.GetItemPyData(item_ite))
            r_list.append(i_list)
        return r_list

    def getLenListChecked(self):
        return len(self.getListChecked())

    def getCorrectCountChecked(self):
        list_checked = self.getLenListChecked()
        return (list_checked > 0 and list_checked < 5)

    def setCheckedGF(self):
        pub.sendMessage(T.PARALLEL_FIGURE_TREE_CHECK_GF,
                        self.getCorrectCountChecked())

    def prepareTestFigurePub(self, message):
        if self.canSendMessage(message.data):
            pub.sendMessage(T.PARALLEL_FIGURE_FILE_TEST_GRAFIC_GF,
                            tuple(self.getListChecked()))

    def prepareResultFigurePub(self, message):
        if self.canSendMessage(message.data):
            pub.sendMessage(T.PARALLEL_FIGURE_FILE_RESU_GRAFIC_GF,
                            tuple(self.getListCheckedForResult()))

    def prepareIteraFigurePub(self, message):
        if self.canSendMessage(message.data):
            pub.sendMessage(T.PARALLEL_FIGURE_FILE_ITER_GRAFIC_GF,
                            tuple(self.getListChecked()))
            pass

    def canSendMessage(self, type_gf):
        if(self.less_type_gf != type_gf):
            self.less_type_gf = type_gf
            return True
        return self.isChangeChecked()

from pandas.tools.plotting import parallel_coordinates


class ParallelFigureGFPresenter:
    def __init__(self, iview, test):
        self.iview = iview

        self.test = test

        pub.subscribe(self.prepareViewTestFigurePub,
                      T.PARALLEL_FIGURE_VIEW_TEST_GRAFIC_GF)

        pub.subscribe(self.prepareViewResultFigurePub,
                      T.PARALLEL_FIGURE_VIEW_RESULT_GRAFIC_GF)

        pub.subscribe(self.prepareViewIterationFigurePub,
                      T.PARALLEL_FIGURE_VIEW_ITERA_GRAFIC_GF)

    def prepareViewTestFigurePub(self, message):
        self.cleanParallelFigure()
        axe = self.iview.figure.gca()
        df = inm().getCsvForTest()
        axe = parallel_coordinates(df, 'Name', ax=axe)
        self.iview.canvas.draw()

    def prepareViewResultFigurePub(self, message):

        ite_list = message.data
        self.cleanParallelFigure()

        count_r = len(ite_list)
        axe_plot = 100 * count_r + 11

        for i_list in ite_list:
            axe = self.iview.figure.add_subplot(axe_plot)
            df = inm().getCsvForResult(i_list)
            axe = parallel_coordinates(df, 'Name', ax=axe)
            self.iview.canvas.draw()
            axe_plot += 1

    def prepareViewIterationFigurePub(self, message):

        ite_list = message.data
        self.cleanParallelFigure()

        count_r = len(ite_list)
        axe_plot = 100 * count_r + 11

        for iteration in ite_list:
            axe = self.iview.figure.add_subplot(axe_plot)
            df = inm().getCsvForIteration(iteration)
            axe = parallel_coordinates(df, 'Name', ax=axe)
            self.iview.canvas.draw()
            axe_plot += 1

    def cleanParallelFigure(self):
        for axe in self.iview.figure.get_axes():
            self.iview.figure.delaxes(axe)


class ButtonsTollFigureGFPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.checkedTreePub, T.PARALLEL_FIGURE_TREE_CHECK_GF)
        self.setEnable(False)

    def checkedTreePub(self, message):
        self.setEnable(message.data)

    def setEnable(self, enable):
        if enable:
            self.enableButtons()
        else:
            self.disableButtons()

    def enableButtons(self):
        self.iview.test.Enable()
        self.iview.result.Enable()
        self.iview.iteration.Enable()

    def disableButtons(self):
        self.iview.test.Disable()
        self.iview.result.Disable()
        self.iview.iteration.Disable()

    def testGrafic(self):
        pub.sendMessage(T.PARALLEL_FIGURE_BUTTON_TEST_GRAFIC_GF, TYPE_TEST)

    def resultGrafic(self):
        pub.sendMessage(T.PARALLEL_FIGURE_BUTTON_RESU_GRAFIC_GF, TYPE_RESULT)

    def iterationGrafic(self):
        pub.sendMessage(T.PARALLEL_FIGURE_BUTTON_ITER_GRAFIC_GF,
                        TYPE_ITERATION)
