#  -*- coding: utf-8 -*-
'''
Created on 25/2/2015

@author: abrahan
'''
import wx
from wx import GetTranslation as _

import py.una.pol.tava.view.vi18n as C
# _(C.NPD_TP)


# -------------------         Panel Splitter           ------------------------
# -------------------                                  ------------------------
class WorkingPageFl(wx.SplitterWindow):
    def __init__(self, parent, test, mode):
        wx.SplitterWindow.__init__(self, parent)

        #  ------ self customize ----------------------------------------

        self.SetMinimumPaneSize(50)
        self.SetBackgroundColour("#696969")
        self.SetBorderSize(1)

        #  ------ self components --------------------------------------
        self.mode = str(mode)
        self.top_panel = TopPanel(self, test, self.mode)
        self.footer = FooterAUINotebook(self, test, self.mode)
        self.SplitHorizontally(self.top_panel, self.footer,
                               int(round(self.GetParent().GetSize().
                                         GetWidth() * 0.50)))
        # ------ self controls -----------------------------------------


# -------------------         Panel for top            ------------------------
# -------------------                                  ------------------------
from py.una.pol.tava.presenter.pparallel.pparallelcoordinatesal import\
    TopPanelPresenter


class TopPanel(wx.Panel):

    def __init__(self, parent, test, mode):
        wx.Panel.__init__(self, parent)

        # ------ self customize ----------------------------------------
        # ------ self components --------------------------------------
        self.parent = parent
        self.presenter = TopPanelPresenter(self, test, mode)
        self.data_tree = ParallelTreeAL(self, test.test_details)
        self.data_figure = ParallelDataFigure(self, mode, test)

        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h.Add(self.data_tree, 1, wx.EXPAND)
        sizer_h.Add(self.data_figure, 3, wx.EXPAND)

        sizer = wx.BoxSizer()
        sizer.Add(sizer_h, 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(sizer)
        # ------ self inicailes executions -----------------------------
        # ------ self controls -----------------------------------------


# ------------------- Arbol de Archvivos e Iteraciones ------------------------
# -------------------                                  ------------------------
import wx.lib.agw.customtreectrl as CT

from py.una.pol.tava.presenter.pparallel.pparallelcoordinatesal import\
    ParallelDataTreePresenter


class ParallelTreeAL(CT.CustomTreeCtrl):
    def __init__(self, parent, test_details):
        CT.CustomTreeCtrl.__init__(self, parent, agwStyle=CT.TR_HIDE_ROOT)

        # ------ self customize ---------------------------------------
        il = wx.ImageList(16, 16)
        self.file_bmp = il.Add(I.filegraph_png)
        self.AssignImageList(il)
        self.SetBackgroundColour('#D9F0F8')

        # ------ self components --------------------------------------
        self.parent = parent
        self.presenter = ParallelDataTreePresenter(self, test_details)

        # ------ self inicailes executions ----------------------------
        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnChecked)

    # ------ self controls -------------------------------------------
    def OnChecked(self, event):
        self.presenter.setChecked()
        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        # ------ self inicailes executions ----------------------------
    # ------ self controls --------------------------------------------


# ------------------- Figuras de Coordenadas Paralelas ------------------------
# -------------------                                  ------------------------
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
import py.una.pol.tava.view.vimages as I

from py.una.pol.tava.presenter.pparallel.pparallelcoordinatesal import\
    ParallelDataFigurePresenter


class ParallelDataFigure(wx.Panel):
    '''
    Clase Panel que contiene la configuracion para la visualizacion del
    componente de coordenadas paralelas.
    '''
    def __init__(self, parent, mode, test):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        self.parent = parent
        self.mode = mode

        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()
        self.button_tolbar = ButtonsTollFigure(self, test)

        self.sizer_toll = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_toll.Add(self.button_tolbar, 4)
        self.sizer_toll.Add(self.toolbar, 1)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer_toll, 0, wx.LEFT | wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

        self.presenter = ParallelDataFigurePresenter(self, test)

        # ------ self inicailes executions ----------------------------
    # ------ self controls --------------------------------------------
    def showNewFigure(self, ite_list):
        self.presenter.newFigureTest(ite_list)

    def cleanFilter(self):
        self.parent.cleanFilter()


