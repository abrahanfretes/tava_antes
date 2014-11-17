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

TYPE_TEST = 0
TYPE_RESULT = 1
TYPE_ITERATION = 2
TYPE_SEQUENTIAL = 3


class WorkingPageParallel(wx.Panel):
    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        #------ Definiciones iniciales ----------------------------------------
        self.test = test
        self.presenter = WorkingPagePresenter(self, test)

        #ultimas iteraciones checkeadas ParallelFigure Test
        self.checked_last_test = []

        #ultimas iteraciones checkeadas ParallelFigure Result
        self.checked_last_result = {}

        #ultimas iteraciones checkeadas ParallelFigure Iteration
        self.checked_last_iteration = []

        #ultimas iteraciones checkeadas ParallelFigure Sequential
        self.checked_last_sequential = []

        self.type_figure_last = None

        self.InitUI()
        #----------------------------------------------------

    def InitUI(self):

        #crea una archivo por cada iteracion
        main_dic = self.presenter.setDicIterationByResult()

        # una Pagina consiste en:
        # Una o mas figuras y,
        # Unas configuraciones
        self.data = ParallelDataTree(self, main_dic)
        self.options = ParallelDataOptions(self)
        self.figure = ParallelFigure(self, self.presenter.test_path)

        box_config = wx.BoxSizer(wx.VERTICAL)
        box_config.Add(self.data, 2, wx.EXPAND)
        box_config.Add(self.options, 1, wx.EXPAND)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(box_config, 1, wx.EXPAND)
        sizer.Add(self.figure, 3, wx.EXPAND)
        self.SetSizer(sizer)

        self.figure.initializeFigureResult(main_dic.keys())
        self.optionsManger()

    def  isTypeModified(self):
        type_aux = self.options.getTypeSelection()
        if self.type_figure_last != type_aux:
            return True
        return False

    def updateTypeFigure(self):
        self.type_figure_last = self.options.getTypeSelection()

    def isTreeModified(self):

        type_p = self.options.getTypeSelection()
        current_state_tree = sorted(self.data.getGraphedList())
        last_state_tree = sorted(self.getLastStateTree(type_p))

        if current_state_tree == last_state_tree:
            return False
        return True

    def getLastStateTree(self, type_p):
        if type_p == TYPE_TEST:
            return self.checked_last_test
        elif type_p == TYPE_RESULT:
            return self.presenter.getListByDic(self.checked_last_result)
        elif type_p == TYPE_ITERATION:
            return self.checked_last_iteration
        elif type_p == TYPE_SEQUENTIAL:
            return self.checked_last_sequential

    def getCurrentStateTree(self, type_p):
        if type_p == TYPE_TEST:
            return self.data.getGraphedList()
        elif type_p == TYPE_RESULT:
            return self.presenter.getListByDic(
                                            self.data.getCurrentDicChecked())
        elif type_p == TYPE_ITERATION:
            #se debera actualizar
            return self.checked_last_iteration
        elif type_p == TYPE_SEQUENTIAL:
            #se debera actualizar
            return self.checked_last_sequential

    def updateListChecked(self):
        type_f = self.options.getTypeSelection()

        if type_f == TYPE_TEST:
            self.checked_last_test = self.data.getGraphedList()
        elif type_f == TYPE_RESULT:
            self.checked_last_result = self.data.getCurrentDicChecked()
        elif type_f == TYPE_ITERATION:
            self.checked_last_iteration = self.data.getGraphedList()
        elif type_f == TYPE_SEQUENTIAL:
            self.checked_last_sequential = self.data.getGraphedList()

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

    def showOnlyTreeModified(self, type_f):

        if type_f == TYPE_TEST:
            list_c = self.data.getCurrentListChecked()
            self.figure.showUpdateFigure(list_c, self.checked_last_test)
        elif type_f == TYPE_RESULT:
            dic_c = self.data.getCurrentDicChecked()
            self.figure.showUpdateSubplot(dic_c, self.checked_last_result)
        elif type_f == TYPE_ITERATION:
            self.figure.cleanParallelFigure()
            lit_c = self.data.getCurrentListChecked()
            self.figure.showNewIteration(lit_c)
        elif type_f == TYPE_SEQUENTIAL:
            list_c = self.data.getCurrentListChecked()
            self.figure.showNewSequencial(list_c)

    def showOnlyTypeModified(self, type_f):

        if type_f == TYPE_TEST:
            list_plot = self.data.getCurrentListChecked()
            self.figure.showNewFigure(list_plot)
        elif type_f == TYPE_RESULT:
            dic_checked = self.data.getCurrentDicChecked()
            self.figure.showNewSubplot(dic_checked)
        elif type_f == TYPE_ITERATION:
            list_plot = self.data.getCurrentListChecked()
            self.figure.showNewIteration(list_plot)
        elif type_f == TYPE_SEQUENTIAL:
            list_c = self.data.getCurrentListChecked()
            self.figure.showNewSequencial(list_c)

    def showTreeAndTypeModified(self, type_f):

        if type_f == TYPE_TEST:
            list_plot = self.data.getCurrentListChecked()
            self.figure.showNewFigure(list_plot)
        elif type_f == TYPE_RESULT:
            dic_checked = self.data.getCurrentDicChecked()
            self.figure.showNewSubplot(dic_checked)
        elif type_f == TYPE_ITERATION:
            list_plot = self.data.getCurrentListChecked()
            self.figure.showNewIteration(list_plot)
        elif type_f == TYPE_SEQUENTIAL:
            list_c = self.data.getCurrentListChecked()
            self.figure.showNewSequencial(list_c)

    def optionsManger(self):
        if(len(self.data.getCurrentListChecked()) == 0):
            self.options.setDisableAllCheckOptions()
        elif(len(self.data.getCurrentListChecked()) > 1):
            self.options.setEnableAllCheckOptions()
            self.options.setDisableCheckSequence()
        else:
            self.options.setEnableAllCheckOptions()

    #------------------------------------------------------------------


