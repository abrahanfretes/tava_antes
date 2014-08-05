# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''

import wx
from wx import GetTranslation as _
from py.una.pol.tava.presenter.pproject import NewProjectDialogPresenter
from py.una.pol.tava.presenter.pproject import RenameProjectDialogPresenter
import py.una.pol.tava.view.vi18n as C
#from sympy.printing.preview import preview


class NewProjectDialog(wx.Dialog):

    def __init__(self, parent):
        super(NewProjectDialog, self).__init__(parent,
            title=_(C.NPD_NEP), size=(621, 220))

        self.presenter = NewProjectDialogPresenter(self)

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        container_panel = wx.Panel(self)
        container_sizer = wx.GridBagSizer(5, 5)

        new_project_text = wx.StaticText(container_panel,
                                          label=_(C.NPD_CNP))
        new_project_text_font = new_project_text.GetFont()
        new_project_text_font.SetWeight(wx.BOLD)
        new_project_text.SetFont(new_project_text_font)
        container_sizer.Add(new_project_text, pos=(0, 0), flag=wx.TOP |
                            wx.LEFT, border=15)

        execute_bmp = wx.StaticBitmap(container_panel,
                               bitmap=wx.Bitmap('view/icons/exec.png'))
        container_sizer.Add(execute_bmp, pos=(0, 4), flag=wx.RIGHT |
                            wx.ALIGN_RIGHT, border=5)

        self.description_text = wx.StaticText(container_panel,
                                             label=_(C.NPD_ENP))
        container_sizer.Add(self.description_text, pos=(1, 0), flag=wx.TOP |
                            wx.LEFT | wx.BOTTOM, border=15)

        line = wx.StaticLine(container_panel)
        container_sizer.Add(line, pos=(2, 0), span=(1, 5),
            flag=wx.EXPAND | wx.BOTTOM, border=10)

        name_project_text = wx.StaticText(container_panel,
                                          label=_(C.NPD_NAP))
        container_sizer.Add(name_project_text, pos=(3, 0), flag=wx.LEFT,
                            border=10)

        self.name_project_textctrl = wx.TextCtrl(container_panel)
        self.name_project_textctrl.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.name_project_textctrl.SetFocus()
        container_sizer.Add(self.name_project_textctrl, pos=(3, 1),
                            span=(1, 3), flag=wx.TOP | wx.EXPAND)

        help_button = wx.Button(container_panel, label=_(C.NPD_HELP))
        container_sizer.Add(help_button, pos=(5, 0), flag=wx.LEFT, border=10)

        self.ok_button = wx.Button(container_panel, label=_(C.NPD_OK))
        self.ok_button.Bind(wx.EVT_BUTTON, self.OnNew)
        container_sizer.Add(self.ok_button, pos=(5, 3))

        cancel_button = wx.Button(container_panel, label=_(C.NPD_CAN))
        cancel_button.Bind(wx.EVT_BUTTON, self.OnCancel)
        container_sizer.Add(cancel_button, pos=(5, 4), span=(1, 1),
            flag=wx.BOTTOM | wx.RIGHT, border=5)

        container_sizer.AddGrowableCol(2)
        container_panel.SetSizer(container_sizer)

        self.ConfigDefaulLabel()

    def OnKeyUp(self, e):

        if self.presenter.IsNameValido(self.name_project_textctrl.Value):
            self.ok_button.Enable(True)
            self.ConfigEnableLabel()

            if wx.WXK_RETURN == e.GetKeyCode():
                self.OnCreate(self.name_project_textctrl.Value)
        else:
            if len(self.name_project_textctrl.Value) == 0:
                self.ConfigDefaulLabel()
            else:
                self.ConfigDisableLabel()

    def ConfigDefaulLabel(self):
        self.description_text.SetLabel(_(C.NPD_ENP))
        self.ok_button.Disable()
        self.description_text.SetForegroundColour((77, 77, 77))
        self.name_project_textctrl.SetBackgroundColour((250, 250, 250))

    def ConfigEnableLabel(self):
        self.description_text.SetLabel(_(C.NPD_ENP))
        self.description_text.SetForegroundColour((0, 0, 0))
        self.name_project_textctrl.SetBackgroundColour((255, 255, 255))

    def ConfigDisableLabel(self):
        self.description_text.SetLabel(_(C.NPD_PAE))
        self.ok_button.Disable()
        self.description_text.SetForegroundColour(wx.RED)
        self.name_project_textctrl.SetBackgroundColour((237, 93, 93))

    def OnNew(self, e):
        self.OnCreate(self.name_project_textctrl.Value)

    def OnCreate(self, nameProject):
        self.presenter.OnNew(nameProject)
        self.OnClose()

    def OnCancel(self, e):
        self.Close(True)

    def OnClose(self):
        self.Close(True)