# ------------------- Panel Control Configuracion      ------------------------
# -------------------                                  ------------------------


from py.una.pol.tava.presenter.pparallel.pparallelcoordinatesal import\
    ButtonsTollFigurePresenter


class ButtonsTollFigure(wx.Panel):
    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
        self.SetBackgroundColour('#f8f1d9')

        # ------ self components --------------------------------------
        self.parent = parent
        self.update = wx.BitmapButton(self, -1, I.graficar_parallel,
                                      style=wx.NO_BORDER)
        self.update.SetToolTipString(_(C.BTF_UF))

        s_line_update = wx.StaticLine(self, style=LI_VERTICAL)

        self.rename_obj = wx.BitmapButton(self, -1, I.rename_png,
                                          style=wx.NO_BORDER)
        self.rename_obj.SetToolTipString(_(C.BTF_RN))

        self.config = wx.BitmapButton(self, -1, I.update_config,
                                      style=wx.NO_BORDER)
        self.config.SetToolTipString(_(C.BTF_NC))

        self.objetives = wx.BitmapButton(self, -1, I.list_objetives,
                                         style=wx.NO_BORDER)
        self.objetives.SetToolTipString(_(C.BTF_FO))

        self.sort_objetive = wx.BitmapButton(self, -1, I.sort_objetive,
                                             style=wx.NO_BORDER)
        self.sort_objetive.SetToolTipString(_(C.BTF_OO))

        s_line = wx.StaticLine(self, style=LI_VERTICAL)

        self.filters = wx.BitmapButton(self, -1, I.update_figure,
                                       style=wx.NO_BORDER)
        self.filters.SetToolTipString(_(C.BTF_ESF))

        self.clean = wx.BitmapButton(self, -1, I.clear_filters,
                                     style=wx.NO_BORDER)
        self.clean.SetToolTipString(_(C.BTF_CF))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.update)
        sizer.Add(s_line_update, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=4)
        sizer.Add(self.rename_obj)
        sizer.Add(self.config)
        sizer.Add(self.objetives)
        sizer.Add(self.sort_objetive)
        sizer.Add(s_line, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=4)
        sizer.Add(self.filters)
        sizer.Add(self.clean)

        self.SetSizer(sizer)

        self.presenter = ButtonsTollFigurePresenter(self, test)
        # ------ self inicailes executions ----------------------------
        self.Bind(wx.EVT_BUTTON, self.OnClickUpdateGrafic, self.update)
        self.Bind(wx.EVT_BUTTON, self.OnClickRename, self.rename_obj)
        self.Bind(wx.EVT_BUTTON, self.OnClickConfiguration, self.config)
        self.Bind(wx.EVT_BUTTON, self.OnFilterObjetives, self.objetives)
        self.Bind(wx.EVT_BUTTON, self.OnSortObjetives, self.sort_objetive)
        self.Bind(wx.EVT_BUTTON, self.OnFilterObjetive, self.filters)
        self.Bind(wx.EVT_BUTTON, self.OnCleanFilter, self.clean)

    # ------ self controls --------------------------------------------
    def OnClickUpdateGrafic(self, event):
        self.presenter.verifyTreeCheckeo()

    def OnClickRename(self, event):
        list_obj, list_var = self.presenter.getNamesObjetives()
        RenameObjetivoDialog(self, list_obj, list_var)

    def OnClickConfiguration(self, event):
        pa = self.presenter.getParallelAnalizer()
        CustomizeFrontFigure(self, pa.legent, pa.color_lines)

    def OnFilterObjetives(self, event):
        CustomizeObjetives(self)

    def OnSortObjetives(self, event):
        d = SortObjetiveDialog(self, self.presenter.getUpdateSort())
        d.ShowModal()

    def OnFilterObjetive(self, event):
        self.presenter.setFilters()

    def OnCleanFilter(self, event):
        self.presenter.cleanFilter()

    def enableButtons(self):
        self.update.Enable()
        self.clean.Enable()
        self.config.Enable()
        self.objetives.Enable()
        self.sort_objetive.Enable()
        self.filters.Enable()
        self.rename_obj.Enable()

    def disableButtons(self):
        self.update.Disable()
        self.clean.Disable()
        self.config.Disable()
        self.objetives.Disable()
        self.sort_objetive.Disable()
        self.filters.Disable()
        self.rename_obj.Disable()

    def updateConfigPa(self, legent_figure, color_figure):
        self.presenter.updateConfigPa(legent_figure, color_figure)

    def restartDefaul(self):
        self.presenter.restartDefaul()

    def getConfigObV(self):
        return self.presenter.getStatesObjetives()

    def setUpdateListObjetiveV(self, list_obj):
        return self.presenter.setUpdateListObjetive(list_obj)

    def setUpdateSortV(self, new_order_list):
        self.presenter.setUpdateSort(new_order_list)

    def updateNamesObjetives(self, new_names, new_name_var):
        self.presenter.setUpdateNamesObjetives(new_names, new_name_var)

