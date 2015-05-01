#  -*- coding: utf-8 -*-
'''
Created on 14/4/2015

@author: abrahan
'''
import wx
from wx import GetTranslation as _
import wx.lib.agw.labelbook as LB
import wx.lib.colourselect as csel

from py.una.pol.tava.view import vi18n as C
import py.una.pol.tava.view.vimages as I
from py.una.pol.tava.presenter.pparallel.pparallelconal \
    import ConfigurationParallelFigurePresenter


class ColorTv(wx.Panel):
    def __init__(self, parent, label, color, between_size=5, left_size=0):
        wx.Panel.__init__(self, parent=parent)

        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        c_label = wx.StaticText(self, -1, label+': ')
        self.ct = csel.ColourSelect(self, -1, '', color, size=(60, 25))
        sizer.Add(c_label, flag=wx.LEFT, border=left_size)
        sizer.Add(self.ct, flag=wx.LEFT, border=between_size)
        self.SetSizer(sizer)

        # ------ self inicailes executions ----------------------------
        # ----------------------------------------------------
    # ------ self controls --------------------------------------------

    def getValue(self):
        if isinstance(self.ct.GetColour(), wx.Colour):
            return self.ct.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)
        else:
            return self.ct.GetColour()


class BasedButtoon(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.btn_appli = wx.Button(self, label='Aplicar')
        self.btn_cancel = wx.Button(self, label=_(C.CFF_BC))
        self.btn_ok = wx.Button(self, label=_(C.CFF_BO))

        sizer_less = wx.BoxSizer(wx.HORIZONTAL)
        sizer_less.Add(self.btn_appli, 0, wx.ALIGN_LEFT | wx.LEFT, 0)

        sizer_right = wx.BoxSizer(wx.HORIZONTAL)
        sizer_right.Add(self.btn_cancel, 0, wx.LEFT, 10)
        sizer_right.Add(self.btn_ok, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5)

        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_buttons.Add(sizer_less, 1, wx.ALIGN_LEFT)
        sizer_buttons.Add(sizer_right, 1, wx.ALIGN_RIGHT | wx.LEFT, 0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer_buttons, 0, wx.ALL, 0)

        self.SetSizer(sizer)

        # ------ self inicailes executions ----------------------------


class BasedHeader(wx.Panel):
    def __init__(self, parent, title):
        wx.Panel.__init__(self, parent)

        title = wx.StaticText(self, -1, title)
        line = wx.StaticLine(self, -1, size=(20, -1))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.TOP, 3)
        sizer.Add(line, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)


