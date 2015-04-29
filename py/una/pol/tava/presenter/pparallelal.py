#  -*- coding: utf-8 -*-
'''
Created on 9/4/2015

@author: abrahan
'''
import wx
from wx.lib.pubsub import Publisher as pub

import topic as T
import py.una.pol.tava.base.tavac as tvc
from py.una.pol.tava.model.mparallel_analizer import\
    ParallelAnalizerModel as pam


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Sección encargada de los componentes Manejadores (Presenter) para para
# TopPanel
# -> TopPanelPresenter
# Maneja los eventos de creación de archivos y actualización de Figura.
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

class TopPanelPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        self.ite_list = []

        pub.subscribe(self.updateFigureForChangeTreePub,
                      T.PARALLEL_UPDATE_FIGURE_FOR_TREE_AL)

        pub.subscribe(self.updateListObjectPub,
                      T.PARALLEL_UPDATE_FIGURE_LIST_OBJ)

    # ---- Funciones Generales ------------------------------------------------

    def updateFigureForChangeTreePub(self, message):
        ite_tuple = message.data
        self.ite_list = list(ite_tuple)
        ite = self.ite_list[0]
        pam().fileForDelete(ite)
        self.createDates(ite)
        # mensaje de actualizacion de figura
        # mensaje de actualizacion de variables
        # mensaje de actualizacion de objetivos
        pub.sendMessage(T.PARALLEL_UPDATE_ALL_AL, self.ite_list)

    def updateListObjectPub(self, message):
        if self.ite_list != []:
            ite = self.ite_list[0]
            pam().fileForDelete(ite)
            self.createDates(ite)
            # mensaje de actualizacion de figura
            # mensaje de actualizacion de variables
            # mensaje de actualizacion de objetivos
            pub.sendMessage(T.PARALLEL_UPDATE_ALL_AL, self.ite_list)

    def createDates(self, ite):
        p_analizer = pam().getParallelAnalizerByIdTest(self.test.id)
        return pam().createDates(p_analizer, ite)

    # -------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Sección encargada de los componentes Manejadores (Presenter) para
# ParallelTreeAL.
# Maneja los eventos sobre el arbol de iteraciones.
# -> checket
# -> unchecket
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


# ------------------- Clase Presentador de Arbol de Archvivos e Iteraciones ---
# -------------------                                  ------------------------
class ParallelTreeALPresenter:
    def __init__(self, iview, test):

        self.iview = iview
        self.root = self.iview.AddRoot("Test Data")
        self.checkeds_last = []
        self.old_item = None

        pub.subscribe(self.verifyChangeChecked,
                      T.PARALLEL_VERIFY_TREE_CHECKED_AL)
        pub.subscribe(self.setBackGroundTreePub,
                      T.PARALLEL_BACKGROUND_UPDATE_AL)

        self.InitUI(test)
        # ------------------------------------------------------------

        #  Inicializacion del arbol de proyectos
    def InitUI(self, test):
        pa = pam().getParallelAnalizerByIdTest(test.id)
        self.setBackGroundTree(pa.colors_backgrounds)

        for_tree = pam().getFormatTree(test)

        # inicializamos el arbol
        for r_name in for_tree.keys():
            td_item = self.iview.AppendItem(self.root, r_name)
            self.iview.SetItemPyData(td_item, '')
            self.iview.SetItemImage(td_item, 0, wx.TreeItemIcon_Normal)

            for ite_data in for_tree[r_name]:
                tda_item = self.iview.AppendItem(td_item,
                                                 ite_data[0], ct_type=1)
                self.iview.SetItemPyData(tda_item, ite_data[1])
                self.iview.CheckItem(tda_item, False)
                self.iview.SetItemImage(tda_item, 2)

        # ordenamos el arbol
        self.iview.SortChildren(self.root)

        # expandimos el arbol
        for item in self.root.GetChildren():
            self.iview.Expand(item)

        # inicializamos la lista de chequeados
        self.checkeds_last = sorted(self.getListChecked())

    def setBackGroundTreePub(self, messege):
        self.setBackGroundTree(messege.data)

    def setBackGroundTree(self, backColor):
        self.iview.SetBackgroundColour(backColor.split(',')[0])

    def getListChecked(self, true=True):
        to_dicc = []
        for item_result in self.root.GetChildren():
            for item_ite in item_result.GetChildren():
                if true == self.iview.IsItemChecked(item_ite):
                    to_dicc.append(self.iview.GetItemPyData(item_ite))
        return to_dicc

    def getListItemChecked(self, true=True):
        to_dicc = []
        for item_result in self.root.GetChildren():
            for item_ite in item_result.GetChildren():
                if true == self.iview.IsItemChecked(item_ite):
                    to_dicc.append(item_ite)
        return to_dicc

    def getLenListChecked(self):
        return len(self.getListChecked())

    def setChecked(self):
        pub.sendMessage(T.PARALLEL_TREE_CHECK_FIGURE_AL, self.getOneChecked())
        if self.getOneChecked():
            pub.sendMessage(T.PARALLEL_TREE_CHECK_FILTER_AL,
                            tuple(self.getListChecked()))

    def getOneChecked(self):
        if 1 == self.getLenListChecked():
            if not (self.getListItemChecked()[0] == self.old_item):
                return True
            else:
                pub.sendMessage(T.PARALLEL_ONCLICK_BUTTON_EXECUTE_AL)
        return False

    def verifyChangeChecked(self, message):
        pub.sendMessage(T.PARALLEL_UPDATE_FIGURE_FOR_TREE_AL,
                        tuple(self.getListChecked()))
        pub.sendMessage(T.PARALLEL_TREE_CHECK_SET_FILTER_AL,
                        tuple(self.getListChecked()))

        self.updateFigureItem()
        pub.sendMessage(T.PARALLEL_ONCLICK_BUTTON_EXECUTE_AL)

    def updateFigureItem(self):
        if self.old_item is not None:
            self.iview.SetItemImage(self.old_item, 2)
        item = self.getListItemChecked()[0]
        self.iview.SetItemImage(item, 1)
        self.old_item = item
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Sección encargada de los componentes Manejadores (Presenters) para una figura
# de Coordenadas Paralelas:
# -> ParallelFigureALPresenter
# -> BaseButtonsTollBar
# -> ButtonsExecutionPresenter
# -> ButtonsConfigPresenter
# -> ButtonsFilterPresenter
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