class RenameProjectDialog(wx.Dialog):

    def __init__(self, parent, message):
        super(RenameProjectDialog, self).__init__(parent,
            title='Renombrar Recurso', size=(550, 180))

        project_item = message.data
        self.project = project_item[0]
        self.item = project_item[1]
        self.previous_name = self.project.name

        self.presenter_re = RenameProjectDialogPresenter(self)

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):

        cpanel = wx.Panel(self)
        csizer = wx.GridBagSizer(4, 5)

        level_name = wx.StaticText(cpanel, label='nuevo nombre')
        csizer.Add(level_name, pos=(0, 0), flag=wx.LEFT | wx.TOP, border=20)

        self.new_name = wx.TextCtrl(cpanel, value=self.previous_name)
        csizer.Add(self.new_name, pos=(0, 1), span=(1, 4), flag=wx.BOTTOM |
                   wx.TOP | wx.RIGHT | wx.EXPAND, border=16)

        self.ok_button = wx.Button(cpanel, label='OK')

        csizer.Add(self.ok_button, pos=(3, 3),
                   flag=wx.BOTTOM | wx.TOP | wx.RIGHT, border=16)

        cancel_button = wx.Button(cpanel, label='Cancel')

        csizer.Add(cancel_button, pos=(3, 4),
                   flag=wx.BOTTOM | wx.TOP | wx.RIGHT, border=16)

        csizer.AddGrowableCol(2)
        cpanel.SetSizer(csizer)

        self.new_name.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.ok_button.Bind(wx.EVT_BUTTON, self.OnOkRenameEvent)
        cancel_button.Bind(wx.EVT_BUTTON, self.OnCancel)

    def OnKeyUp(self, e):

        if self.presenter_re.IsNameValido(self.new_name.Value):
            self.ok_button.Enable(True)
            self.ConfigEnableLabel()

            if wx.WXK_RETURN == e.GetKeyCode():
                self.OnOkRename(self.new_name.Value)
        else:
            if self.previous_name == self.new_name.Value:
                self.ConfigEnableLabel()
            elif len(self.new_name.Value) == 0:
                self.ConfigDefaulLabel()
            else:
                self.ConfigDisableLabel()

    def ConfigDefaulLabel(self):
        self.ok_button.Disable()
        self.new_name.SetBackgroundColour((250, 250, 250))

    def ConfigEnableLabel(self):
        self.new_name.SetBackgroundColour((255, 255, 255))

    def ConfigDisableLabel(self):
        self.ok_button.Disable()
        self.new_name.SetBackgroundColour((237, 93, 93))

    def OnOkRenameEvent(self, event):
        self.OnOkRename(self.new_name.Value)

    def OnOkRename(self, new_name):
        if self.previous_name != self.new_name.Value:
            self.presenter_re.OnUpDateName(new_name, self.project, self.item)
        self.Close(True)

    def OnCancel(self, e):
        self.Close(True)

    def OnClose(self):
        self.Close(True)