# ------------------- CustomizeFrontFigure             ------------------------
# -------------------                                  ------------------------
class ConfigurationParallelFigure(wx.Dialog):

    def __init__(self, parent, pa):
        wx.Dialog.__init__(self, parent, size=(600, 500))

        bg_colors = pa.colors_backgrounds.split(',')

        self.lb = LB.LabelBook(self, -1, agwStyle=LB.INB_USE_PIN_BUTTON)
        self.lb.SetColour(LB.INB_TAB_AREA_BACKGROUND_COLOUR, bg_colors[2])

        self.tab_backGround = TabBackGroung(self, bg_colors)
        self.tab_figure_grid = TabFigureGrip(self, pa)
        self.tab_sort_objetive = TabSortObjetive(self, pa)
        self.tab_selected_obj = TabSelectedObjectives(self, pa)
        self.tab_rename = TabRename(self, pa)
        self.tab_rename_var = TabRenameVar(self, pa)

        # Paginas agregadas
        self.lb.AddPage(self.tab_backGround, "BackGrounds", False)
        self.lb.AddPage(self.tab_figure_grid, "Figura", False)
        self.lb.AddPage(self.tab_sort_objetive, "Sort Objective", False)
        self.lb.AddPage(self.tab_selected_obj, "Select Objective", False)
        self.lb.AddPage(self.tab_rename, "Rename Objective", False)
        self.lb.AddPage(self.tab_rename_var, "Rename Variables", True)

        line = wx.StaticLine(self)

        error_rename = wx.BoxSizer(wx.HORIZONTAL)
        self.ico_error = wx.StaticBitmap(self, -1, I.execute_png)
        self.text_error = wx.StaticText(self, -1, '')
        error_rename.Add(self.ico_error, 0, wx.TOP | wx.LEFT, 5)
        error_rename.Add(self.text_error, 0, wx.TOP, 5)

        self.buttons = BasedButtoon(self)
        sizer_foo = wx.BoxSizer(wx.HORIZONTAL)
        sizer_foo.Add(error_rename, 1, wx.EXPAND)
        sizer_foo.Add(self.buttons, 2.5, wx.EXPAND)

        self.presemter = ConfigurationParallelFigurePresenter(self, pa)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.lb, 12, wx.EXPAND)
        sizer.Add(line, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        sizer.Add(sizer_foo, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # ------ self inicailes executions ----------------------------
        self.buttons.btn_appli.Bind(wx.EVT_BUTTON, self.OnButtonApply)
        self.buttons.btn_cancel.Bind(wx.EVT_BUTTON, self.OnButtonCancel)
        self.buttons.btn_ok.Bind(wx.EVT_BUTTON, self.OnButtonOk)
        self.Bind(wx.EVT_CHAR, self.OnKeyDown)

        self.CenterOnScreen()
        self.ShowModal()
    # ------ self controls --------------------------------------------

    def enableButtonP(self):
        self.buttons.btn_appli.Enable()
        self.buttons.btn_ok.Enable()
        self.setUpdateEnable(self.tab_rename.state_obj,
                             self.tab_rename_var.state_var)

    def disableButtonP(self):
        self.buttons.btn_appli.Disable()
        self.buttons.btn_ok.Disable()
        self.setUpdateEnable(self.tab_rename.state_obj,
                             self.tab_rename_var.state_var)

    def OnButtonApply(self, event):
        self.presemter.setApplyConfig()

    def OnButtonCancel(self, event):
        self.presemter.setCancel()

    def OnButtonOk(self, event):
        self.presemter.setSave()

    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.presemter.setCancel()

    def setBackGroundLB(self, color):
        self.lb.SetColour(LB.INB_TAB_AREA_BACKGROUND_COLOUR, color)
        self.lb.Refresh()

    def setUpdateEnable(self, re_obj, re_var):
        if re_obj and re_var:
            self.ico_error.SetBitmap(I.execute_png)
            self.text_error.SetLabel('')
            return None

        self.ico_error.SetBitmap(I.errornewproject_png)
        if (not re_obj) and re_var:
            self.text_error.SetLabel('In Rename Objectives')
        elif re_obj and (not re_var):
            self.text_error.SetLabel('In Rename Variables')
        else:
            self.text_error.SetLabel('In Rename Objectives \n and Variables')

        return None


# ------------------- CustomizeFrontFigure             ------------------------
# -------------------                                  ------------------------
class TabBackGroung(wx.Panel):

    def __init__(self, parent, bg_colors):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
        self.parent = parent
        self.color_f = []

        # ------ self components --------------------------------------
        self.header = BasedHeader(self, 'Colores de Fondos')

        body_sizer = wx.BoxSizer(wx.VERTICAL)
        self.ct1 = ColorTv(self, 'Tree BackGround', bg_colors[0], 0, 40)
        self.cf1 = ColorTv(self, 'Figure BackGround', bg_colors[1], 0, 27)
        self.ctf1 = ColorTv(self, 'Toll Figure BackGround', bg_colors[2], 0, 0)

        body_sizer.Add(self.ct1)
        body_sizer.Add(self.cf1)
        body_sizer.Add(self.ctf1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.header, 1, wx.EXPAND)
        sizer.Add(body_sizer, 10, wx.ALIGN_LEFT | wx.ALL, 5)

        self.SetSizer(sizer)

        # ------ self inicailes executions ----------------------------
        # ----------------------------------------------------
    # ------ self controls --------------------------------------------

    def getValuesTab(self):
        c1 = self.ct1.getValue()
        c2 = self.cf1.getValue()
        c3 = self.ctf1.getValue()
        return c1 + ',' + c2 + ',' + c3


# ------------------- CustomizeFrontFigure             ------------------------
# -------------------                                  ------------------------
class TabFigureGrip(wx.Panel):

    def __init__(self, parent, pa):
        wx.Panel.__init__(self, parent)
        # ------ self customize ---------------------------------------

        # ------ self components --------------------------------------
        fg = pa.figure_grid
        self.grid_aux = fg.grid

        header = BasedHeader(self, _(C.CFF_CC))
        self.grid_on = wx.RadioButton(self, -1, "con trama ",
                                      style=wx.RB_GROUP)
        self.grid_off = wx.RadioButton(self, -1, "sin trama ")

        g_fg_option = wx.BoxSizer(wx.HORIZONTAL)
        g_fg_option.Add(self.grid_on)
        g_fg_option.Add(self.grid_off)

        # orientación de trama
        o_list = ['vertical y orizontal', 'solo vertical', 'solo horizontal']
        o_title = wx.StaticText(self, -1, "Orientacion de Trama:")
        self.o_cb = wx.ComboBox(self, 500, o_list[fg.orientation],
                                choices=o_list, style=wx.CB_READONLY)
        orientation_sizer = wx.BoxSizer(wx.HORIZONTAL)
        orientation_sizer.Add(o_title, 1, wx.LEFT, 23)
        orientation_sizer.Add(self.o_cb, 1, wx.LEFT, 2)

        # ancho de línea
        lw_title = wx.StaticText(self, -1, "Ancho de Línea de Trama:")
        self.lw_sc = wx.SpinCtrl(self, -1, "", min=1, max=5,
                                 initial=fg.red_width)
        linewidth_sizer = wx.BoxSizer(wx.HORIZONTAL)
        linewidth_sizer.Add(lw_title, 1, wx.LEFT, 1)
        linewidth_sizer.Add(self.lw_sc, 1, wx.LEFT, 2)

        # estilo de línea
        sl_list = ['. . . . . .', '- - - - - -', '-. -. -. -.', '-----------']
        sl_title = wx.StaticText(self, -1, "Estílo de Línea de Trama:")
        self.sl_cb = wx.ComboBox(self, 500, sl_list[fg.red_style],
                                 choices=sl_list, style=wx.CB_READONLY)
        style_sizer = wx.BoxSizer(wx.HORIZONTAL)
        style_sizer.Add(sl_title, 1, wx.LEFT, 5)
        style_sizer.Add(self.sl_cb, 1, wx.LEFT, 2)

        # color de línea
        self.color_red = ColorTv(self, 'Color de Línea de Trama',
                                 fg.red_color, 0, 5)

        g_fg_sizer = wx.BoxSizer(wx.VERTICAL)
        g_fg_sizer.Add(g_fg_option, 0, wx.TOP, 5)
        g_fg_sizer.Add(orientation_sizer, 0, wx.TOP, 5)
        g_fg_sizer.Add(linewidth_sizer, 0, wx.TOP, 5)
        g_fg_sizer.Add(style_sizer, 0, wx.TOP, 5)
        g_fg_sizer.Add(self.color_red, 0, wx.TOP, 5)

        # estatic box
        g_sbox_title = wx.StaticBox(self, -1,
                                    "Personalización de la Trama de la Figura")
        box1 = wx.StaticBoxSizer(g_sbox_title, wx.VERTICAL)
        box1.Add(g_fg_sizer, 1, wx. EXPAND | wx.LEFT | wx.ALL, 5)

        # legenda
        self.check_legent = wx.CheckBox(self, -1, _(C.CFF_L))
        self.check_legent.SetValue(pa.legent)
        # color de lineas
        self.color_lines = ColorTv(self, _(C.CFF_LC), pa.color_lines)

        pa_sizer = wx.BoxSizer(wx.VERTICAL)
        pa_sizer.Add(self.check_legent, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        pa_sizer.Add(self.color_lines, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        body_sizer = wx.BoxSizer(wx.VERTICAL)
        body_sizer.Add(pa_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        body_sizer.Add(box1, 0, wx.EXPAND | wx.ALL, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(header, 1, wx.EXPAND)
        sizer.Add(body_sizer, 10, wx.EXPAND)

        self.grid_on.Bind(wx.EVT_RADIOBUTTON, self.On_Grid)
        self.grid_off.Bind(wx.EVT_RADIOBUTTON, self.Off_Grid)

        self.SetSizer(sizer)

        self.setEnableComponets(fg.grid)
        # ------ self inicailes executions ----------------------------

    # ------ self controls --------------------------------------------

    def getValuesTab(self):
        grid = self.grid_aux
        orientation = self.o_cb.GetSelection()
        lines_color = self.color_red.getValue()
        lines_width = self.lw_sc.GetValue()
        lines_style = self.sl_cb.GetSelection()
        color_lines = self.color_lines.getValue()
        legent = self.check_legent.GetValue()

        return [grid, orientation, lines_color, lines_width, lines_style,
                color_lines, legent]

    def setEnableComponets(self, grid_on):
        if grid_on:
            self.grid_on.SetValue(True)
            self.o_cb.Enable()
            self.lw_sc.Enable()
            self.sl_cb.Enable()
            self.color_red.ct.Enable()

        else:
            self.grid_off.SetValue(True)
            self.o_cb.Disable()
            self.lw_sc.Disable()
            self.sl_cb.Disable()
            self.color_red.ct.Disable()

            self.grid_off.SetValue(True)

    def On_Grid(self, event):
        self.grid_aux = True
        self.setEnableComponets(self.grid_aux)

    def Off_Grid(self, event):
        self.grid_aux = False
        self.setEnableComponets(self.grid_aux)


from wx.lib.itemspicker import ItemsPicker, EVT_IP_SELECTION_CHANGED


class TabSortObjetive(wx.Panel):
    def __init__(self, parent, pa):
        wx.Panel.__init__(self, parent)
        # ------ self customize ---------------------------------------
        self.parent = parent
        # ------ self components --------------------------------------
        self.header = BasedHeader(self, 'Ordenamiento de Objetivos')
        self.Init(pa)

    def Init(self, pa):
        self.new_sort = []
        self.list_obj = pa.order_name_obj.split(',')
        self.names = pa.name_objetive.split(',')
        self.list_obj_index = pa.order_objective
        self.ip = ItemsPicker(self, -1, pa.order_name_obj.split(','),
                              _(C.SOD_ITC), _(C.SOD_IPN))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.header, 1, wx.EXPAND)
        self.sizer.Add(self.ip, 10, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(self.sizer)
        self.ip.Bind(EVT_IP_SELECTION_CHANGED, self.OnSelectionChange)

    def updateDate(self, pa):
        self.Init(pa)

    def OnSelectionChange(self, e):
        if len(self.list_obj) == len(e.GetItems()):
            self.new_sort = e.GetItems()

    def getValuesTab(self):
        if len(self.list_obj) == len(self.new_sort):
            if self.list_obj != self.new_sort:
                list_index = [str(self.names.index(name))
                              for name in self.new_sort]
                str_index = ','.join(list_index)
                return [','.join(self.new_sort), str_index]

        return [','.join(self.list_obj), self.list_obj_index]


class TabSelectedObjectives(wx.Panel):
    def __init__(self, parent, pa):
        wx.Panel.__init__(self, parent)
        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        self.header = BasedHeader(self, _(C.CO_OD))

        self.Init(pa)

    def Init(self, pa):
        self.list_enable = pa.enable_objectives.split(',')
        self.lb = wx.CheckListBox(self, -1, (80, 50), wx.DefaultSize,
                                  pa.name_objetive.split(','))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.header, 0, wx.EXPAND)
        sizer.Add(self.lb, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 25)
        self.SetSizer(sizer)

        # ------ self inicailes executions ----------------------------
        self.lb.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox)
        self.initCheckingValues()

        # ------ self controls --------------------------------------------
    def EvtCheckListBox(self, event):
        index = event.GetSelection()
        if self.lb.IsChecked(index):
            self.list_enable[index] = '1'
        else:
            self.list_enable[index] = '0'
        self.lb.SetSelection(index)

    def initCheckingValues(self):
        for i in range(len(self.list_enable)):
            if self.list_enable[i] == '1':
                self.lb.Check(i)

    def getValuesTab(self):

        return [','.join(self.list_enable),
                ','.join([str(i) for i in self.lb.GetChecked()]),
                ','.join(self.lb.GetCheckedStrings())]


import wx.dataview as dv


class TabRename(wx.Panel):
    def __init__(self, parent, pa):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.state_obj = True

        # ------ self customize ---------------------------------------

        header = BasedHeader(self, _(C.ROD_RO))

        # grilla de nombres de Objetivos
        self.dvlc = dv.DataViewListCtrl(self)
        self.dvlc.AppendTextColumn('Fila', width=35, align=wx.ALIGN_CENTER)
        self.dvlc.AppendTextColumn(_(C.TLC_NC), width=200)
        self.dvlc.AppendTextColumn(_(C.TLC_NN),
                                   mode=dv.DATAVIEW_CELL_EDITABLE, width=200)
        index = 0
        list_obj = pa.order_name_obj.split(',')
        for data in list_obj:
            index += 1
            self.dvlc.AppendItem([str(index), data, ''])
        self.count_objetive = index

        # estado se nombres de Objetivos
        obj_tmp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ico_tmp = wx.StaticBitmap(self, -1, I.ok_png)
        self.state_tmp = wx.StaticText(self, -1, ' Estado: Correcto')
        obj_tmp_sizer.Add(self.ico_tmp, 0)
        obj_tmp_sizer.Add(self.state_tmp, 0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(header, 0, flag=wx.EXPAND)
        sizer.Add(obj_tmp_sizer, 0, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(self.dvlc, 4, wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)
        self.SetSizer(sizer)

        self.dvlc.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.verificNamesOb)

    def updateRename(self, pa):
        self.dvlc.DeleteAllItems()

        index = 0
        list_obj = pa.order_name_obj.split(',')
        for data in list_obj:
            index += 1
            self.dvlc.AppendItem([str(index), data, ''])
        self.count_objetive = index

    def verificNamesOb(self, event):
        if self.isInvalidName(self.dvlc):
            self.state_obj = False
            self.ico_tmp.SetBitmap(I.errornewproject_png)
            self.state_tmp.SetLabel(' Estado:  Error, ' +
                                    self.getNamesWithError())
            self.parent.disableButtonP()
        else:
            self.state_obj = True
            self.ico_tmp.SetBitmap(I.ok_png)
            self.state_tmp.SetLabel(' Estado: Correcto')
            self.parent.enableButtonP()

    def isInvalidName(self, dvlc):

        for row in range(self.count_objetive):
            name = dvlc.GetTextValue(row, 2)

            if '/' in name:
                return True
            elif '.' in name:
                return True
            elif ',' in name:
                return True
            if len(name.strip(' ')) > 100:
                return True

            for row_ in range(self.count_objetive):
                if row != row_:
                    if name == dvlc.GetTextValue(row_, 2) and name != '':
                        return True

            for r in range(self.count_objetive):
                if row != r:
                    if dvlc.GetTextValue(r, 1) == dvlc.GetTextValue(row, 2):
                        if dvlc.GetTextValue(r, 2) == '':
                            return True

        return False

    def getNamesWithError(self):
        for row in range(self.count_objetive):
            dvlc = self.dvlc
            name = self.dvlc.GetTextValue(row, 2)

            if '/' in name:
                return 'Caracter invalido: "/" en Fila: ' + str(row + 1)
            elif '.' in name:
                return 'Caracter invalido: "." en Fila: ' + str(row + 1)
            elif ',' in name:
                return 'Caracter invalido: "," en Fila: ' + str(row + 1)
            if len(name.strip(' ')) > 100:
                return 'Mayor a longitud maxima: "/" en Fila: ' + str(row + 1)

            for row_ in range(self.count_objetive):
                if row != row_:
                    if name == self.dvlc.GetTextValue(row_, 2) and name != '':
                        return 'Nombre Repetido: en Fila: ' +\
                            str(row + 1) + ' y ' + str(row_+1)

            for r in range(self.count_objetive):
                if row != r:
                    if dvlc.GetTextValue(r, 1) == dvlc.GetTextValue(row, 2):
                        if dvlc.GetTextValue(r, 2) == '':
                            return 'Nombre Repetido: en Fila: ' +\
                                str(row + 1) + ' y ' + str(r+1)
        return 'Error!!!'

    def getValuesTab(self):
        to_ret = []
        for row in range(self.count_objetive):
            to_ret.append(self.dvlc.GetTextValue(row, 2))
        return to_ret


class TabRenameVar(wx.Panel):
    def __init__(self, parent, pa):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.state_var = True

        # ------ self customize ---------------------------------------

        header = BasedHeader(self, _(C.ROD_RV))

        # grilla de nombres de Variables
        self.dvlc = dv.DataViewListCtrl(self)
        self.dvlc.AppendTextColumn('Row', width=35)
        self.dvlc.AppendTextColumn(_(C.TLC_NC), width=200)
        self.dvlc.AppendTextColumn(_(C.TLC_NN),
                                   mode=dv.DATAVIEW_CELL_EDITABLE, width=200)
        list_obj = pa.name_variable.split(',')
        index = 0
        for data in list_obj:
            index += 1
            self.dvlc.AppendItem([str(index), data, ''])
        self.count_objetive = index

        # estado se nombres de Objetivos
        obj_tmp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ico_tmp = wx.StaticBitmap(self, -1, I.ok_png)
        self.state_tmp = wx.StaticText(self, -1, ' :Estado')
        obj_tmp_sizer.Add(self.ico_tmp, 0)
        obj_tmp_sizer.Add(self.state_tmp, 0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(header, 0, flag=wx.EXPAND)
        sizer.Add(obj_tmp_sizer, 0, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(self.dvlc, 4, wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)
        self.SetSizer(sizer)

        self.dvlc.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.verificNamesOb)

    def updateRenameVar(self, pa):
        self.dvlc.DeleteAllItems()

        index = 0
        list_obj = pa.order_name_obj.split(',')
        for data in list_obj:
            index += 1
            self.dvlc.AppendItem([str(index), data, ''])
        self.count_objetive = index

    def verificNamesOb(self, event):
        if self.isInvalidName(self.dvlc):
            self.state_var = False
            self.ico_tmp.SetBitmap(I.errornewproject_png)
            self.state_tmp.SetLabel(' Estado:  Error, ' +
                                    self.getNamesWithError())
            self.parent.disableButtonP()
        else:
            self.state_var = True
            self.ico_tmp.SetBitmap(I.ok_png)
            self.state_tmp.SetLabel(' Estado: Correcto')
            self.parent.enableButtonP()

    def isInvalidName(self, dvlc):

        for row in range(self.count_objetive):
            name = dvlc.GetTextValue(row, 2)

            if '/' in name:
                return True
            elif '.' in name:
                return True
            elif ',' in name:
                return True
            if len(name.strip(' ')) > 100:
                return True

            for row_ in range(self.count_objetive):
                if row != row_:
                    if name == dvlc.GetTextValue(row_, 2) and name != '':
                        return True

            for r in range(self.count_objetive):
                if row != r:
                    if dvlc.GetTextValue(r, 1) == dvlc.GetTextValue(row, 2):
                        if dvlc.GetTextValue(r, 2) == '':
                            return True

        return False

    def getNamesWithError(self):
        for row in range(self.count_objetive):
            dvlc = self.dvlc
            name = self.dvlc.GetTextValue(row, 2)

            if '/' in name:
                return 'Caracter invalido: "/" en Fila: ' + str(row + 1)
            elif '.' in name:
                return 'Caracter invalido: "." en Fila: ' + str(row + 1)
            elif ',' in name:
                return 'Caracter invalido: "," en Fila: ' + str(row + 1)
            if len(name.strip(' ')) > 100:
                return 'Mayor a longitud maxima: "/" en Fila: ' + str(row + 1)

            for row_ in range(self.count_objetive):
                if row != row_:
                    if name == self.dvlc.GetTextValue(row_, 2) and name != '':
                        return 'Nombre Repetido: en Fila: ' +\
                            str(row + 1) + ' y ' + str(row_+1)

            for r in range(self.count_objetive):
                if row != r:
                    if dvlc.GetTextValue(r, 1) == dvlc.GetTextValue(row, 2):
                        if dvlc.GetTextValue(r, 2) == '':
                            return 'Nombre Repetido: en Fila: ' +\
                                str(r+1) + ' y ' + str(row+1)
        return 'Error!!!'

    def getValuesTab(self):
        to_ret = []
        for row in range(self.count_objetive):
            to_ret.append(self.dvlc.GetTextValue(row, 2))
        return to_ret
