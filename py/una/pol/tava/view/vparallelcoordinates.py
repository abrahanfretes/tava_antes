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
from pandas import read_csv
from pandas.tools.plotting import andrews_curves

parallel_suplot = tipo_graphict = 1


class WorkingPageParallel(wx.Panel):
    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        #------ Definiciones iniciales ----------------------------------------
        self.test = test
        self.presenter = WorkingPagePresenter(self, test)

        self.InitUI()
        #----------------------------------------------------

    def InitUI(self):

        # una Pagina consiste en:
        # Una o mas figuras y,
        # Unas configuraciones
        self.data = ParallelData(self, self.test)
        self.options = ParallelDataOptions(self)
        self.figure = ParallelFigure(self)

        box_config = wx.BoxSizer(wx.VERTICAL)
        box_config.Add(self.data, 2, wx.EXPAND)
        box_config.Add(self.options, 1, wx.EXPAND)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(box_config, 1, wx.EXPAND)
        sizer.Add(self.figure, 3, wx.EXPAND)
        self.SetSizer(sizer)

        self.presenter.setDicIterationByResult()
        keys_result = self.presenter.dic_path_iteration.keys()
        self.figure.createKeysForSubPlot(keys_result)

    def showGraphicTava(self):

        if self.isFirstInvocation():
            cleaned_dic = self.clearDicChecked(self.data.getDicIteChecked())
            new_dic = self.presenter.updateDicCheckedLast(cleaned_dic)
            dic_path_plot = self.presenter.createFileForParallel(new_dic)
            self.figure.showSubplots(dic_path_plot)
            self.data.updateListChecked()

            self.figure.showed_figure = True
            self.options.UpDateNameButton()
        else:
            modified = self.data.isTreeModified()
            if modified:
                cleaned_dic = self.data.getDicIteChecked()
                #print  cleaned_dic
                new_dic = self.presenter.updateDicCheckedLast(cleaned_dic)
                #print  new_dic
                dic_path_plot = self.presenter.createFileForParallel(new_dic)
                print dic_path_plot
                self.figure.updateSubplots(dic_path_plot)
                self.data.updateListChecked()

            else:
                print  'Arbol no modificado'

    def  isFirstInvocation(self):
            return not self.figure.showed_figure

    def clearDicChecked(self, dic_checked):
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

    def createKeysForSubPlot(self, keys_result):
        self.presenter.createKeysForSubPlot(sorted(keys_result))

    def  showSubplots(self, dic_for_plot):
        self.presenter.showSubplots(dic_for_plot)

    def  updateSubplots(self, dic_for_plot):
        self.presenter.updateSubplots(dic_for_plot)

    def CreateSubplots(self, dic_for_plot):
        self.presenter.createSubplots(dic_for_plot)

    def UpdateSubplots(self, dic_for_plot):
        self.presenter.updateSubplots(dic_for_plot)

    def ShowAndrewsCurves(self, file_path, c_plot):
        axe = self.figure.add_subplot(c_plot)
        df = read_csv(file_path)
        axe = andrews_curves(df, 'Name', axe)

        self.canvas.draw()
#------------------- Config Data ------------------------------------------


class ParallelData(CT.CustomTreeCtrl):
    def __init__(self, parent, test):
        CT.CustomTreeCtrl.__init__(self, parent,
                                agwStyle=CT.TR_HIDE_ROOT)

        #------ Definiciones iniciales ----------------------------------------
        self.presenter = ParallelDataPresenter(self)

        self.test = test
        self.root = self.AddRoot("Test Data")

        #lista de  iteraciones checkeadas
        self.list_shecked = []

        il = wx.ImageList(16, 16)
        self.file_bmp = il.Add(I.filegraph_png)
        self.AssignImageList(il)
        self.SetBackgroundColour('#D9F0F8')

        self.InitUI()
        #----------------------------------------------------

    def InitUI(self):

        # Inicializacion del arbol de proyectos
        self.presenter.InitializeTree(self.test)
        self.presenter.expandItemTree()

        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnChecked)

        #----------------------------------------------------

    def updateListChecked(self):
        self.list_shecked = self.presenter.setGraphedList()

    def getDicIteChecked(self):
        items_checked = self.presenter.getGraphedDictionary()
        return  items_checked

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

    def  isTreeModified(self):
        aux = self.presenter.setGraphedList()
        if self.list_shecked != aux:
            return True
        return False

    def  getPlottedInteractions(self):
        to_ret = []
        for item_result in self.root.GetChildren():
            for item_ite in item_result.GetChildren():
                if self.IsItemChecked(item_ite):
                    to_ret.append(self.GetItemPyData(item_ite))

        return to_ret

    def OnChecked(self, event):
        pass
        #======================================================================
        # print 'OnChecked'
        # print  self.getDicIteChecked
        # print  self.list_shecked
        #======================================================================


class ParallelDataOptions(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.button_grafic = wx.Button(self, -1, 'Show')
        self.Bind(wx.EVT_BUTTON, self.OnUpDateGrafic, self.button_grafic)

    def OnUpDateGrafic(self, event):
        self.parent.showGraphicTava()

    def UpDateNameButton(self):
        self.button_grafic.SetLabel('Update')


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
