# -*- coding: utf-8 -*-
'''
Created on 18/11/2014

@author: abrahan
'''

import wx

from py.una.pol.tava.presenter.pparallelcoordinatesdata_aux import\
                                                    WorkingPageDataPresenter


class WorkingPageParallelData(wx.Panel):
    def __init__(self, parent, test, mode):
        wx.Panel.__init__(self, parent)

        #------ Definiciones iniciales ----------------------------------------
        self.mode = str(mode)
        self.presenter = WorkingPageDataPresenter(self, test)
        self.InitUI(test.test_details)
        #----------------------------------------------------

    def InitUI(self, test_details):

        self.data_tree = ParallelDataTree(self, test_details)
        self.data_tree_p = self.data_tree.presenter

        self.b_plot = wx.Button(self, -1, 'Show')
        self.b_clean_filter = wx.Button(self, -1, 'Limpiar Filtro')

        self.data_figure = ParallelDataFigure(self, self.mode)
        self.data_figure_p = self.data_figure.presenter

        self.footer = FooterAUINotebook(self, self.presenter.test.test_details,
                                        self.mode)
        self.data_var_p = self.footer.data_var_p
        self.data_obj_p = self.footer.data_obj_p
        self.filters_p = self.footer.filters_p

        sizer_bf = wx.BoxSizer(wx.VERTICAL)
        sizer_bf.Add(self.b_plot)
        sizer_bf.Add(self.b_clean_filter)

        sizer_vb = wx.BoxSizer(wx.VERTICAL)
        sizer_vb.Add(self.data_tree, 5, wx.EXPAND)
        sizer_vb.Add(sizer_bf, 1, wx.EXPAND)

        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h.Add(sizer_vb, 1, wx.EXPAND)
        sizer_h.Add(self.data_figure, 3, wx.EXPAND)

        sizer_v = wx.BoxSizer(wx.VERTICAL)
        sizer_v.Add(sizer_h, 1, wx.EXPAND)
        sizer_v.Add(self.footer, 6, wx.EXPAND)

        self.SetSizer(sizer_v)

        self.Bind(wx.EVT_BUTTON, self.OnUpdateGrafic, self.b_plot)
        self.Bind(wx.EVT_BUTTON, self.OnCleanFilter, self.b_clean_filter)

        self.optionsManger()
        #------------------------------------------------------

    #referido a button graficar
    def  OnUpdateGrafic(self, event):

        ite = self.data_tree_p.getListChecked()[0]

        if self.data_tree_p.isChangeChecked():
            if(not self.presenter.fileExists(ite)):
                self.presenter.createFiles(ite)
            self.___updateView()

        elif self.filters_p.isFilterModified():
            #obtener los valores de filtros
            filters = self.filters_p.getListValues()
            #crear archivos
            self.presenter.createFilesWithFilter(ite, filters)
            self.___updateView(False)

    def ___updateView(self, new=True):

        ite_list = self.data_tree_p.getListChecked()
        self.data_figure_p.newFigureTest(ite_list)
        self.data_var_p.updateDatas(ite_list)
        self.data_obj_p.updateDatas(ite_list)
        self.filters_p.update(ite_list[0], new)

    #referido a button filtros
    def OnCleanFilter(self, event):
        ite = self.data_tree_p.getListChecked()[0]
        self.presenter.deleteFile(ite)
        self.presenter.createFiles(ite)
        self.___updateView()

    #los dos botones
    def  optionsManger(self):
        if 1 == self.data_tree_p.getLenListChecked():
            self.b_plot.Enable()
            self.b_clean_filter.Enable()
        else:
            self.b_plot.Disable()
            self.b_clean_filter.Disable()


#------------------- Arbol de Archvivos e Iteraciones -------------------------
#-------------------                                  -------------------------
import wx.lib.agw.customtreectrl as CT

from py.una.pol.tava.presenter.pparallelcoordinatesdata_aux\
                                            import ParallelDataTreePresenter