# ------------------- SortObjetiveDialog               ------------------------
# -------------------                                  ------------------------

from wx.lib.itemspicker import ItemsPicker, EVT_IP_SELECTION_CHANGED


class SortObjetiveDialog(wx.Dialog):
    def __init__(self, parent, list_obj):
        wx.Dialog.__init__(self, parent)

        self.parent = parent
        self.list_obj = list_obj
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.ip = ItemsPicker(self, -1, self.list_obj,
                              _(C.SOD_ITC), _(C.SOD_IPN))
        self.ip._source.SetMinSize((-1, 150))
        sizer.Add(self.ip, 0, wx.ALL, 10)

        sizer_h = wx.BoxSizer(wx.HORIZONTAL)

        b_cancel = wx.Button(self, -1, _(C.SOD_BC))
        b_cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.b_ok = wx.Button(self, -1, _(C.SOD_BO))
        self.b_ok.Disable()
        self.b_ok.Bind(wx.EVT_BUTTON, self.OnOk)
        sizer_h.Add(b_cancel, 0, wx.ALL, 10)
        sizer_h.Add(self.b_ok, 0, wx.ALL, 10)

        sizer.Add(sizer_h, 0, wx.ALL, 10)

        self.SetSizer(sizer)

        self.ip.Bind(EVT_IP_SELECTION_CHANGED, self.OnSelectionChange)

        self.Fit()

    def OnSelectionChange(self, e):
        self.b_ok.Disable()
        if len(self.list_obj) == len(e.GetItems()):
            self.list_obj = e.GetItems()
            self.b_ok.Enable()

    def OnOk(self, event):
        self.parent.setUpdateSortV(self.list_obj)
        self.Close()

    def OnCancel(self, event):
        self.Close()