class ParallelFigure(wx.Panel):
    '''
    Clase Panel que contiene la configuracion para la visualizacion del
    componente de coordenadas paralelas.
    '''
    def __init__(self, parent, dir_path):
        wx.Panel.__init__(self, parent)

        #------ Definiciones iniciales ----------------------------------------
        self.presenter = ParallelFigurePresenter(self, dir_path)
        self.title_g = 'TAVA'
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

    #--------------------------------------------------------------------------
    #    Funciones especificas para cada tipo de grafico
    #--------------------------------------------------------------------------

    #---- Funciones definidas para ParallelFigure Test ------------------------
    def showNewFigure(self, current_plot):
        self.presenter.newFigureTest(current_plot, self.title_g)

    def showUpdateFigure(self, current_plot, last_plot):
        self.presenter.updateFigureTest(current_plot, last_plot)

    #---- Funciones definidas para ParallelFigure Result ----------------------
    def initializeFigureResult(self, keys_result):
        self.presenter.initializeFigureResult(sorted(keys_result))

    def  showNewSubplot(self, dic_for_plot):
        self.presenter.newFigureResult(dic_for_plot, self.title_g)

    def  showUpdateSubplot(self, current_plot, last_plot):
        self.presenter.updateFigureResult(current_plot, last_plot,
                                                                self.title_g)

    def ShowAndrewsCurves(self, file_path, c_plot):
        axe = self.figure.add_subplot(c_plot)
        df = read_csv(file_path)
        axe = andrews_curves(df, 'Name', axe)
        self.canvas.draw()

    #---- Funciones definidas para ParallelFigure Iteration -------------------
    def showNewIteration(self, list_plot):
        self.presenter.newFigureIteration(list_plot, self.title_g)

    #---- Funciones definidas para ParallelFigure Sequential ------------------
    def showNewSequencial(self, path_plot):
        self.presenter.newFigureSequential(path_plot, self.title_g)

    #------------------------------------------------------------------


#------------------- Set Test Actions Options ---------------------------------
class ParallelDataOptions(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.presenter = ParallelDataOptionsPresenter(self)
        self.styleNameList = ['Test', 'Result', 'Iteracion', 'Secuencial']
        self.InitUI()
        #----------------------------------------------------

    def InitUI(self):
        dimension = len(self.styleNameList)
        self.radiob = wx.RadioBox(self, -1, 'tipo grafico por:',
            wx.DefaultPosition, wx.DefaultSize, self.styleNameList, dimension,
            wx.RA_SPECIFY_ROWS)

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

    def  setDisableCheckSequence(self):
        self.radiob.EnableItem(3, False)

    def  setEnableCheckSequence(self):
        self.radiob.EnableItem(3, True)

    def  setEnableAllCheckOptions(self):
        for option in range(len(self.styleNameList)):
            self.radiob.EnableItem(option, True)

    def  setDisableAllCheckOptions(self):
        for option in range(len(self.styleNameList)):
            self.radiob.EnableItem(option, False)

#------------------------------------------------------------------------------


#------------------- Config Tree Test Data ------------------------------------
class ParallelDataTree(CT.CustomTreeCtrl):
    def __init__(self, parent, main_dic):
        CT.CustomTreeCtrl.__init__(self, parent, agwStyle=CT.TR_HIDE_ROOT)

        #------ Definiciones iniciales -------------------------------
        self.parent = parent
        self.presenter = ParallelDataPresenter(self)
        self.root = self.AddRoot("Test Data")

        #lista de  iteraciones checkeadas
        self.list_shecked = []

        self.InitUI(main_dic)
        #------------------------------------------------------------

    def InitUI(self, main_dic):

        il = wx.ImageList(16, 16)
        self.file_bmp = il.Add(I.filegraph_png)
        self.AssignImageList(il)
        self.SetBackgroundColour('#D9F0F8')

        # Inicializacion del arbol de proyectos
        self.presenter.InitializeTree(main_dic)
        self.presenter.expandItemTree()

        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnChecked)

    def AddTestDetailNode(self, result_id, resul_name):
        td_item = self.AppendItem(self.root, resul_name)
        self.SetItemPyData(td_item, result_id)
        self.SetItemImage(td_item, 0, wx.TreeItemIcon_Normal)
        return td_item

    def AddTestDataNode(self, td_item, i_name, identifier, check):
        tda_item = self.AppendItem(td_item, identifier, ct_type=1)
        self.SetItemPyData(tda_item, i_name)
        self.CheckItem(tda_item, check)
        return tda_item

    def getCurrentListChecked(self):
        items_checked = self.presenter.getCurrentListChecked(True)
        return  items_checked

    def getCurrentDicChecked(self):
        items_checked = self.presenter.getCurrentDicChecked(True)
        return  items_checked

    def  isTreeModified(self):
        aux = self.presenter.getGraphedList()
        if self.list_shecked != aux:
            return True
        return False

    def  getGraphedList(self):
        aux = self.presenter.getGraphedList()
        return aux

    def updateListChecked(self):
        self.list_shecked = self.presenter.getGraphedList()

    def OnChecked(self, event):
        self.parent.optionsManger()
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
