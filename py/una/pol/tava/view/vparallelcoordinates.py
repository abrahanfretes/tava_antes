# -*- coding: utf-8 -*-
'''
Created on 11/10/2014

@author: abrahan
'''

import wx
# Para emplear como backend la libreria WxPython
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
import numpy as np
from py.una.pol.tava.presenter.pparallelcoordinates import WorkingPagePresenter
import py.una.pol.tava.view.vimages as I

import wx.lib.agw.customtreectrl as CT
from py.una.pol.tava.presenter.pparallelcoordinates\
                                                import ParallelDataPresenter
from py.una.pol.tava.presenter.pparallelcoordinates\
                                                import ParallelFigurePresenter
from py.una.pol.tava.presenter.pparallelcoordinates\
                                            import ParallelDataOptionsPresenter
from pandas import read_csv
from pandas.tools.plotting import andrews_curves

parallel_suplot = 0
parallel_figure = 1


class WorkingPageParallel(wx.Panel):
    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        #------ Definiciones iniciales ----------------------------------------
        self.test = test
        self.presenter = WorkingPagePresenter(self, test)

        #ultimas iteraciones checkeadas para el tipo de Subplot
        self.checked_last_ite_subplot = []

        #ultimas iteraciones checkeadas para el tipo de no Subplot
        self.checked_last_ite_figure = []

        #ultimas iteraciones checkeadas para el tipo secuencial
        self.checked_last_ite_sec = []

        #ultimas iteraciones checkeadas para el tipo por iteracion
        self.checked_last_ite_ite = []

        self.type_figure_last = None

        self.InitUI()
        #----------------------------------------------------

    def InitUI(self):

        # una Pagina consiste en:
        # Una o mas figuras y,
        # Unas configuraciones
        self.data = ParallelDataTree(self, self.test)
        self.options = ParallelDataOptions(self)
        self.figure = ParallelFigure(self)

        box_config = wx.BoxSizer(wx.VERTICAL)
        box_config.Add(self.data, 2, wx.EXPAND)
        box_config.Add(self.options, 1, wx.EXPAND)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(box_config, 1, wx.EXPAND)
        sizer.Add(self.figure, 3, wx.EXPAND)
        self.SetSizer(sizer)

        #crea una archivo por cada iteracion
        self.presenter.setDicIterationByResult()
        self.initializeSubplot()
        self.initializeIte()

    def  isTypeModified(self):
        type_aux = self.options.getTypeSelection()
        if self.type_figure_last != type_aux:
            return True
        return False

    def updateTypeFigure(self):
        self.type_figure_last = self.options.getTypeSelection()

    def showGraphicTava(self, type_figure):
        '''
        Selecciona la funcion a ejecutar teniendo en cuenta el typo de grafico
        y las opciones chekeadas en el arbol de iteraciones.

        :param type_figure: Integer.
        '''
        type_modified = self.isTypeModified()
        tree_modiefed = self.isTreeModified()

        if tree_modiefed and not type_modified:
            print '------------------------------------'
            print 'tree: modified, type: not modified'
            print '------------------------------------'
            self.showOnlyTreeModified(type_figure)
            self.updateListChecked()
            self.updateTypeFigure()

        elif not tree_modiefed and type_modified:
            print '------------------------------------'
            print 'tree: not modified, type: modified'
            print '------------------------------------'
            self.figure.cleanParallelFigure()
            self.showOnlyTypeModified(type_figure)
            self.updateTypeFigure()

        elif  tree_modiefed and type_modified:
            print '------------------------------------'
            print 'tree: modified, type: modified'
            print '------------------------------------'
            self.figure.cleanParallelFigure()
            self.showTreeAndTypeModified(type_figure)
            self.updateListChecked()
            self.updateTypeFigure()

        else:
            print 'tree: not modified, type: not modified'

    def isTreeModified(self):

        type_f = self.options.getTypeSelection()

        if type_f == 0:
            return self.isTreeModifiedSubplot()
        elif type_f == 1:
            return self.isTreeModifiedFigure()
        elif type_f == 2:
            return self.isTreeModifiedSec()
        elif type_f == 3:
            return self.isTreeModifiedIte()

    def updateListChecked(self):
        type_f = self.options.getTypeSelection()

        if type_f == 0:
            self.checked_last_ite_subplot = self.data.setGraphedList()
        elif type_f == 1:
            self.checked_last_ite_figure = self.data.setGraphedList()
        elif type_f == 2:
            self.checked_last_ite_sec = self.data.setGraphedList()
        elif type_f == 3:
            self.checked_last_ite_ite = self.data.setGraphedList()

    def showOnlyTreeModified(self, type_f):

        if type_f == 0:
            dic_namepath_file = self.createPathFileForTypeSubplot()
            self.figure.updateSubplots(dic_namepath_file)
        elif type_f == 1:
            self.presenter.setDicNameIteCheckedLastFigure(None)
            path_plot = self.createPathFileForTypeFigure()
            self.figure.showParallelFigureUpdate(path_plot)
        elif type_f == 2:
            self.presenter.setDicNameIteCheckedLastSec(None)
            path_plot = self.createPathFileForTypeSec()
            self.figure.showParallelSecuencialUpdate(path_plot)
        elif type_f == 3:
            dic_for_plot = self.createPathFileForTypeIte()
            self.figure.showParallelIteUpdate(dic_for_plot)

    def showOnlyTypeModified(self, type_f):

        if type_f == 0:
            dic_namepath_file = self.presenter.dic_name_path_subplot
            self.figure.updateSubplots(dic_namepath_file)
        elif type_f == 1:
            path_plot = self.presenter.name_path_figure
            self.figure.showParallelFigureUpdate(path_plot)
        elif type_f == 2:
            path_plot = self.presenter.name_path_sec
            self.figure.showParallelSecuencialUpdate(path_plot)
        elif type_f == 3:
            dic_for_plot = self.presenter.dic_name_path_ite
            self.figure.showParallelIteUpdate(dic_for_plot)

    def showTreeAndTypeModified(self, type_f):

        if type_f == 0:
            self.presenter.setDicNameIteCheckedLastSubplot(None)
        elif type_f == 1:
            pass
        elif type_f == 2:
            pass
        elif type_f == 3:
            self.presenter.setDicNameIteCheckedLastIte(None)

        self.showOnlyTreeModified(type_f)

    #---- Funciones definidas para Parallel Secuencial ------------------------

    def createPathFileForTypeSec(self):
        #obtengo la lista de iteraciones checkeadas
        cleaned_dic = self.data.getDicIteChecked()
        new_dic = self.presenter.updateDicCheckedLastSec(cleaned_dic)
        path_plot = self.presenter.createFileForSec(new_dic)
        return path_plot

    def  isTreeModifiedSec(self):
        aux = self.data.setGraphedList()
        if self.checked_last_ite_sec != aux:
            return True
        return False

    #------------------------------------------------------------------

    #---- Funciones definidas para ParallelFigure sin SubPlot -----------------
    def initializeParallelFigure(self):
        pass

    def createPathFileForTypeFigure(self):
        #obtengo la lista de iteraciones checkeadas
        cleaned_dic = self.data.getDicIteChecked()
        new_dic = self.presenter.updateDicCheckedLastFigure(cleaned_dic)
        path_plot = self.presenter.createFileForFigure(new_dic)
        return path_plot

    def  isTreeModifiedFigure(self):
        aux = self.data.setGraphedList()
        if self.checked_last_ite_figure != aux:
            return True
        return False

    #------------------------------------------------------------------

    #---- Funciones definidas para Parallel SubPlot ---------------------------

    def createPathFileForTypeSubplot(self):
        #obtengo la lista de iteraciones checkeadas
        dic_checked = self.data.getDicIteChecked()
        #actualizo la lista de checkeados anteriores, retorno la diferencia
        dic_new = self.presenter.updateDicCheckedLastSubplot(dic_checked)
        #obtengo la lista de actualizacion, creo el archivo y devuelvo path
        dic_namepath_file = self.presenter.createFileForSubplot(dic_new)
        return dic_namepath_file

    def initializeSubplot(self):
        keys_result = self.presenter.dic_path_iteration.keys()
        self.figure.createKeysForSubPlot(keys_result)

    def  isTreeModifiedSubplot(self):
        aux = self.data.setGraphedList()
        if self.checked_last_ite_subplot != aux:
            return True
        return False

    #------------------------------------------------------------------

    #---- Funciones definidas para Parallel Iteracion -------------------------

    def createPathFileForTypeIte(self):
        #obtengo la lista de iteraciones checkeadas
        dic_checked = self.data.getDicIteChecked()
        list_checked = self.presenter.getListChecked(dic_checked)
        #actualizo la lista de checkeados anteriores, retorno la diferencia y
        #obtengo la lista de actualizacion, creo el archivo y devuelvo path
        dic_name = self.presenter.updateDicCheckedLastIte(list_checked)

        return dic_name

    def initializeIte(self):
        keys_result = self.presenter.getKeyIteForSubplot()
        self.presenter.createFileForIte(keys_result)
        self.figure.createKeysIteForPlot(keys_result)

    def  isTreeModifiedIte(self):
        aux = self.data.setGraphedList()
        if self.checked_last_ite_ite != aux:
            return True
        return False

    #------------------------------------------------------------------

    def  isFirstInvocation(self):
            return not self.figure.showed_figure

    def clearDicChecked(self, dic_checked):
        '''
        Elimina de la lista los archivos resultados que no tenga ninguna
        iteracion checkeado.
        '''
        for key_result in dic_checked.keys():
            if dic_checked[key_result] == ():
                del dic_checked[key_result]
        return dic_checked