class RenameObjetivoDialog(wx.Dialog):
    def __init__(self, parent, list_obj, list_var):
        super(RenameObjetivoDialog, self).__init__(parent, size=(450, 500))
        self.parent = parent

        # ------ self customize ---------------------------------------
        tID = wx.NewId()

        sizer_title = wx.BoxSizer(wx.HORIZONTAL)
        text_title = wx.StaticText(self, label=_(C.ROD_RO))
        line_s = wx.StaticLine(self, style=LI_HORIZONTAL)
        sizer_title.Add(text_title, 0)
        sizer_title.Add(line_s, 1,
                        flag=wx.EXPAND | wx.RIGHT | wx.LEFT, border=10)

        sizer_title1 = wx.BoxSizer(wx.HORIZONTAL)
        text_title1 = wx.StaticText(self, label=_(C.ROD_RV))
        line_s1 = wx.StaticLine(self, style=LI_HORIZONTAL)
        sizer_title1.Add(text_title1, 0)
        sizer_title1.Add(line_s1, 1,
                         flag=wx.EXPAND | wx.RIGHT | wx.LEFT, border=10)

        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        b_cancel = wx.Button(self, -1, _(C.ROD_BC))
        self.b_ok = wx.Button(self, -1, _(C.ROD_BO))
        sizer_h.Add(b_cancel, 0, wx.ALL | wx.ALIGN_LEFT, 10)
        sizer_h.Add(self.b_ok, 0, wx.ALL | wx.ALIGN_LEFT, 10)

        self.list = TestListCtrl(self, tID, list_obj)
        self.list1 = TestListCtrl(self, -1, list_var)
        # boxsizer.Add(self.list, 1, wx.EXPAND)

        sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(boxsizer, 1, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(sizer_title, 0,
                  flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        sizer.Add(self.list, 2, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(sizer_title1, 0,
                  flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        sizer.Add(self.list1, 2, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(sizer_h, 0, flag=wx.BOTTOM | wx.LEFT | wx.RIGHT, border=10)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        b_cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.b_ok.Bind(wx.EVT_BUTTON, self.OnOk)
        self.Bind(wx.EVT_CHAR, self.OnKeyDown)

        self.Centre()
        self.ShowModal()

    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.Close()

    def OnOk(self, event):
        self.parent.updateNamesObjetives(self.list.getDatas(),
                                         self.list1.getDatas())
        self.Close()

    def OnCancel(self, event):
        self.Close()


import wx.dataview as dv
# ---------------------------------------------------------------------------


class TestListCtrl(dv.DataViewListCtrl):

    def __init__(self, parent, ID, list_obj, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        dv.DataViewListCtrl.__init__(self, parent, ID, pos, size, style)
        self.parent = parent
        self.count_objetive = len(list_obj)

        self.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.verificNames)

        self.AppendTextColumn(_(C.TLC_NC), width=250)
        self.AppendTextColumn(_(C.TLC_NN),
                              mode=dv.DATAVIEW_CELL_EDITABLE, width=250)

        for data in list_obj:
            self.AppendItem(data)

        self.parent.b_ok.Disable()

    def getDatas(self):
        to_ret = []
        for row in range(self.count_objetive):
            to_ret.append(self.GetTextValue(row, 1))
        return to_ret

    def verificNames(self, event):
        row = event.GetItem().GetID() - 1
        name = self.GetTextValue(row, 1)

        self.parent.b_ok.Enable()
        if not self.isValidName(name) or self.isRepeatName(name, row)\
                or self.isRepeatNameOthers() or not self.isModificSomeName():
            self.parent.b_ok.Disable()

    def isValidName(self, name):
        if len(name.strip(' ')) == 0:
            return False
        elif '/' in name:
            return False
        elif '.' in name:
            return False
        if len(name.strip(' ')) > 100:
            return False
        return True

    def isRepeatName(self, name, current_row):
        for row in range(self.count_objetive):
            if row != current_row:
                if name == self.GetTextValue(row, 1):
                    return True

        return False

    def isRepeatNameOthers(self):
        for row in range(self.count_objetive):
            for row_ in range(self.count_objetive):
                if row != row_:
                    if self.GetTextValue(row, 1) == self.GetTextValue(row_, 1):
                        return True

        return False

    def isModificSomeName(self):
        for row in range(self.count_objetive):
            name = self.GetTextValue(row, 1)
            if self.GetTextValue(row, 0) != name.strip(' '):
                return True
        return False
    # ---------------------------------------------

# ------------------- CustomizeFrontFigure             ------------------------
# -------------------                                  ------------------------

import wx.lib.colourselect as csel


class CustomizeFrontFigure(wx.Dialog):

    def __init__(self, parent, legent_figure, color_figure):
        super(CustomizeFrontFigure, self).__init__(parent, size=(300, 215))

        # ------ self customize ---------------------------------------
        self.parent = parent
        self.color_f = []
        self.color_lines = color_figure

        # ------ self components --------------------------------------
        self.panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self.panel, -1, _(C.CFF_CC))

        self.legent = wx.CheckBox(self.panel, -1, _(C.CFF_L))
        self.legent.SetValue(legent_figure)

        colour_sizer = wx.BoxSizer(wx.HORIZONTAL)
        colour_sizer.Add(wx.StaticText(self.panel, -1, _(C.CFF_LC)))
        self.c_lines = csel.ColourSelect(self.panel, -1,
                                                colour=color_figure,
                                                size=(60, 25))
        colour_sizer.Add(self.c_lines)

        line = wx.StaticLine(self.panel, -1, size=(20, -1))

        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_restart_d = wx.Button(self.panel, label=_(C.CFF_RC))
        btn_ok = wx.Button(self.panel, label=_(C.CFF_BO))
        btn_cancel = wx.Button(self.panel, label=_(C.CFF_BC))
        btn_ok.SetDefault()
        btnsizer.Add(btn_restart_d, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        btnsizer.Add(btn_cancel, 0, wx.ALL, 5)
        btnsizer.Add(btn_ok, 0, wx.ALL, 5)

        sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(line, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.legent, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        sizer.Add(colour_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.TOP, 35)

        self.panel.SetSizer(sizer)

        # ------ self inicailes executions ----------------------------
        self.Bind(csel.EVT_COLOURSELECT, self.OnSelectColour,
                  id=self.c_lines.GetId())
        btn_restart_d.Bind(wx.EVT_BUTTON, self.OnRestartDefaul)
        btn_ok.Bind(wx.EVT_BUTTON, self.OnButtonOk)
        btn_cancel.Bind(wx.EVT_BUTTON, self.OnButtonCancel)
        self.panel.Bind(wx.EVT_CHAR, self.OnKeyDown)

        self.Centre()
        self.ShowModal()
        # ----------------------------------------------------

    # ------ self controls --------------------------------------------
    def OnSelectColour(self, event):
        self.color_f = list(event.GetValue())

    def OnButtonOk(self, event):

        if not (self.color_f == []):
            from matplotlib.colors import rgb2hex
            self.color_lines = rgb2hex(self.normCol(self.color_f))
        self.parent.updateConfigPa(self.legent.GetValue(),
                                   self.color_lines)
        self.Close(True)

    def OnButtonCancel(self, event):
        self.Close(True)

    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.Close()

    def OnRestartDefaul(self, event):
        self.parent.restartDefaul()
        self.Close(True)

    def normCol(self, rgb_c):
        to_ret = []
        for c in rgb_c:
            to_ret.append(c / 255.0)
        return to_ret


class CustomizeObjetives(wx.Dialog):

    def __init__(self, parent):
        super(CustomizeObjetives, self).__init__(parent, size=(300, 400))

        # ------ self customize ---------------------------------------
        self.parent = parent
        self.no, self.vo = parent.getConfigObV()
        self.color_f = []
        self.InitUI()

        self.Centre()
        self.ShowModal()
        # ----------------------------------------------------

    def InitUI(self):

        # ------ self components --------------------------------------

        sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self, -1, _(C.CO_OD), (45, 15))
        sl = wx.StaticLine(self)

        sizerh = wx.BoxSizer(wx.HORIZONTAL)
        lb = wx.CheckListBox(self, -1, (80, 50), wx.DefaultSize, self.no)
        self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, lb)
        lb.SetSelection(0)
        self.lb = lb

        sizerv = wx.BoxSizer(wx.VERTICAL)
        btn_cancel = wx.Button(self, label=_(C.CO_BC))
        btn_ok = wx.Button(self, label=_(C.CO_BO))

        sizerv.Add(btn_ok)
        sizerv.Add(btn_cancel)

        sizerh.Add(self.lb, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizerh.Add(sizerv, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        sizer.Add(title, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(sl, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizerh, 5, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.SetSizer(sizer)

        for i in range(len(self.vo)):
            if self.vo[i] == '1':
                lb.Check(i)

        btn_ok.Bind(wx.EVT_BUTTON, self.OnButtonOk)
        btn_cancel.Bind(wx.EVT_BUTTON, self.OnButtonCancel)

    def EvtCheckListBox(self, event):
        index = event.GetSelection()
        self.vo[index] = '0'
        if self.lb.IsChecked(index):
            self.vo[index] = '1'
        self.lb.SetSelection(index)

        # ------ self components --------------------------------------
        # ------ self controls --------------------------------------------
    def OnButtonCancel(self, event):
        self.Close(True)

    def OnButtonOk(self, event):
        self.parent.setUpdateListObjetiveV(self.vo)
        self.Close(True)
        # ------ self inicailes executions ----------------------------

# ------------------- AUI Notebook par el footer       ------------------------
# -------------------                                  ------------------------
import wx.lib.agw.aui as aui


class FooterAUINotebook(aui.AuiNotebook):

    def __init__(self, parent, test, mode):
        '''
        Método de inicialización de la clase AUINotebook.
        :param parent: referencia al objeto padre de la clase.
        '''
        aui.AuiNotebook.__init__(self, parent=parent)

        # ------ self customize ---------------------------------------
        self.SetAGWWindowStyleFlag(aui.AUI_NB_TOP)

        # ------ self components --------------------------------------
        data_var = ParallelDataVar(self, test, mode)
        data_obj = ParallelDataObj(self, test, mode)
        filters = AddFilterObjetivesScroll(self, test, mode)

        # ------ self inicailes executions ----------------------------
        self.AddPage(data_var, _(C.FAN_V), True)
        self.AddPage(data_obj, _(C.FAN_O), False)
        self.AddPage(filters, _(C.FAN_F), False)

    # ------ self controls --------------------------------------------


# ------------------- Pagina vizualizador de variables ------------------------
# -------------------                                  ------------------------
from wx.lib.scrolledpanel import ScrolledPanel

from py.una.pol.tava.presenter.pparallel.pparallelcoordinatesal import\
    ParallelDataVarPresenter


class ParallelDataVar(ScrolledPanel):
    def __init__(self, parent, test, mode):
        ScrolledPanel.__init__(self, parent, -1)

        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        self.parent = parent
        self.mode = mode
        self.InitUI()
        self.presenter = ParallelDataVarPresenter(self, test)

    def InitUI(self):

        l_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dvlc = dv.DataViewListCtrl(self)
        l_sizer.Add(self.dvlc, 1, flag=wx.EXPAND)

        self.SetSizer(l_sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

        # ------ self inicailes executions ----------------------------
    # ------ self controls --------------------------------------------


# ------------------- Pagina para visualizar Objetivos ------------------------
# -------------------                                  ------------------------
from py.una.pol.tava.presenter.pparallel.pparallelcoordinatesal import\
    ParallelDataObjPresenter


class ParallelDataObj(ScrolledPanel):
    def __init__(self, parent, test, mode):
        ScrolledPanel.__init__(self, parent, -1)

        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        self.parent = parent
        self.mode = mode
        self.InitUI()
        self.presenter = ParallelDataObjPresenter(self, test)

    def InitUI(self):
        l_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dvlc = dv.DataViewListCtrl(self)
        l_sizer.Add(self.dvlc, 1, flag=wx.EXPAND)

        self.SetSizer(l_sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

        # ------ self inicailes executions ----------------------------
    # ------ self controls --------------------------------------------


# ------------------- Scrolled para los filtros        ------------------------
# -------------------                                  ------------------------
from py.una.pol.tava.presenter.pparallel.pparallelcoordinatesal import\
    AddFilterObjetivesScrollPresenter


class AddFilterObjetivesScroll(ScrolledPanel):
    def __init__(self, parent, test, mode):
        ScrolledPanel.__init__(self, parent, -1)

        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        self.parent = parent
        self.mode = mode
        self.presenter = AddFilterObjetivesScrollPresenter(self, test)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        # ------ self inicailes executions ----------------------------

    # ------ self controls --------------------------------------------
    def addItem(self, vmin, vmax, nobj, min_v_r, max_v_r):
        value = AddFilterObjetives(self, vmin, vmax, nobj, min_v_r, max_v_r)
        self.sizer.Add(value, 1, flag=wx.EXPAND)
        return value

    def addSiserHere(self):
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()


# ------------------- Clase contenedor de Filtros      ------------------------
# -------------------                                  ------------------------
from wx import LI_VERTICAL, LI_HORIZONTAL


class AddFilterObjetives(wx.Panel):
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

        line_ver1 = wx.StaticLine(self, style=LI_VERTICAL)
        sizer_main.Add(line_ver1, 0.1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
                       border=5)
        sizer_main.Add(sizer, 1, flag=wx.EXPAND)
        line_ver = wx.StaticLine(self, style=LI_VERTICAL)
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
