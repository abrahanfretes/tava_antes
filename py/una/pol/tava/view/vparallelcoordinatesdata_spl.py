# -*- coding: utf-8 -*-
'''
Created on 02/02/2015

@author: abrahan
'''
import wx


#-------------------         Panel Splitter           -------------------------
#-------------------                                  -------------------------
class WorkingPageParallelSpl(wx.SplitterWindow):
    def __init__(self, parent, test, mode):
        wx.SplitterWindow.__init__(self, parent)

        #------ self customize ----------------------------------------

        self.SetMinimumPaneSize(50)
        self.SetBackgroundColour('#696969')
        self.SetBorderSize(1)

        #------ self components --------------------------------------
        self.mode = str(mode)

        self.top_panel = TopPanel(self, test, self.mode)
        self.footer = FooterAUINotebook(self, test.test_details, self.mode)
        self.SplitHorizontally(self.top_panel, self.footer,
        int(round(self.GetParent().GetSize().GetWidth() * 0.60)))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)

    #------ self controls --------------------------------------------
    def updateFooter(self, ite_list, new):
        self.footer.data_var_p.updateDatas(ite_list)
        self.footer.data_obj_p.updateDatas(ite_list)
        self.footer.filters_p.update(ite_list[0], new)

    def isFilterModified(self):
        return self.footer.filters_p.isFilterModified()

    def getListValues(self):
        return self.footer.filters_p.getListValues()


#-------------------         Panel for top            -------------------------
#-------------------                                  -------------------------
from py.una.pol.tava.presenter.pparallelcoordinatesdata_spl import\
                                                            TopPanelPresenter


class TopPanel(wx.Panel):

    def __init__(self, parent, test, mode):
        wx.Panel.__init__(self, parent)

        #------ self customize ----------------------------------------

        #------ self components --------------------------------------
        self.parent = parent
        self.presenter = TopPanelPresenter(self, test, mode)

        self.data_tree = ParallelDataTree(self, test.test_details)
        self.config = ConfigPanel(self)
        self.data_figure = ParallelDataFigure(self, mode)

        sizer_vb = wx.BoxSizer(wx.VERTICAL)
        sizer_vb.Add(self.data_tree, 5, wx.EXPAND)
        sizer_vb.Add(self.config, 1, wx.EXPAND | wx.TOP, 10)

        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h.Add(sizer_vb, 1, wx.EXPAND)
        sizer_h.Add(self.data_figure, 3, wx.EXPAND)

        sizer = wx.BoxSizer()
        sizer.Add(sizer_h, 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(sizer)

        #------ self inicailes executions ---------------------------
        self.optionsManger()

    #------ self controls --------------------------------------------
    def  optionsManger(self):
        if 1 == self.data_tree.presenter.getLenListChecked():
            self.config.enableButtons()
        else:
            self.config.disableButtons()

    def  upDateGrafic(self):

        ite = self.data_tree.presenter.getListChecked()[0]

        if self.data_tree.presenter.isChangeChecked():
            if(not self.presenter.fileExists(ite)):
                self.presenter.createFiles(ite)
            self.___updateView()

        elif self.parent.isFilterModified():
            filters = self.parent.getListValues()
            self.presenter.createFilesWithFilter(ite, filters)
            self.___updateView(False)

    def ___updateView(self, new=True):
        ite_list = self.data_tree.presenter.getListChecked()
        self.data_figure.presenter.newFigureTest(ite_list)
        self.parent.updateFooter(ite_list, new)

    def cleanFilter(self):
        ite = self.data_tree.presenter.getListChecked()[0]
        self.presenter.deleteFile(ite)
        self.presenter.createFiles(ite)
        self.___updateView()


#------------------- Arbol de Archvivos e Iteraciones -------------------------
#-------------------                                  -------------------------
import wx.lib.agw.customtreectrl as CT

from py.una.pol.tava.presenter.pparallelcoordinatesdata_spl\
                                            import ParallelDataTreePresenter


class ParallelDataTree(CT.CustomTreeCtrl):
    def __init__(self, parent, test_details):
        CT.CustomTreeCtrl.__init__(self, parent, agwStyle=CT.TR_HIDE_ROOT)

        #------ self customize ---------------------------------------
        il = wx.ImageList(16, 16)
        self.file_bmp = il.Add(I.filegraph_png)
        self.AssignImageList(il)
        self.SetBackgroundColour('#D9F0F8')

        #------ self components --------------------------------------
        self.parent = parent
        self.presenter = ParallelDataTreePresenter(self, test_details)

        #------ self inicailes executions ----------------------------
        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnChecked)

    #------ self controls -------------------------------------------
    def OnChecked(self, event):
        self.parent.optionsManger()

        #------ self customize ---------------------------------------
        #------ self components --------------------------------------
        #------ self inicailes executions ----------------------------
    #------ self controls --------------------------------------------


#------------------- Panel Control Configuracion      -------------------------
#-------------------                                  -------------------------
class ConfigPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        #------ self customize ---------------------------------------
        #------ self components --------------------------------------
        self.parent = parent
        self.SetBackgroundColour('#f8f1d9')

        self.update = wx.Button(self, -1, 'Show')
        self.clean = wx.Button(self, -1, 'Limpiar Filtro')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.update)
        sizer.Add(self.clean)

        self.SetSizer(sizer)

        #------ self inicailes executions ----------------------------
        self.Bind(wx.EVT_BUTTON, self.OnUpdateGrafic, self.update)
        self.Bind(wx.EVT_BUTTON, self.OnCleanFilter, self.clean)

    #------ self controls --------------------------------------------
    def  OnUpdateGrafic(self, event):
        self.parent.upDateGrafic()

    def OnCleanFilter(self, event):
        self.parent.cleanFilter()

    def enableButtons(self):
        self.update.Enable()
        self.clean.Enable()

    def disableButtons(self):
        self.update.Disable()
        self.clean.Disable()


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

        #------ self customize ---------------------------------------
        #------ self components --------------------------------------
        self.mode = mode
        self.title_g = 'TAVA'

        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        self.presenter = ParallelDataFigurePresenter(self)

        #------ self inicailes executions ----------------------------

    #------ self controls --------------------------------------------
    def showNewFigure(self, ite_list):
        self.presenter.newFigureTest(ite_list, self.title_g)