# ------------------- Clase Presentador de Figura Coordenadas Paralelas  ------
# -------------------                                  ------------------------
class ParallelFigureALPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        self.figure_axes = None
        self.title_g = ''
        self.ite_list = []

        pub.subscribe(self.newFigureTestPub, T.PARALLEL_UPDATE_ALL_AL)
        pub.subscribe(self.setBackGroundFigurePub,
                      T.PARALLEL_BACKGROUND_UPDATE_AL)
        pub.subscribe(self.setGridFigurePub, T.PARALLEL_GRID_UPDATE_AL)

        self.Init()

    def Init(self):

        pa = self.getParallelAnalizer()
        self.setBackGroundFigure(pa.colors_backgrounds)

    # ---- Funciones Generales ------------------------------------------------
    def setGridFigurePub(self, message):
        if self.figure_axes is not None:
            self.newFigureTest(self.ite_list)

    def setBackGroundFigurePub(self, message):
        self.setBackGroundFigure(message.data)

    def setBackGroundFigure(self, backColor):
        list_bac = backColor.split(',')
        self.iview.figure.set_facecolor(list_bac[1])
        self.iview.SetBackgroundColour(list_bac[2])
        self.iview.toolbar.SetBackgroundColour(list_bac[2])
        self.iview.canvas.draw()

    def newFigureTestPub(self, message):
        # self.iview.figure.set_facecolor('#FFAAAA')
        self.ite_list = message.data
        self.newFigureTest(self.ite_list)

    def newFigureTestShowPub(self, message):
        ite_list = message.data
        self.newFigureTest(ite_list)

    def cleanParallelFigure(self):
        if not(self.figure_axes is None):
            self.iview.figure.delaxes(self.figure_axes)

    def getParallelAnalizer(self):
        return pam().getParallelAnalizerByIdTest(self.test.id)
    # -------------------------------------------------------------------------

    # ---- Funciones definidas para ParallelFigure Test -----------------------
    def newFigureTest(self, ite_list, suptitle=''):
        pa = self.getParallelAnalizer()
        self.color_g = (pa.color_lines,)
        self.legend_g = pa.legent
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
        for iteration in ite_list:
            axe = pam().getParallelAxe(iteration, _len, _pos, axe,
                                       self.legend_g, self.color_g)
            pa = self.getParallelAnalizer()
            axe = self._setAddConfigGrip(axe, pa.figure_grid)

            self.iview.canvas.draw()
            _pos += 1
        self.iview.canvas.draw()
        return axe
    # --------------------------------------------------------------------------

    def _setAddConfigGrip(self, axe, figure_grid):
        fg = figure_grid
        if fg.grid:
            o_axis = tvc.ORIENTATION_LINE_AL[fg.orientation]
            s_linestyle = tvc.STYLE_LINE_AL[fg.red_style]
            axe.grid(b=True,  which='major', axis=o_axis,
                     color=fg.red_color, linestyle=s_linestyle,
                     linewidth=fg.red_width)
        else:
            axe.grid(fg.grid)
        return axe


