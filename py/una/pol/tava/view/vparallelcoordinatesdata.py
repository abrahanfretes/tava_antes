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
from wx import GetTranslation as _
import py.una.pol.tava.view.vi18n as C
from  wx.lib.scrolledpanel import ScrolledPanel

from py.una.pol.tava.presenter.pparallelcoordinatesdata import\
                                                    WorkingPageDataPresenter
from py.una.pol.tava.presenter.pparallelcoordinatesdata import\
                                                    ParallelDataFigurePresenter

from py.una.pol.tava.view.vparallelcoordinates import ParallelDataTree
from wx import LI_VERTICAL


class WorkingPageParallelData(wx.Panel):
    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        #------ Definiciones iniciales ----------------------------------------
        self.test = test
        self.presenter = WorkingPageDataPresenter(self, test)

        #ultimas iteraciones checkeadas ParallelFigure Test
        self.checked_last_test = []

        #ultimas iteraciones checkeadas ParallelFigure Test
        self.filter_objetives = {}

        self.InitUI()
        #----------------------------------------------------

    def InitUI(self):

        #crea un archivo por cada iteracion
        main_dic = self.presenter.setDicIterationByResult()

        self.data_tree = ParallelDataTree(self, main_dic)
        self.b_plot = wx.Button(self, -1, 'Show')
        self.b_filter = wx.Button(self, -1, 'Filtrar')
        self.data_view = ParallelDataView(self, self.presenter.test_path)
        self.data_figure = ParallelDataFigure(self, self.presenter.test_path)

        sizer_vb = wx.BoxSizer(wx.VERTICAL)
        sizer_vb.Add(self.data_tree, 5, wx.EXPAND)

        sizer_bf = wx.BoxSizer(wx.VERTICAL)
        sizer_bf.Add(self.b_plot)
        sizer_bf.Add(self.b_filter)

        sizer_vb.Add(sizer_bf, 1, wx.EXPAND)

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
        self.Bind(wx.EVT_BUTTON, self.OnUpDateFilter, self.b_filter)

    def OnUpDateFilter(self, event):
        list_plot = self.data_tree.getCurrentListChecked()
        print list_plot
        arg = self.presenter.dictObjetiveMinMax[list_plot[0]]
        arg1 = self.presenter.dictObjetiveMinMaxTem[list_plot[0]]
        values = AddFilterObjetivesDialog(self, arg, arg1)

    def updateFrom(self, filtros):
        list_plot = self.data_tree.getCurrentListChecked()
        self.presenter.updateForFilters(filtros, list_plot[0])
        self.___updateView()
        pass

    def  OnUpDateGrafic(self, event):

        if self.isTreeModified():
            self.___updateView()

    def ___updateView(self):

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

    def  getFiltersObjetive(self, identifier):

        return self.presenter.dictObjetiveMinMax[identifier]

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
        self.dvlc.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.OnRightClick)
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

        if row != -1:
            self.parent.individualMangerGrafic(self.dvlc.GetTextValue(row, 0))
        return None

    def OnRightClick(self, event):
        print 'llego'

        if not hasattr(self, "popupID1"):
            print 'entro 1'
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnAddFiltersObj, id=self.popupID1)
            #self.Bind(wx.EVT_MENU, self.OnDeletedAllFile, id=self.popupID2)

        # make a menu
        menu = wx.Menu()
        menu.Append(self.popupID1, 'Add Filter for Objetives')
        menu.Append(self.popupID2, 'hola1')

        self.PopupMenu(menu)
        menu.Destroy()

    def  OnAddFiltersObj(self, event):
        #aca obtener esos valores
        arg = self.parent.getFiltersObjetive(20)

        values = AddFilterObjetivesDialog(self, arg)
        print 'hollllllaaaaaaaaaaaa'
        pass