class ParallelDataTree(CT.CustomTreeCtrl):
    def __init__(self, parent, test_details):
        CT.CustomTreeCtrl.__init__(self, parent, agwStyle=CT.TR_HIDE_ROOT)

        #------ Definiciones iniciales -------------------------------
        self.parent = parent
        self.presenter = ParallelDataTreePresenter(self, test_details)
        self.InitUI()

        #------------------------------------------------------------

    def InitUI(self):

        il = wx.ImageList(16, 16)
        self.file_bmp = il.Add(I.filegraph_png)
        self.AssignImageList(il)
        self.SetBackgroundColour('#D9F0F8')

        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnChecked)

    def OnChecked(self, event):
        self.parent.optionsManger()
#------------------------------------------------------------------------------

#------------------- Figuras de Coordenadas Paralelas -------------------------
#-------------------                                  -------------------------
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar

from py.una.pol.tava.presenter.pparallelcoordinatesdata_aux import\
                                                    ParallelDataFigurePresenter


class ParallelDataFigure(wx.Panel):
    '''
    Clase Panel que contiene la configuracion para la visualizacion del
    componente de coordenadas paralelas.
    '''
    def __init__(self, parent, mode):
        wx.Panel.__init__(self, parent)

        #------ Definiciones iniciales ----------------------------------------
        self.mode = mode
        self.title_g = 'TAVA'
        self.InitUI()
        self.presenter = ParallelDataFigurePresenter(self)
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

    def showNewFigure(self, ite_list):
        self.presenter.newFigureTest(ite_list, self.title_g)
#------------------------------------------------------------------------------

#------------------- AUI Notebook par el footer       -------------------------
#-------------------                                  -------------------------
import wx.lib.agw.aui as aui


class FooterAUINotebook(aui.AuiNotebook):
    '''
    AUI Notebook class
    '''

    def __init__(self, parent, details, mode):
        '''
        Método de inicialización de la clase AUINotebook.
        :param parent: referencia al objeto padre de la clase.
        '''
        aui.AuiNotebook.__init__(self, parent=parent)

        self.default_style = (aui.AUI_NB_DEFAULT_STYLE |
                                aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER)

        self.SetWindowStyleFlag(self.default_style)
        self.SetArtProvider(aui.ChromeTabArt())

        self.data_var = ParallelDataVar(self, details, mode)
        self.data_var_p = self.data_var.presenter

        self.data_obj = ParallelDataObj(self, details, mode)
        self.data_obj_p = self.data_obj.presenter

        self.filters = AddFilterObjetivesScroll(self, details, mode)
        self.filters_p = self.filters.presenter

        self.AddPage(self.data_var, 'Variables', True)
        self.AddPage(self.data_obj, 'Objetivos', False)
        self.AddPage(self.filters, 'Filtros', False)
#------------------------------------------------------------------------------

#------------------- Pagina para visualizar Variables -------------------------
#-------------------                                  -------------------------
from  wx.lib.scrolledpanel import ScrolledPanel
import wx.dataview as dv

from py.una.pol.tava.presenter.pparallelcoordinatesdata_aux import\
                                                    ParallelDataVarPresenter


