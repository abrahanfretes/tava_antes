#  -*- coding: utf-8 -*-
'''
Created on 1/5/2015

@author: abrahan
'''
import wx
from wx.lib.pubsub import Publisher as pub

from py.una.pol.tava.presenter import topic as T
from py.una.pol.tava.model.mcurves import AndrewsCurvesModel as acm

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

        #=======================================================================
        # pub.subscribe(self.updateListObjectPub,
        #               T.PARALLEL_UPDATE_FIGURE_LIST_OBJ)
        #=======================================================================

    # ---- Funciones Generales ------------------------------------------------

    def updateFigureForChangeTreePub(self, message):
        ite_tuple = message.data
        self.ite_list = list(ite_tuple)
        ite = self.ite_list[0]
        acm().fileForDelete(ite)
        self.createDates(ite)
        # mensaje de actualizacion de figura
        # mensaje de actualizacion de variables
        # mensaje de actualizacion de objetivos
        pub.sendMessage(T.PARALLEL_UPDATE_ALL_AL, self.ite_list)

    #===========================================================================
    # def updateListObjectPub(self, message):
    #     if self.ite_list != []:
    #         ite = self.ite_list[0]
    #         pam().fileForDelete(ite)
    #         self.createDates(ite)
    #         # mensaje de actualizacion de figura
    #         # mensaje de actualizacion de variables
    #         # mensaje de actualizacion de objetivos
    #         pub.sendMessage(T.PARALLEL_UPDATE_ALL_AL, self.ite_list)
    #===========================================================================

    def createDates(self, ite):
        ac = acm().getCurvesByTestId(self.test.id)
        return acm().createDates(ac, ite)

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
class CurvesTreePresenter:
    def __init__(self, iview, test):

        self.iview = iview
        self.root = self.iview.AddRoot("Test Data")
        self.checkeds_last = []
        self.old_item = None

        pub.subscribe(self.verifyChangeCheckedPub,
                      T.PARALLEL_VERIFY_TREE_CHECKED_AL)
        pub.subscribe(self.setBackGroundTreePub,
                      T.PARALLEL_BACKGROUND_UPDATE_AL)

        self.InitUI(test)
        # ------------------------------------------------------------

        #  Inicializacion del arbol de proyectos
    def InitUI(self, test):
        ac = acm().getCurvesByTestId(test.id)
        self.__setBackGround(ac.colors_backgrounds)

        for_tree = acm().getFormatTree(test)

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
        self.checkeds_last = sorted(self.__getListChecked())

    # ---- Metodos usados con Topic -----------
    # ---                           -----------
    def setBackGroundTreePub(self, messege):
        self.__setBackGround(messege.data)

    def verifyChangeCheckedPub(self, message):
        pub.sendMessage(T.PARALLEL_UPDATE_FIGURE_FOR_TREE_AL,
                        tuple(self.__getListChecked()))
        pub.sendMessage(T.PARALLEL_TREE_CHECK_SET_FILTER_AL,
                        tuple(self.__getListChecked()))

        self.__updateFigureItem()
        pub.sendMessage(T.PARALLEL_ONCLICK_BUTTON_EXECUTE_AL)

    # ---- Metodos usados No Localmente -----------
    # ---                               -----------

    def setChecked(self):
        # oculta y desoculta los botones para iltros heredados de BaseButton
        pub.sendMessage(T.PARALLEL_TREE_CHECK_FIGURE_AL,
                        self.__getOneChecked())
        if self.__getOneChecked():
            # oculta y desoculta los botones para iltros
            pub.sendMessage(T.PARALLEL_TREE_CHECK_FILTER_AL,
                            tuple(self.__getListChecked()))

    # ---- Metodos usados Localmente -----------
    # ---                            -----------

    def __setBackGround(self, backColor):
        self.iview.SetBackgroundColour(backColor.split(',')[0])

    def __getListChecked(self, true=True):
        to_dicc = []
        for item_result in self.root.GetChildren():
            for item_ite in item_result.GetChildren():
                if true == self.iview.IsItemChecked(item_ite):
                    to_dicc.append(self.iview.GetItemPyData(item_ite))
        return to_dicc

    def __updateFigureItem(self):
        if self.old_item is not None:
            self.iview.SetItemImage(self.old_item, 2)
        item = self.__getListItemChecked()[0]
        self.iview.SetItemImage(item, 1)
        self.old_item = item

    def __getLenListChecked(self):
        return len(self.__getListChecked())

    def __getOneChecked(self):
        if 1 == self.__getLenListChecked():
            if not (self.__getListItemChecked()[0] == self.old_item):
                return True
            else:
                pub.sendMessage(T.PARALLEL_ONCLICK_BUTTON_EXECUTE_AL)
        return False

    def __getListItemChecked(self, true=True):
        to_dicc = []
        for item_result in self.root.GetChildren():
            for item_ite in item_result.GetChildren():
                if true == self.iview.IsItemChecked(item_ite):
                    to_dicc.append(item_ite)
        return to_dicc

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
class CurvesFigurePresenter:
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

        ac = self.__getAC()
        self.__setBackGroundFigure(ac.colors_backgrounds)

    # ---- Metodos usados con Topic -----------
    # ---                           -----------
    def newFigureTestPub(self, message):
        self.ite_list = message.data
        self.newFigureTest(self.ite_list)

    def setBackGroundFigurePub(self, message):
        self.__setBackGroundFigure(message.data)

    def setGridFigurePub(self, message):
        if self.figure_axes is not None:
            self.newFigureTest(self.ite_list)

    # ---- Metodos usados No Localmente -----------
    # ---                               -----------

    def newFigureTestShowPub(self, message):
        ite_list = message.data
        self.newFigureTest(ite_list)

    def newFigureTest(self, ite_list, suptitle=''):
        pa = self.__getAC()
        self.color_g = (pa.color_lines,)
        self.legend_g = pa.legent
        self.__cleanParallelFigure()
        suptitle = self.title_g
        self.figure_axes = self._initFigurePaint(ite_list, suptitle)

    def getAdrewsCurves(self):
        return self.__getAC()

    # ---- Metodos usados Localmente -----------
    # ---                            -----------

    def __getAC(self):
        return acm().getCurvesByTestId(self.test.id)

    def __setBackGroundFigure(self, backColor):
        list_bac = backColor.split(',')
        self.iview.figure.set_facecolor(list_bac[1])
        self.iview.SetBackgroundColour(list_bac[2])
        self.iview.toolbar.SetBackgroundColour(list_bac[2])
        self.iview.canvas.draw()

    def __cleanParallelFigure(self):
        if not(self.figure_axes is None):
            self.iview.figure.delaxes(self.figure_axes)

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
            axe = acm().getCurvesAxe(iteration, _len, _pos, axe,
                                     self.legend_g, self.color_g)
            # ac = self.__getAC()
            # axe = self._setAddConfigGrip(axe, ac.figure_grid)

            self.iview.canvas.draw()
            _pos += 1
        self.iview.canvas.draw()
        return axe
    # --------------------------------------------------------------------------

    #===========================================================================
    # def _setAddConfigGrip(self, axe, figure_grid):
    #     fg = figure_grid
    #     if fg.grid:
    #         o_axis = tvc.ORIENTATION_LINE_AL[fg.orientation]
    #         s_linestyle = tvc.STYLE_LINE_AL[fg.red_style]
    #         axe.grid(b=True,  which='major', axis=o_axis,
    #                  color=fg.red_color, linestyle=s_linestyle,
    #                  linewidth=fg.red_width)
    #     else:
    #         axe.grid(fg.grid)
    #     return axe
    #===========================================================================


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

