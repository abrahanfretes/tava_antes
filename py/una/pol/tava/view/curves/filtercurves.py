#  -*- coding: utf-8 -*-
'''
Created on 2/5/2015

@author: abrahan
'''
import wx
from wx import GetTranslation as _
import wx.lib.agw.aui as aui
from wx import dataview as dv
from wx.lib.scrolledpanel import ScrolledPanel

from py.una.pol.tava.view import vi18n as C


class CurvesFilter(wx.Panel):
    def __init__(self, parent, page_curves, test):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        self.tab_aui = aui.AuiNotebook(self)
        self.tab_aui.SetAGWWindowStyleFlag(aui.AUI_NB_TOP)
        self.InitUI()
        self.presenter = CurvesFilterPresenter(self, test)

        sizer = wx.BoxSizer()
        sizer.Add(self.tab_aui, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # ------ self inicailes executions ----------------------------

    def InitUI(self):
        self.var = dv.DataViewListCtrl(self.tab_aui)
        self.obj = dv.DataViewListCtrl(self.tab_aui)
        self.fil = ScrolledPanel(self.tab_aui)

        self.tab_aui.AddPage(self.var, _(C.FAN_V), False)
        self.tab_aui.AddPage(self.obj, _(C.FAN_O), False)
        self.tab_aui.AddPage(self.fil,  _(C.FAN_F), False)

        self.sizer_aux = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_fil = wx.BoxSizer(wx.VERTICAL)
        self.sizer_fil.Add(self.sizer_aux, 1, wx.EXPAND)
        self.fil.SetSizer(self.sizer_fil)

    def deltePages(self):
        self.tab_aui.DeletePage(self.tab_aui.GetPageIndex(self.var))
        self.tab_aui.DeletePage(self.tab_aui.GetPageIndex(self.obj))
        self.tab_aui.DeletePage(self.tab_aui.GetPageIndex(self.fil))

    def addItemFil(self, vmin, vmax, nobj, min_v_r, max_v_r):
        value = FilterObjetives(self.fil, vmin, vmax, nobj, min_v_r, max_v_r)
        self.sizer_aux.Add(value, 1, flag=wx.EXPAND)
        return value

    def addSiserHere(self):
        self.fil.SetSizer(self.sizer_fil)
        self.fil.SetAutoLayout(1)
        self.fil.SetupScrolling()

    # ------ self controls --------------------------------------------


from py.una.pol.tava.model.mcurves import AndrewsCurvesModel as acm


class CurvesFilterPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        self.InitUI()

    def InitUI(self):

        # inicialización para valores de variables
        ac = acm().getCurvesByTestId(self.test.id)
        v_names = ac.name_variable
        columns = v_names.split(',')
        self.countColumn = len(columns)
        self.iview.var.AppendTextColumn('key', width=50)
        for name in columns:
            self.iview.var.AppendTextColumn(name, width=110)

        # inicialización para valores de objetivos
        o_names = ac.order_name_obj
        columns = o_names.split(',')
        self.countColumn = len(columns)
        self.iview.obj.AppendTextColumn('key', width=50)
        for name in columns:
            self.iview.obj.AppendTextColumn(name, width=150)

    def updateValuesList(self, ite_list):
        ite = ite_list[0]
        self.iview.deltePages()

        self.iview.InitUI()
        self.InitUI()

        # actualizacion de variables
        for var in acm().getListVariables(ite):
            self.iview.var.AppendItem(var)

        # actualizacion de objetivos
        for obj in acm().getListObjectives(ite):
            self.iview.obj.AppendItem(obj)

        # actualizacion de Objetivos
        # filtro las variables correspondientes
        vmin, vmax = acm().getMinMaxObjective(ite)

        # obtengo los nombres
        ac = acm().getCurvesByTestId(self.test.id)
        names = ac.order_name_obj.split(',')

        # creo los filtros
        self.values = []

        if len(names) == len(vmin):
            for index in range(len(names)):
                value = self.iview.addItemFil(vmin[index], vmax[index],
                                              names[index], vmin[index],
                                              vmax[index])
                self.values.append(value)
        # actualizo la vista
        self.iview.addSiserHere()
        self.updateBeforeValues()

    def updateBeforeValues(self):
        self.min_before = []
        self.max_before = []
        for value in self.values:
            self.min_before.append(value.getMinValue())
            self.max_before.append(value.getMaxValue())

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


# ------------------- Clase para Filtros  Individual   ------------------------
# -------------------                                  ------------------------
class FilterObjetives(wx.Panel):
    def __init__(self, parent, vmin, vmax, nobj, min_v_r, max_v_r):
        wx.Panel.__init__(self, parent=parent)

        # ------ self customize ---------------------------------------

        # ------ self components --------------------------------------
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
                                          min=self.min_value_r,
                                          max=self.max_value_r, size=(30, -1),
                                          inc=0.01)
        self.min_spin.SetDigits(self.len_digits)

        sizer_in_min.Add(self.min_spin, 1, flag=wx.EXPAND)

        sizer_in_max = wx.BoxSizer(wx.VERTICAL)

        self.max_spin = wx.SpinCtrlDouble(self, initial=self.max_value,
                                          min=self.min_value_r,
                                          max=self.max_value_r, size=(30, -1),
                                          inc=0.01)
        self.max_spin.SetDigits(self.len_digits)

        sizer_in_max.Add(self.max_spin, 1, flag=wx.EXPAND)

        sizer.Add(s_line, 0.5, flag=wx.EXPAND | wx.TOP, border=5)
        sizer.Add(title, 0.5, flag=wx.ALIGN_CENTER)
        sizer.Add(line, 0.5, flag=wx.EXPAND)

        sizer.Add(sizer_in_min, 1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
                  border=5)
        sizer.Add(sizer_in_max, 1, flag=wx.EXPAND | wx.BOTTOM, border=10)
        sizer.Add(sizer_value_absolute, 0.5, flag=wx.EXPAND)

        line_ver1 = wx.StaticLine(self, style=wx.LI_VERTICAL)
        sizer_main.Add(line_ver1, 0.1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
                       border=5)
        sizer_main.Add(sizer, 1, flag=wx.EXPAND)
        line_ver = wx.StaticLine(self, style=wx.LI_VERTICAL)
        sizer_main.Add(line_ver, 0.1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
                       border=5)

        self.SetSizer(sizer_main)

        # ------ self inicailes executions ----------------------------

    # ------ self controls --------------------------------------------
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