# ------------------- Clase Presentador de Botones para Ejecución     ---------
# -------------------                                  ------------------------
class BaseButtonsTollBar:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.checkedTreePub, T.PARALLEL_TREE_CHECK_FIGURE_AL)

        self.checkedTree(False)

    def checkedTreePub(self, message):
        self.checkedTree(message.data)

    def checkedTree(self, enable):
        if enable:
            self.iview.enableButtons()
        else:
            self.iview.disableButtons()


# ------------------- Clase Presentador de Botones para Ejecución     ---------
# -------------------                                  ------------------------
class ButtonsExecutionPresenter(BaseButtonsTollBar):
    def __init__(self, iview):
        BaseButtonsTollBar.__init__(self, iview)

        pub.subscribe(self.onClickExecute,
                      T.PARALLEL_ONCLICK_BUTTON_EXECUTE_AL)

        pub.subscribe(self.setBackGroundExecutionPub,
                      T.PARALLEL_BACKGROUND_UPDATE_AL)

    def setBackGroundExecutionPub(self, message):
        self.iview.SetBackgroundColour(message.data.split(',')[2])
        self.iview.GetParent().SetBackgroundColour(message.data.split(',')[2])

    def onClickExecute(self, message):
        self.checkedTree(False)

    def verifyTreeCheckeo(self):
        pub.sendMessage(T.PARALLEL_VERIFY_TREE_CHECKED_AL)


# ------------------- Clase Presentador de Botones para Configuración    ------
# -------------------                                  ------------------------
class ButtonsConfigPresenter(BaseButtonsTollBar):
    def __init__(self, iview, pa):
        BaseButtonsTollBar.__init__(self, iview)
        self.pa = pa

        pub.subscribe(self.setBackGroundConfigPub,
                      T.PARALLEL_BACKGROUND_UPDATE_AL)

    def setBackGroundConfigPub(self, message):
        self.iview.SetBackgroundColour(message.data.split(',')[2])

    def getParallelAnalizer(self):
        self.pa = pam().getParallelAnalizerById(self.pa.id)
        return self.pa

    def checkedTree(self, enable):
        self.iview.enableButtons()


# ------------------- Clase Presentador de Botones para Filtros      ----------
# -------------------                                  ------------------------
class ButtonsFilterPresenter(BaseButtonsTollBar):
    def __init__(self, iview):
        BaseButtonsTollBar.__init__(self, iview)

        self.ite_less = None

        pub.subscribe(self.checkedSetFilterPub,
                      T.PARALLEL_TREE_CHECK_SET_FILTER_AL)
        pub.subscribe(self.checkedFilterPub, T.PARALLEL_TREE_CHECK_FILTER_AL)
        pub.subscribe(self.onClickExecute,
                      T.PARALLEL_ONCLICK_BUTTON_EXECUTE_AL)
        pub.subscribe(self.setBackGroundFilterPub,
                      T.PARALLEL_BACKGROUND_UPDATE_AL)

    def setBackGroundFilterPub(self, message):
        self.iview.SetBackgroundColour(message.data.split(',')[2])

    def onClickExecute(self, message):
        self.checkedTree(True)

    def checkedSetFilterPub(self, message):
        self.ite_less = message.data[0]
        self.checkedTree(True)

    def checkedFilterPub(self, message):
        if self.ite_less == message.data[0]:
            self.checkedTree(True)
        else:
            self.checkedTree(False)

    def setFilters(self):
        pub.sendMessage(T.PARALLEL_ON_SET_FILTERS_OBJ_AL)

    def cleanFilter(self):
        pub.sendMessage(T.PARALLEL_ON_CLEAN_FILTERS_OBJ_AL)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Sección encargada de los componentes Manejadores (Presenters) para los Tab de
# de BottonPanel:
# -> TabVariablesPresenter
# -> TabObjectivesPresenter
# -> TabFiltrosPresenter
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# ------------------- Clase Presentador del Tab para Variables ----------------
# -------------------                                  ------------------------
class TabVariablesPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test

        pub.subscribe(self.updateDatasPub, T.PARALLEL_UPDATE_ALL_AL)

        self.InitUI()

    def InitUI(self):
        pa = pam().getParallelAnalizerByIdTest(self.test.id)
        v_names = 'key,' + pa.name_variable
        columns = v_names.split(',')
        self.countColumn = len(columns)
        for name in columns:
            self.iview.dvlc.AppendTextColumn(name, width=110)

    def updateDatasPub(self, message):
        ite_list = list(message.data)
        self.updateDatasVar(ite_list)

    def updateDatasVar(self, ite_list):
        self.iview.dvlc.Destroy()
        self.iview.InitUI()
        self.InitUI()

        for iteration in ite_list:
            for var in pam().getVariablesForTab(iteration):
                self.iview.dvlc.AppendItem(var)