class ParallelFigure(wx.Panel):
    '''
    Clase Panel que contiene la configuracion para la visualizacion del
    componente de coordenadas paralelas.
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        #------ Definiciones iniciales ----------------------------------------
        self.presenter = ParallelFigurePresenter(self)
        self.showed_figure = False
        self.InitUI()
        #----------------------------------------------------

    def InitUI(self):

        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

    #---- Funciones Generales -------------------------------------------------
    def cleanParallelFigure(self):
        self.presenter.cleanParallelFigure()
        self.figure.clear()

    def  updateShowedFigure(self, value):
        self.showed_figure = value
    #-------------------------------------------------------------------------

    #---- Funciones definidas para Parallel SubPlot ---------------------------
    def createKeysForSubPlot(self, keys_result):
        self.presenter.createKeysForSubPlot(sorted(keys_result))

    def  showSubplots(self, dic_for_plot):
        self.presenter.showSubplots(dic_for_plot)

    def  updateSubplots(self, dic_for_plot):
        self.presenter.updateSubplots(dic_for_plot)

    def ShowAndrewsCurves(self, file_path, c_plot):
        axe = self.figure.add_subplot(c_plot)
        df = read_csv(file_path)
        axe = andrews_curves(df, 'Name', axe)
        self.canvas.draw()
    #------------------------------------------------------------------

    #---- Funciones definidas para ParallelFigure sin SubPlot -----------------
    def showParallelFigure(self, path_plot):
        self.presenter.showForParallelFigure(path_plot)

    def showParallelFigureUpdate(self, path_plot):
        self.presenter.showParallelFigureUpdate(path_plot)

    #------------------------------------------------------------------

    #---- Funciones definidas para ParallelFigure Secuencial -----------------
    def showParallelSecuencial(self, path_plot):
        self.presenter.showParallelSecuencial(path_plot)

    def showParallelSecuencialUpdate(self, path_plot):
        self.presenter.showParallelSecuencialUpdate(path_plot)

    #------------------------------------------------------------------

    #------------------------------------------------------------------

    #---- Funciones definidas para ParallelFigure Iteracion -------------------

    def createKeysIteForPlot(self, keys_result):
        self.presenter.createKeysIteForPlot(sorted(keys_result))

    def showParallelIteUpdate(self, dic_for_plot):
        self.presenter.showParallelIteUpdate(dic_for_plot)

    #------------------------------------------------------------------


#------------------- Set Test Actions Options ---------------------------------
class ParallelDataOptions(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.presenter = ParallelDataOptionsPresenter(self)
        self.styleNameList = ['Por Result', 'Por Test', 'Secuencial',
                              'Por Iteracion']
        self.InitUI()
        #----------------------------------------------------

    def InitUI(self):
        dimension = len(self.styleNameList)
        self.radiob = wx.RadioBox(self, -1, 'tipo grafico', wx.DefaultPosition,
            wx.DefaultSize, self.styleNameList, dimension, wx.RA_SPECIFY_ROWS)

        self.button_grafic = wx.Button(self, -1, 'Show')
        self.Bind(wx.EVT_BUTTON, self.OnUpDateGrafic, self.button_grafic)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.radiob, 3, wx.EXPAND)
        sizer.Add(self.button_grafic, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def OnUpDateGrafic(self, event):
        self.parent.showGraphicTava(self.radiob.GetSelection())
        self.UpDateNameButton()

    def UpDateNameButton(self):
        self.button_grafic.SetLabel('Update')

    def getTypeSelection(self):
        return self.radiob.GetSelection()

#------------------------------------------------------------------------------


#------------------- Config Tree Test Data ------------------------------------
class ParallelDataTree(CT.CustomTreeCtrl):
    def __init__(self, parent, test):
        CT.CustomTreeCtrl.__init__(self, parent, agwStyle=CT.TR_HIDE_ROOT)

        #------ Definiciones iniciales -------------------------------
        self.presenter = ParallelDataPresenter(self)
        self.test = test
        self.root = self.AddRoot("Test Data")

        #lista de  iteraciones checkeadas
        self.list_shecked = []

        self.InitUI()
        #------------------------------------------------------------

    def InitUI(self):

        il = wx.ImageList(16, 16)
        self.file_bmp = il.Add(I.filegraph_png)
        self.AssignImageList(il)
        self.SetBackgroundColour('#D9F0F8')

        # Inicializacion del arbol de proyectos
        self.presenter.InitializeTree(self.test)
        self.presenter.expandItemTree()

        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnChecked)

    def AddTestDetailNode(self, result_id, resul_name):
        td_item = self.AppendItem(self.root, resul_name)
        self.SetItemPyData(td_item, result_id)
        self.SetItemImage(td_item, 0, wx.TreeItemIcon_Normal)
        return td_item

    def AddTestDataNode(self, td_item, iteration_id, identifier, check):
        tda_item = self.AppendItem(td_item, identifier, ct_type=1)
        self.SetItemPyData(tda_item, iteration_id)
        self.CheckItem(tda_item, check)
        return tda_item

    def getDicIteChecked(self):
        items_checked = self.presenter.getGraphedDictionary(True)
        return  items_checked

    def getDicIteNotChecked(self):
        items_notchecked = self.presenter.getGraphedDictionary(False)
        return  items_notchecked

    def  isTreeModified(self):
        aux = self.presenter.setGraphedList()
        if self.list_shecked != aux:
            return True
        return False

    def  setGraphedList(self):
        aux = self.presenter.setGraphedList()
        return aux

    def updateListChecked(self):
        self.list_shecked = self.presenter.setGraphedList()

    def OnChecked(self, event):
        pass
#------------------------------------------------------------------------------


class ZoomPan:
    '''
    Clase encargada de gestionar de scrolling y seleccion para invocar a los
    métodos zoom y pan factory.
    '''
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None

    def zoom_factory(self, ax, fig, base_scale=2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            # get event x location
            xdata = event.xdata
            # get event y location
            ydata = event.ydata

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print event.button

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width *
                         (relx)])
            ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height *
                         (rely)])
            ax.figure.canvas.draw()

        # get the figure of interest
        fig = ax.get_figure()
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax, fig):
        def onPress(event):
            if event.inaxes != ax:
                return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None:
                return
            if event.inaxes != ax:
                return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        # get the figure of interest
        fig = ax.get_figure()

        # attach the call back
        fig.canvas.mpl_connect('button_press_event', onPress)
        fig.canvas.mpl_connect('button_release_event', onRelease)
        fig.canvas.mpl_connect('motion_notify_event', onMotion)

        # return the function
        return onMotion


class TabPanel(wx.Panel):
    '''
    Clase Panel empleada como ejemplo de pestaña para la Notebook
    '''
    """ A simple wx.Panel class. """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111, xlim=(0, 1), ylim=(0, 1),
                                 autoscale_on=False)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()
        self.axes.set_title('Click to zoom')
        x, y, s, c = np.random.rand(4, 200)
        s *= 200

        self.axes.scatter(x, y, s, c)
        scale = 1.1
        zp = ZoomPan()
        zp.zoom_factory(self.axes, self.figure, base_scale=scale)
        zp.pan_factory(self.axes, self.figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()