class ParallelDataVar(ScrolledPanel):
    def __init__(self, parent, details, mode):
        ScrolledPanel.__init__(self, parent, -1)
        self.parent = parent
        self.mode = mode

        l_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dvlc = dv.DataViewListCtrl(self)
        l_sizer.Add(self.dvlc, 1, flag=wx.EXPAND)

        self.SetSizer(l_sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

        self.presenter = ParallelDataVarPresenter(self, details)
#------------------------------------------------------------------------------

#------------------- Pagina para visualizar Objetivos -------------------------
#-------------------                                  -------------------------
from py.una.pol.tava.presenter.pparallelcoordinatesdata_aux import\
                                                    ParallelDataObjPresenter


class ParallelDataObj(ScrolledPanel):
    def __init__(self, parent, details, mode):
        ScrolledPanel.__init__(self, parent, -1)
        self.parent = parent
        self.mode = mode

        l_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dvlc = dv.DataViewListCtrl(self)
        l_sizer.Add(self.dvlc, 1, flag=wx.EXPAND)

        self.SetSizer(l_sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

        self.presenter = ParallelDataObjPresenter(self, details)
#------------------------------------------------------------------------------

#------------------- Scrolled para los filtros        -------------------------
#-------------------                                  -------------------------
from py.una.pol.tava.presenter.pparallelcoordinatesdata_aux import\
                                            AddFilterObjetivesScrollPresenter


class AddFilterObjetivesScroll(ScrolledPanel):
    def __init__(self, parent, details, mode):
        ScrolledPanel.__init__(self, parent, -1)

        self.parent = parent
        self.mode = mode
        self.presenter = AddFilterObjetivesScrollPresenter(self, details)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

    def addItem(self, vmin, vmax, nobj, min_v_r, max_v_r):
        value = AddFilterObjetives(self, vmin, vmax, nobj, min_v_r, max_v_r)
        self.sizer.Add(value, 1, flag=wx.EXPAND)
        return value

    def addSiserHere(self):
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()
#------------------------------------------------------------------------------

#------------------- Clase que agrega Filtros         -------------------------
#-------------------                                  -------------------------
import py.una.pol.tava.view.vimages as I


from wx import LI_VERTICAL


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

        self.min_spin = wx.SpinCtrlDouble(self, initial=self.min_value,
        min=self.min_value_r,  max=self.max_value_r, size=(30, -1), inc=0.01)
        self.min_spin.SetDigits(self.len_digits)

        sizer_in_min.Add(self.min_spin, 1, flag=wx.EXPAND)

        sizer_in_max = wx.BoxSizer(wx.VERTICAL)

        self.max_spin = wx.SpinCtrlDouble(self, initial=self.max_value,
        min=self.min_value_r,  max=self.max_value_r, size=(30, -1), inc=0.01)
        self.max_spin.SetDigits(self.len_digits)

        sizer_in_max.Add(self.max_spin, 1, flag=wx.EXPAND)

        sizer.Add(s_line, 0.5, flag=wx.EXPAND | wx.TOP, border=5)
        sizer.Add(title, 0.5, flag=wx.ALIGN_CENTER)
        sizer.Add(line, 0.5, flag=wx.EXPAND)

        sizer.Add(sizer_in_min, 1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
                                                                    border=5)
        sizer.Add(sizer_in_max, 1, flag=wx.EXPAND | wx.BOTTOM, border=10)
        sizer.Add(sizer_value_absolute, 0.5, flag=wx.EXPAND)

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
        #======================================================================
        # if self.max_spin.GetValue() > self.min_spin.GetValue():
        #     self.min_bmp.SetBitmap(I.ok_png)
        #     self.max_bmp.SetBitmap(I.ok_png)
        #     #self.parent.parent.ok_button.Enable(True)
        # else:
        #     self.min_bmp.SetBitmap(I.errornewproject_png)
        #     self.max_bmp.SetBitmap(I.errornewproject_png)
        #     #self.parent.parent.ok_button.Enable(False)
        #======================================================================
        pass

    def getObjectValues(self):
        return [self.min_spin.GetValue(), self.max_spin.GetValue()]

    def getMinValue(self):
        return self.min_spin.GetValue()

    def getMaxValue(self):
        return self.max_spin.GetValue()

    def getLengDigits(self, min_v, max_v):
        if len(str(min_v)) > len(str(max_v)):
            return len(str(min)) - 2

        return len(str(max)) - 2

    def  setValues(self, vmin, vmax):
        self.min_spin.SetValue(float(vmin))
        self.max_spin.SetValue(float(vmax))
#------------------------------------------------------------------------------