#------------------- AUI Notebook par el footer       -------------------------
#-------------------                                  -------------------------
import wx.lib.agw.aui as aui


class FooterAUINotebook(aui.AuiNotebook):

    def __init__(self, parent, details, mode):
        '''
        Método de inicialización de la clase AUINotebook.
        :param parent: referencia al objeto padre de la clase.
        '''
        aui.AuiNotebook.__init__(self, parent=parent)

        #------ self customize ---------------------------------------
        self.SetAGWWindowStyleFlag(aui.AUI_NB_BOTTOM)

        #------ self components --------------------------------------
        self.data_var = ParallelDataVar(self, details, mode)
        self.data_var_p = self.data_var.presenter

        self.data_obj = ParallelDataObj(self, details, mode)
        self.data_obj_p = self.data_obj.presenter

        self.filters = AddFilterObjetivesScroll(self, details, mode)
        self.filters_p = self.filters.presenter

        #------ self inicailes executions ----------------------------
        self.AddPage(self.data_var, 'Variables', True)
        self.AddPage(self.data_obj, 'Objetivos', False)
        self.AddPage(self.filters, 'Filtros', False)

    #------ self controls --------------------------------------------


#------------------- Pagina vizualizador de variables -------------------------
#-------------------                                  -------------------------
from  wx.lib.scrolledpanel import ScrolledPanel
import wx.dataview as dv

from py.una.pol.tava.presenter.pparallelcoordinatesdata_aux import\
                                                    ParallelDataVarPresenter


class ParallelDataVar(ScrolledPanel):
    def __init__(self, parent, details, mode):
        ScrolledPanel.__init__(self, parent, -1)

        #------ self customize ---------------------------------------
        #------ self components --------------------------------------
        self.parent = parent
        self.mode = mode

        l_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dvlc = dv.DataViewListCtrl(self)
        l_sizer.Add(self.dvlc, 1, flag=wx.EXPAND)

        self.SetSizer(l_sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

        self.presenter = ParallelDataVarPresenter(self, details)
        #------ self inicailes executions ----------------------------
    #------ self controls --------------------------------------------


#------------------- Pagina para visualizar Objetivos -------------------------
#-------------------                                  -------------------------
from py.una.pol.tava.presenter.pparallelcoordinatesdata_aux import\
                                                    ParallelDataObjPresenter


class ParallelDataObj(ScrolledPanel):
    def __init__(self, parent, details, mode):
        ScrolledPanel.__init__(self, parent, -1)

        #------ self customize ---------------------------------------
        #------ self components --------------------------------------
        self.parent = parent
        self.mode = mode

        l_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dvlc = dv.DataViewListCtrl(self)
        l_sizer.Add(self.dvlc, 1, flag=wx.EXPAND)

        self.SetSizer(l_sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

        self.presenter = ParallelDataObjPresenter(self, details)

        #------ self inicailes executions ----------------------------
    #------ self controls --------------------------------------------


#------------------- Scrolled para los filtros        -------------------------
#-------------------                                  -------------------------
from py.una.pol.tava.presenter.pparallelcoordinatesdata_aux import\
                                            AddFilterObjetivesScrollPresenter


class AddFilterObjetivesScroll(ScrolledPanel):
    def __init__(self, parent, details, mode):
        ScrolledPanel.__init__(self, parent, -1)

        #------ self customize ---------------------------------------
        #------ self components --------------------------------------
        self.parent = parent
        self.mode = mode
        self.presenter = AddFilterObjetivesScrollPresenter(self, details)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        #------ self inicailes executions ----------------------------

    #------ self controls --------------------------------------------
    def addItem(self, vmin, vmax, nobj, min_v_r, max_v_r):
        value = AddFilterObjetives(self, vmin, vmax, nobj, min_v_r, max_v_r)
        self.sizer.Add(value, 1, flag=wx.EXPAND)
        return value

    def addSiserHere(self):
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

#------------------- Clase contenedor de Filtros      -------------------------
#-------------------                                  -------------------------
import py.una.pol.tava.view.vimages as I


from wx import LI_VERTICAL


class AddFilterObjetives(wx.Panel):
    def __init__(self, parent, vmin, vmax, nobj, min_v_r, max_v_r):
        wx.Panel.__init__(self, parent=parent)

        #------ self customize ---------------------------------------

        #------ self components --------------------------------------
        self.parent = parent
        self.min_value_r = float(min_v_r)
        self.max_value_r = float(max_v_r)
        self.min_value = float(vmin)
        self.max_value = float(vmax)
        self.name_objetive = nobj
        self.len_digits = self.__getLengDigits()

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        s_line = wx.StaticLine(self)
        font_title = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
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

        #------ self inicailes executions ----------------------------

    #------ self controls --------------------------------------------
    def __getLengDigits(self):
        if len(str(self.min_value_r)) > len(str(self.max_value_r)):
            return len(str(self.min_value_r)) - 2
        return len(str(self.max_value_r)) - 2

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

    def setValues(self, vmin, vmax):
        self.min_spin.SetValue(float(vmin))
        self.max_spin.SetValue(float(vmax))
#------------------------------------------------------------------------------
