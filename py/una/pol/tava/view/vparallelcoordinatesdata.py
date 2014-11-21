'''
Created on 18/11/2014

@author: abrahan
'''
import os
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
import wx.dataview as dv
from  wx.lib.scrolledpanel import ScrolledPanel

from py.una.pol.tava.presenter.pparallelcoordinatesdata import\
                                                    WorkingPageDataPresenter
from py.una.pol.tava.presenter.pparallelcoordinatesdata import\
                                                    ParallelDataFigurePresenter

from py.una.pol.tava.view.vparallelcoordinates import ParallelDataTree


class WorkingPageParallelData(wx.Panel):
    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        #------ Definiciones iniciales ----------------------------------------
        self.test = test
        self.presenter = WorkingPageDataPresenter(self, test)

        #ultimas iteraciones checkeadas ParallelFigure Test
        self.checked_last_test = []

        self.InitUI()
        #----------------------------------------------------

    def InitUI(self):

        #crea una archivo por cada iteracion
        main_dic = self.presenter.setDicIterationByResult()

        self.data_tree = ParallelDataTree(self, main_dic)
        self.b_plot = wx.Button(self, -1, 'Show')
        self.data_view = ParallelDataView(self, self.presenter.test_path)
        self.data_figure = ParallelDataFigure(self, self.presenter.test_path)

        sizer_vb = wx.BoxSizer(wx.VERTICAL)
        sizer_vb.Add(self.data_tree, 5, wx.EXPAND)
        sizer_vb.Add(self.b_plot, 1, wx.EXPAND)

        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h.Add(sizer_vb, 1, wx.EXPAND)
        sizer_h.Add(self.data_figure, 3, wx.EXPAND)

        sizer_v = wx.BoxSizer(wx.VERTICAL)
        sizer_v.Add(sizer_h, 1, wx.EXPAND)
        sizer_v.Add(self.data_view, 2, wx.EXPAND)

        self.SetSizer(sizer_v)

        self.optionsManger()
        self.data_view.initDataView(self.presenter.getNameVariables())
        self.Bind(wx.EVT_BUTTON, self.OnUpDateGrafic, self.b_plot)

    def  OnUpDateGrafic(self, event):

        if self.isTreeModified():
            list_plot = self.data_tree.getCurrentListChecked()
            self.data_figure.cleanParallelFigure()
            self.data_figure.showNewFigure(list_plot)
            self.data_view.updateDataView(list_plot[0])

    def  optionsManger(self):
        if 1 == len(self.data_tree.getCurrentListChecked()):
            self.b_plot.Enable()
        else:
            self.b_plot.Disable()

    def  individualMangerGrafic(self, id_indivi):
        namefile = self.presenter.getFileForIndividual(id_indivi)
        self.data_figure.showNewIndividual(namefile)

    def isTreeModified(self):
        current_state_tree = sorted(self.data_tree.getCurrentListChecked())
        if self.checked_last_test == current_state_tree:
            return False
        self.checked_last_test = current_state_tree
        return True


class ParallelDataFigure(wx.Panel):
    '''
    Clase Panel que contiene la configuracion para la visualizacion del
    componente de coordenadas paralelas.
    '''
    def __init__(self, parent, dir_path):
        wx.Panel.__init__(self, parent)

        #------ Definiciones iniciales ----------------------------------------
        self.presenter = ParallelDataFigurePresenter(self, dir_path)
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

    #--------------------------------------------------------------------------
    #    Funciones especificas para cada tipo de grafico
    #--------------------------------------------------------------------------

    #---- Funciones definidas para ParallelFigure Test ------------------------
    def showNewFigure(self, current_plot):
        self.presenter.newFigureTest(current_plot, self.title_g)

    #------------------------------------------------------------------

    #---- Funciones definidas para ParallelFigure Test ------------------------

    def showNewIndividual(self, filename):
        self.presenter.newFigureIndividual(filename, self.title_g)


class ParallelDataView(ScrolledPanel):
    def __init__(self, parent, dir_path):
        ScrolledPanel.__init__(self, parent, -1)
        self.parent = parent
        self.countColumn = 0
        self.dir_pathl = dir_path

        l_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dvlc = dv.DataViewListCtrl(self)
        l_sizer.Add(self.dvlc, 1, flag=wx.EXPAND)

        self.SetSizer(l_sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

        #------ add event -----------------------------------------------------
        self.dvlc.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.OnSelectionRow)
        #----------------------------------------------------

    def initDataView(self, names_var):
        names_var_key = 'key,' + names_var
        columns = names_var_key.split(',')
        self.countColumn = len(columns)
        for name in columns:
            self.dvlc.AppendTextColumn(name, width=150)

    def updateDataView(self, filename):
        self.dvlc.DeleteAllItems()

        i_path = os.path.join(self.dir_pathl, filename[:-4])
        f = open(i_path)
        indi = f.readline()[:-1]
        while indi != '':
            indi_list = indi.split(',')
            self.dvlc.AppendItem(indi_list)
            indi = f.readline()[:-1]

    def  OnSelectionRow(self, event):
        row = self.dvlc.GetSelectedRow()
        list_path = []
        if row != -1:
            for column in range(self.countColumn):
                list_path.append(self.dvlc.GetTextValue(row, column))
            self.parent.individualMangerGrafic(self.dvlc.GetTextValue(row, 0))
        return None
