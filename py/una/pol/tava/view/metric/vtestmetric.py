# -*- coding: utf-8 -*-
'''
Created on 2/6/2015

@author: abrahan
'''
import wx
from wx import GetTranslation as _

from py.una.pol.tava.presenter.metric.ptestmetric import\
    TestMetricDialogPresenter
from py.una.pol.tava.view import vi18n as C

padding = 10


class BasedName(wx.Panel):
    def __init__(self, parent, static_label='', names=[], hide_names=[]):
        wx.Panel.__init__(self, parent)
        self.name_correct = False
        self.existin_names = names
        self.existin_hide_names = hide_names

        self.label = wx.StaticText(self, label=static_label+': ')
        self.input = wx.TextCtrl(self)
        self.notice = wx.StaticText(self)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.label, 1, wx.ALL, 0)
        sizer.Add(self.input, 5, wx.ALIGN_LEFT | wx.ALL, 0)
        sizer.Add(self.notice, 1, wx.ALL, 0)
        self.SetSizer(sizer)

        # ------ self inicailes executions ----------------------------

    def validateName(self):
        name = self.input.GetValue()
        if len(name) > 0:
            if len(name.strip(' ')) == 0:
                self.notice.SetLabel('Error')
                self.name_correct = False
                return self.name_correct
            if '/' in name:
                self.notice.SetLabel('Error')
                self.name_correct = False
                return self.name_correct
            if name[0] == '.':
                self.notice.SetLabel('Error')
                self.name_correct = False
                return self.name_correct
            if len(name.strip(' ')) > 100:
                self.notice.SetLabel('Error')
                self.name_correct = False
                return self.name_correct
            if name in self.existin_names:
                self.notice.SetLabel('Error')
                self.name_correct = False
                return self.name_correct
            if name in self.existin_hide_names:
                self.notice.SetLabel('Error')
                self.name_correct = False
                return self.name_correct

            self.notice.SetLabel('')
            self.name_correct = True
        else:
            self.notice.SetLabel('')
            self.name_correct = False

        return self.name_correct


class BasedButtoon(wx.Panel):
    def __init__(self, parent, l_accept=None, l_cancel=None):
        wx.Panel.__init__(self, parent)

        if l_accept is None:
            l_accept = _(C.CFF_BO)
        if l_cancel is None:
            l_cancel = _(C.CFF_BC)

        self.cancel = wx.Button(self, label=l_cancel)
        self.accept = wx.Button(self, label=l_accept)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.cancel, 0, wx.RIGHT, 25)
        sizer.Add(self.accept, 0)
        self.SetSizer(sizer)


class TestMetricDialog(wx.Dialog):
    '''
    Clase Dialog que define la ventana de creación de un nuevo proyecto.
    '''

    def __init__(self, parent, project):
        wx.Dialog.__init__(self, parent, -1, "New Test Metric",
                           size=(600, 630))

        # ------ Definiciones iniciales ---------------------------------------
        self.presenter = TestMetricDialogPresenter(self, project)
        self.InitUI()

        self.Centre()
        self.ShowModal()
        # ----------------------------------------------------

    def InitUI(self):

        header_title = wx.StaticText(self, -1, "Test Metric ")
        header_title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        header_line = wx.StaticLine(self, -1)

        siser_header = wx.BoxSizer(wx.VERTICAL)
        siser_header.Add(header_title, 0, wx.ALIGN_LEFT | wx.ALL, padding)
        siser_header.Add(header_line, 0, wx.EXPAND | wx.ALL, padding)

        __lm = self.presenter.getNamesMetric()
        self.name = BasedName(self, "Test Name", __lm)

        label_project = wx.StaticText(self, label="Project: ")
        input_project = wx.StaticText(self, label=self.presenter.name)
        sizer_input2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_input2.Add(label_project, 0, wx.LEFT | wx.RIGHT, padding)
        sizer_input2.Add(input_project, 0)

        # =====================================================================
        # self.ip = ItemsPicker(self, -1, __l, 'Files', 'Files Selected',
        #                       ipStyle=IP_SORT_CHOICES |
        #                       IP_SORT_SELECTED | IP_REMOVE_FROM_CHOICES)
        # =====================================================================

        __l = self.presenter.getNamesResults()
        label_combo = wx.StaticText(self, -1, "Orientacion de Trama:")
        self.combo_result = wx.ComboBox(self, 500, choices=__l,
                                        style=wx.CB_READONLY)

        combo_sizer = wx.BoxSizer(wx.HORIZONTAL)
        combo_sizer.Add(label_combo, 0)
        combo_sizer.Add(self.combo_result, 0)

        self.bfooter = BasedButtoon(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(siser_header, 0, wx.EXPAND, wx.ALL, padding)
        sizer.Add(self.name, 0, wx.EXPAND, wx.ALL, padding)
        sizer.Add(sizer_input2, 0, wx.EXPAND)
        # sizer.Add(self.ip, 1, wx.EXPAND)
        sizer.Add(combo_sizer, 0, wx.EXPAND)
        sizer.Add(self.bfooter, 0, wx.ALIGN_RIGHT | wx.ALL, 20)

        self.SetSizer(sizer)

        # init setting
        self.name.input.SetFocus()
        self.bfooter.accept.Disable()
        self.bfooter.cancel.Bind(wx.EVT_BUTTON, self.OnButtonCancel)
        self.bfooter.accept.Bind(wx.EVT_BUTTON, self.OnButtonOk)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyDown)
        self.combo_result.Bind(wx.EVT_COMBOBOX, self.OnChangeCombo)
        # self.ip.Bind(EVT_IP_SELECTION_CHANGED, self.OnChangeIp)

    def OnKeyDown(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            self.Close()
        elif key_code == wx.WXK_RETURN:
            if self.enableAcceptOption():
                self.presenter.addTest(self.name.input,
                                       self.combo_result.GetSelection())
        else:
            self.enableAcceptOption()

    def OnButtonCancel(self, event):
        self.Close()

    def OnButtonOk(self, event):
        self.presenter.addTest(self.name.input.GetValue(),
                               self.combo_result.GetSelection())

    def enableAcceptOption(self):
        if not self.name.validateName():
            self.bfooter.accept.Disable()
            return False
        elif wx.NOT_FOUND is self.combo_result.GetSelection():
            self.bfooter.accept.Disable()
            return False
        else:
            self.bfooter.accept.Enable()
            return True

    def OnChangeCombo(self, event):
        self.enableAcceptOption()