class AddFilterObjetivesDialog(wx.Dialog):
    def __init__(self, parent, values_filter, values_filter_tem):
        super(AddFilterObjetivesDialog, self).__init__(parent,
                                title='Algo', size=(650, 300),
                            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.parent = parent
        g_sizer = wx.GridBagSizer(6, 5)

        self.filter_var = AddFilterObjetivesScroll(self, values_filter, values_filter_tem)

        #------ Buttons -------------------------------------------------------
        bsizer = wx.BoxSizer(wx.HORIZONTAL)

        help_button = wx.Button(self, label=_(C.NPD_HELP))

        cancel_button = wx.Button(self, label=_(C.NPD_CAN))
        self.ok_button = wx.Button(self, label=_(C.NPD_OK))
        bsizer.Add(cancel_button, flag=wx.ALIGN_LEFT | wx.BOTTOM, border=10)
        bsizer.Add(self.ok_button, flag=wx.ALIGN_LEFT | wx.BOTTOM, border=10)

        cancel_button.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.ok_button.Bind(wx.EVT_BUTTON, self.OnOkey)
        self.ok_button.Enable(False)
        #----------------------------------------------------

        g_sizer.Add(self.filter_var, pos=(0, 0), span=(5, 7), flag=wx.EXPAND)
        g_sizer.Add(help_button, pos=(6, 0), flag=wx.LEFT, border=20)
        g_sizer.Add(bsizer, pos=(6, 1), span=(1, 6),
                  flag=wx.ALIGN_RIGHT, border=20)

        self.SetSizer(g_sizer)
        g_sizer.AddGrowableCol(0)
        g_sizer.AddGrowableRow(0)

        self.Centre()
        self.Show(True)

    def  OnOkey(self, event):
        values = self.filter_var.getListValues()
        self.parent.updateFrom(values)

        print 'okey'
        print values
        self.Close()

    def OnCancel(self, event):
        print 'cancel'
        self.Close()


class AddFilterObjetivesScroll(ScrolledPanel):
    def __init__(self, parent, values_filter, values_filter_tem):
        ScrolledPanel.__init__(self, parent, -1)
        self.parent = parent
        self.values = []
        self.init_values = values_filter_tem

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        for obj in self.init_values.keys():
            name = obj
            min_v = self.init_values[obj][0]
            max_v = self.init_values[obj][1]
            min_v_r = values_filter[obj][0]
            max_v_r = values_filter[obj][1]
            value = AddFilterObjetives(self, min_v, max_v, name, min_v_r, max_v_r)
            sizer.Add(value, 1, flag=wx.EXPAND)
            self.values.append(value)

        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

    def  getListValues(self):
        current_values = {}
        for fil in self.values:
            t_values = fil.getObjectValues()
            current_values[t_values[0]] = t_values[1]
        return current_values

import py.una.pol.tava.view.vimages as I


class AddFilterObjetives(wx.Panel):
    def __init__(self, parent, vmin, vmax, nobj, min_v_r, max_v_r):
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent
        self.min_value_r = float(min_v_r)
        self.max_value_r = float(max_v_r)
        self.min_value = float(vmin)
        self.max_value = float(vmax)
        self.name_objetive = nobj
        self.len_digits = self.__getLengDigits()
        
        print '------------'
        print self.name_objetive
        print self.min_value_r
        print self.max_value_r
        print self.min_value
        print self.max_value

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        #------ Titulo de Proyecto Tava ---------------------------------------
        s_line = wx.StaticLine(self)
        font_title = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        #font_title.SetWeight(wx.BOLD)
        font_title.SetPointSize(10)
        title = wx.StaticText(self, label=self.name_objetive, style=2)
        title.SetFont(font_title)

        line = wx.StaticLine(self)

        sizer_value_absolute = wx.BoxSizer(wx.VERTICAL)
        min_value = wx.StaticText(self, label='min: ' + str(self.min_value_r))
        sizer_value_absolute.Add(min_value, 1, flag=wx.EXPAND)
        max_value = wx.StaticText(self, label='max: ' + str(self.max_value_r))
        sizer_value_absolute.Add(max_value, 1, flag=wx.EXPAND)
        line_s = wx.StaticLine(self)
        sizer_value_absolute.Add(line_s, 1, flag=wx.EXPAND)

        sizer_in_min = wx.BoxSizer(wx.VERTICAL)
        sizer_in_min_b = wx.BoxSizer(wx.HORIZONTAL)
        self.min_bmp = wx.StaticBitmap(self)
        self.min_bmp.SetBitmap(I.warningnewproject_png)
        in_min_value = wx.StaticText(self, label='new min')
        sizer_in_min_b.Add(self.min_bmp, flag=wx.LEFT, border=2)
        sizer_in_min_b.Add(in_min_value, 0.3, flag=wx.EXPAND)

        self.min_spin = wx.SpinCtrlDouble(self, initial=self.min_value,
        min=self.min_value_r,  max=self.max_value_r, size=(30, -1), inc=0.01)
        #self.min_spin.SetMin(self.min_value_r)
        #self.min_spin.SetMax(self.max_value_r)
        self.min_spin.SetDigits(self.len_digits)

        #v_in_min_value = wx.TextCtrl(self)
        sizer_in_min.Add(sizer_in_min_b, 0.3, flag=wx.EXPAND)
        sizer_in_min.Add(self.min_spin, 1, flag=wx.EXPAND)

        sizer_in_max = wx.BoxSizer(wx.VERTICAL)

        sizer_in_max_b = wx.BoxSizer(wx.HORIZONTAL)
        self.max_bmp = wx.StaticBitmap(self)
        self.max_bmp.SetBitmap(I.warningnewproject_png)
        in_max_value = wx.StaticText(self, label='new max')
        sizer_in_max_b.Add(self.max_bmp, flag=wx.LEFT, border=2)
        sizer_in_max_b.Add(in_max_value, 0.3, flag=wx.EXPAND)

        self.max_spin = wx.SpinCtrlDouble(self, initial=self.max_value,
        min=self.min_value_r,  max=self.max_value_r, size=(30, -1), inc=0.01)
        #self.max_spin.SetMin(self.min_value_r)
        #self.max_spin.SetMax(self.max_value_r)
        self.max_spin.SetDigits(self.len_digits)

        sizer_in_max.Add(sizer_in_max_b, 0.3, flag=wx.EXPAND)
        sizer_in_max.Add(self.max_spin, 1, flag=wx.EXPAND)

        sizer.Add(s_line, 0.5, flag=wx.EXPAND | wx.TOP, border=5)
        sizer.Add(title, 0.5, flag=wx.ALIGN_CENTER)
        sizer.Add(line, 0.5, flag=wx.EXPAND)

        sizer.Add(sizer_value_absolute, 0.5, flag=wx.EXPAND)

        sizer.Add(sizer_in_min, 1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
                                                                    border=5)
        sizer.Add(sizer_in_max, 1, flag=wx.EXPAND | wx.BOTTOM, border=10)

        line_ver1 = wx.StaticLine(self, style=LI_VERTICAL)
        sizer_main.Add(line_ver1, 0.1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
                                                                    border=5)
        sizer_main.Add(sizer, 1, flag=wx.EXPAND)
        line_ver = wx.StaticLine(self, style=LI_VERTICAL)
        sizer_main.Add(line_ver, 0.1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
                                                                    border=5)

        self.SetSizer(sizer_main)

        self.max_spin.Bind(wx.EVT_SPINCTRLDOUBLE, self.validateValues)
        self.min_spin.Bind(wx.EVT_SPINCTRLDOUBLE, self.validateValues)

        self.max_spin.Bind(wx.EVT_KEY_UP, self.validateValues)
        self.min_spin.Bind(wx.EVT_KEY_UP, self.validateValues)

    def __getLengDigits(self):
        if len(str(self.min_value_r)) > len(str(self.max_value_r)):
            return len(str(self.min_value_r)) - 2

        return len(str(self.max_value_r)) - 2

    def validateValues(self, event):
        if self.max_spin.GetValue() > self.min_spin.GetValue():
            self.min_bmp.SetBitmap(I.ok_png)
            self.max_bmp.SetBitmap(I.ok_png)
            self.parent.parent.ok_button.Enable(True)
        else:
            self.min_bmp.SetBitmap(I.errornewproject_png)
            self.max_bmp.SetBitmap(I.errornewproject_png)
            self.parent.parent.ok_button.Enable(False)

    def getObjectValues(self):
        return (self.name_objetive,
                (self.min_spin.GetValue(),
                self.max_spin.GetValue()))
