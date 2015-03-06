'''
Created on 25/2/2015

@author: abrahan
'''
import wx
from wx.lib.pubsub import Publisher as pub
import topic as T

from py.una.pol.tava.model.mresult import ResultModel as rm
from py.una.pol.tava.model.miteration import InterationModel as im
from py.una.pol.tava.model.mindividual import IndividualModel as inm
from py.una.pol.tava.model.mparallel_analizer import ParallelAnalizerModel

from py.una.pol.tava.presenter.pparallelcoordinates import\
    parallel_coordinatesTava


class TopPanelPresenter:
    def __init__(self, iview, test, mode):
        self.iview = iview
        self.test = test
        self.mode = mode

        pub.subscribe(self.updateConfigPAPub, T.PARALLELANALIZER_UPDATE_FIGURE)
        pub.subscribe(self.updateFigurePub, T.PARALLEL_UPDATE_FIGURE)
        pub.subscribe(self.updateListObjetivesPub,
                      T.PARALLEL_UPDATE_FIGURE_LIST_OBJ)

    # ---- Funciones Generales ------------------------------------------------
    def updateConfigPAPub(self, message):
        self.iview.upDateGrafic(True)

    def updateListObjetivesPub(self, message):
        self.fileDelete(self.iview.getCurrentIteChecked())
        self.iview.upDateGrafic(True)

    def updateFigurePub(self, message):
        self.iview.upDateGrafic()

    def fileExists(self, ite):
        return inm().fileExists(ite, self.mode)

    def fileDelete(self, ite):
        return inm().fileDelete(ite, self.mode)

    def createFiles(self, ite):
        pam = ParallelAnalizerModel()
        p_analizer = pam.getParallelAnalizerByIdTest(self.test.id)
        return inm().createFiles(ite, self.mode, p_analizer.enable_objectives,
                                 p_analizer.order_objective)

    def createFilesWithFilter(self, ite, filters):
        return inm().createFilesWithFilter(ite, self.mode, filters)

    def deleteFile(self, ite):
        return inm().deleteFile(ite, self.mode)
    # -------------------------------------------------------------------------


# ------------------- ParallelDataPresenter -----------------------------------
class ParallelDataTreePresenter:
    def __init__(self, iview, test_details):

        self.iview = iview
        self.root = self.iview.AddRoot("Test Data")

        # ultimas iteraciones checkeadas ParallelFigure Test
        self.checkeds_last = []

        self.InitUI(test_details)
        # ------------------------------------------------------------

        #  Inicializacion del arbol de proyectos
    def InitUI(self, details):

        # inicializamos el arbol
        for detail in details:
            r_name = rm().getNameById(detail.result_id)
            td_item = self.iview.AppendItem(self.root, r_name)
            self.iview.SetItemPyData(td_item, '')
            self.iview.SetItemImage(td_item, 0, wx.TreeItemIcon_Normal)

            for data in detail.test_datas:
                idn = str(im().getIdentifierById(data.iteration_id))
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

    def getListChecked(self, true=True):
        to_dicc = []
        for item_result in self.root.GetChildren():
            for item_ite in item_result.GetChildren():
                if true == self.iview.IsItemChecked(item_ite):
                    to_dicc.append(self.iview.GetItemPyData(item_ite))
        return to_dicc

    def getLenListChecked(self):
        return len(self.getListChecked())

    def isChangeChecked(self):
        aux = sorted(self.getListChecked())
        if self.checkeds_last != aux:
            self.checkeds_last = aux
            return True
        return False

    def setChecked(self):
        pub.sendMessage(T.PARALLEL_TREE_CHECK_FIGURE, self.getOneChecked())

    def getOneChecked(self):
        return 1 == self.getLenListChecked()

# ------------------------------------------------------------------------------


class ParallelDataFigurePresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        self.figure_axes = None

        self.parallel_analizer = self.initParallelAnalizer()
        self.customizeFigure()

    # ---- Funciones Generales ------------------------------------------------
    def cleanParallelFigure(self):
        if not(self.figure_axes is None):
            self.iview.figure.delaxes(self.figure_axes)

    def initParallelAnalizer(self):
        pam = ParallelAnalizerModel()
        return pam.getParallelAnalizerByIdTest(self.test.id)

    def customizeFigure(self):
        self.title_g = ''
        self.color_g = (self.parallel_analizer.color_figure,)
        self.legend_g = self.parallel_analizer.legent_figure

    def updateConfigPa(self, parallel_analizer):
        pam = ParallelAnalizerModel()
        self.parallel_analizer = pam.upDate(parallel_analizer)
        self.customizeFigure()
        pub.sendMessage(T.PARALLELANALIZER_UPDATE_FIGURE)

    def restartDefaul(self):
        pam = ParallelAnalizerModel()
        self.parallel_analizer = pam.updateByFigure(self.parallel_analizer)
        self.customizeFigure()
        pub.sendMessage(T.PARALLELANALIZER_UPDATE_FIGURE, (True))
    # -------------------------------------------------------------------------

    # ---- Funciones definidas para ParallelFigure Test -----------------------
    def newFigureTest(self, ite_list, suptitle=''):
        self.cleanParallelFigure()
        suptitle = self.title_g
        self.figure_axes = self._initFigurePaint(ite_list, suptitle)
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    #     Funciones Bases o comunes para todos los tipos de grafico
    # --------------------------------------------------------------------------
    def _initFigurePaint(self, ite_list, suptitle='', sp_axe=None):
        axe = None
        if sp_axe is None:
            axe = self.iview.figure.gca()
        else:
            axe = self.iview.figure.add_subplot(sp_axe)
        self.iview.figure.suptitle(suptitle)
        axe = self._figurePaint(axe, ite_list)
        return axe

    def _figurePaint(self, axe, ite_list, count_last=0):
        _pos = 0 + count_last
        _len = len(ite_list) + count_last
        for ite in ite_list:

            df = inm().getCsv(ite, self.iview.mode)

            axe = parallel_coordinatesTava(df, 'Name', _len, _pos, axe,
                                           True, self.legend_g,
                                           color=self.color_g)
            axe.grid(b=True)
            self.iview.canvas.draw()
            _pos += 1
        self.iview.canvas.draw()
        return axe
    # --------------------------------------------------------------------------


class ButtonsTollFigurePresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test

        pub.subscribe(self.checkedTreePub, T.PARALLEL_TREE_CHECK_FIGURE)

        self.checkedTree(False)

    def checkedTreePub(self, message):
        self.checkedTree(message.data)

    def checkedTree(self, enable):
        if enable:
            self.iview.enableButtons()
        else:
            self.iview.disableButtons()

    def updateGrafic(self):
        pub.sendMessage(T.PARALLEL_UPDATE_FIGURE)

    def getStatesObjetives(self):
        no = rm().getNamesObjetivestById(self.test.test_details[0].result_id)
        vo = self.getParallelAnalizer().enable_objectives
        return no.split(','), vo.split(',')

    def getParallelAnalizer(self):
        pam = ParallelAnalizerModel()
        return pam.getParallelAnalizerByIdTest(self.test.id)

    def getUpdateListObjetive(self, list_obj):
        parallel_analizer = self.getParallelAnalizer()
        parallel_analizer.enable_objectives = ','.join(list_obj)
        names = parallel_analizer.name_objetive.split(',')

        obj_orders_var = []
        obj_orders_name = []
        order_name_obj = []
        for i in range(len(list_obj)):
            if list_obj[i] == '1':
                obj_orders_var.append(str(i))
                obj_orders_name.append(names[i])
                order_name_obj.append(names[i])

        parallel_analizer.order_objective = ','.join(obj_orders_var)
        parallel_analizer.order_name_obj = ','.join(order_name_obj)
        pam = ParallelAnalizerModel()
        pam.upDate(parallel_analizer)
        pub.sendMessage(T.PARALLEL_UPDATE_FIGURE_LIST_OBJ)

    def getObjetivesForSort(self):
        return self.getParallelAnalizer().order_name_obj.split(',')

    def updateSort(self, order_name_obj):
        parallel_analizer = self.getParallelAnalizer()
        names = parallel_analizer.name_objetive.split(',')

        obj_orders_var = []
        for obj_name in order_name_obj:
            obj_orders_var.append(str(names.index(obj_name)))

        parallel_analizer.order_objective = ','.join(obj_orders_var)
        parallel_analizer.order_name_obj = ','.join(order_name_obj)
        pam = ParallelAnalizerModel()
        pam.upDate(parallel_analizer)
        pub.sendMessage(T.PARALLEL_UPDATE_FIGURE_LIST_OBJ)


class ParallelDataVarPresenter:
    def __init__(self, iview, details):
        self.iview = iview

        self.InitUI(details)

    def InitUI(self, details):
        r = rm().getResultById(details[0].result_id)
        v_names = 'key,' + r.name_variables
        columns = v_names.split(',')
        self.countColumn = len(columns)
        for name in columns:
            self.iview.dvlc.AppendTextColumn(name, width=110)

    def updateDatas(self, ite_list):

        self.iview.dvlc.DeleteAllItems()
        for ite in ite_list:
            for var in inm().getVar(ite, self.iview.mode):
                self.iview.dvlc.AppendItem(var)


class ParallelDataObjPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        self.InitUI()

    def InitUI(self):
        pa = ParallelAnalizerModel().getParallelAnalizerByIdTest(self.test.id)

        o_names = 'key,' + pa.order_name_obj
        columns = o_names.split(',')
        self.countColumn = len(columns)
        for name in columns:
            self.iview.dvlc.AppendTextColumn(name, width=150)

    def updateDatas(self, ite_list):

        self.iview.dvlc.Destroy()
        self.iview.InitUI()
        self.InitUI()

        for ite in ite_list:
            for var in inm().getObj(ite, self.iview.mode):
                self.iview.dvlc.AppendItem(var)


class AddFilterObjetivesScrollPresenter:
    def __init__(self, iview, details):
        self.iview = iview
        self.details = details
        self.min_before = []
        self.max_before = []
        self.values = []

    def update(self, ite, is_new=True):

        if is_new:
            if self.values != []:
                for aux in range(len(self.values)):
                    self.values[aux].Destroy()
                self.values = []

            i = im().getIterationById(ite)
            min_s = i.objectives_min.split(',')
            max_s = i.objectives_max.split(',')
            r = rm().getResultById(i.result_id)
            names = r.name_objectives.split(',')

            for index in range(len(names)):
                value = self.iview.addItem(min_s[index], max_s[index],
                                           names[index], min_s[index],
                                           max_s[index])
                self.values.append(value)
            self.iview.addSiserHere()

        else:
            
            vmin, vmax = inm().getMinMax(ite, self.iview.mode)
            for aux in range(len(vmin)):
                filtro = self.values[aux]
                filtro.setValues(vmin[aux], vmax[aux])

        self.updateBeforeValues()

    def isFilterModified(self):

        for index in range(len(self.values)):
            if self.values[index].getMinValue() != self.min_before[index]:
                return True
            if self.values[index].getMaxValue() != self.max_before[index]:
                return True
        return False

    def getListValues(self):
        toRet = []
        for fil in self.values:
            toRet.append(fil.getObjectValues())
        return toRet

    def updateBeforeValues(self):
        self.min_before = []
        self.max_before = []
        for value in self.values:
            self.min_before.append(value.getMinValue())
            self.max_before.append(value.getMaxValue())