# ------------------- Clase Presentador del Tab para Objetivos ----------------
# -------------------                                  ------------------------
class TabObjectivesPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test

        pub.subscribe(self.updateDatasPub, T.PARALLEL_UPDATE_ALL_AL)

        self.InitUI()

    def InitUI(self):
        pa = pam().getParallelAnalizerByIdTest(self.test.id)

        o_names = 'key,' + pa.order_name_obj
        columns = o_names.split(',')
        self.countColumn = len(columns)
        for name in columns:
            self.iview.dvlc.AppendTextColumn(name, width=150)

    def updateDatasPub(self, message):
        ite_list = list(message.data)
        self.updateDatas(ite_list)

    def updateDatas(self, ite_list):
        self.iview.dvlc.Destroy()
        self.iview.InitUI()
        self.InitUI()

        for iteration in ite_list:
            for obj in pam().getObjectivesForTab(iteration):
                self.iview.dvlc.AppendItem(obj)


# ------------------- Clase Presentador del Tab para Filtros  -----------------
# -------------------                                  ------------------------
class TabFiltrosPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        self.less_update = False
        self.min_before = []
        self.max_before = []
        self.values = []

        pub.subscribe(self.updateDatasPub, T.PARALLEL_UPDATE_ALL_AL)
        pub.subscribe(self.setFiltersNowPub, T.PARALLEL_ON_SET_FILTERS_OBJ_AL)
        pub.subscribe(self.setFiltersCleanPub,
                      T.PARALLEL_ON_CLEAN_FILTERS_OBJ_AL)

        pub.subscribe(self.updateRenameObjectPub,
                      T.PARALLEL_UPDATE_FIGURE_RENAME_OBJ)

    def updateDatasPub(self, message):
        ite_list = list(message.data)
        self.updateFiltros(ite_list)

    def setFiltersNowPub(self, message):
        if self.isFilterModified():
            pa = pam().getParallelAnalizerByIdTest(self.test.id)
            pa.maxs_objetive, pa.mins_objetive = self.getListValues()
            pam().upDate(pa)
            self.less_update = True
            pub.sendMessage(T.PARALLEL_UPDATE_FIGURE_LIST_OBJ)

    def setFiltersCleanPub(self, message):
        if self.less_update:
            pa = pam().getParallelAnalizerByIdTest(self.test.id)
            pa.maxs_objetive = None
            pa.mins_objetive = None
            pam().upDate(pa)
            self.less_update = False
            pub.sendMessage(T.PARALLEL_UPDATE_FIGURE_LIST_OBJ)

    def updateRenameObjectPub(self, message):
        # no deberia necesitar si esta guardado
        pub.sendMessage(T.PARALLEL_UPDATE_FIGURE_LIST_OBJ)

    def updateFiltros(self, ite_list):

        # destruir el anterior
        if self.values != []:
            for aux in range(len(self.values)):
                self.values[aux].Destroy()
            self.values = []

        # filtro las variables correspondientes
        iteration = ite_list[0]
        vmin, vmax = pam().getMinMaxForTabFilter(iteration)

        # obtengo los nombres
        pa = pam().getParallelAnalizerByIdTest(self.test.id)
        names = pa.order_name_obj.split(',')

        # creo los filtros
        if len(names) == len(vmin):
            for index in range(len(names)):
                value = self.iview.addItem(vmin[index], vmax[index],
                                           names[index], vmin[index],
                                           vmax[index])
                self.values.append(value)

        # actualizo la vista
        self.iview.addSiserHere()
        self.updateBeforeValues()

    def isFilterModified(self):

        for index in range(len(self.values)):
            if self.values[index].getMinValue() != self.min_before[index]:
                return True
            if self.values[index].getMaxValue() != self.max_before[index]:
                return True
        return False

    def getListValues(self):

        max_list = []
        min_list = []
        for fil in self.values:
            max_list.append(str(fil.getMaxValue()))
            min_list.append(str(fil.getMinValue()))
        return ','.join(max_list), ','.join(min_list)

    def updateBeforeValues(self):
        self.min_before = []
        self.max_before = []
        for value in self.values:
            self.min_before.append(value.getMinValue())
            self.max_before.append(value.getMaxValue())

    def getFiltersByNames(self, tuple_names):
        min_list = []
        max_list = []
        for name in tuple_names:
            for value in self.values:
                if name == value.name_objetive:
                    min_list.append(value.getMinValue())
                    max_list.append(value.getMaxValue())
                    break
        return max_list, min_list
