# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''

import wx
from wx import GetTranslation as _
from py.una.pol.tava.presenter.pproject import NewProjectDialogPresenter
import py.una.pol.tava.view.vi18n as C


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
        self.ok_button.Disable()
        container_sizer.Add(self.ok_button, pos=(5, 3))

        cancel_button = wx.Button(container_panel, label=_(C.NPD_CAN))
        cancel_button.Bind(wx.EVT_BUTTON, self.OnCancel)
        container_sizer.Add(cancel_button, pos=(5, 4), span=(1, 1),
            flag=wx.BOTTOM | wx.RIGHT, border=5)

        container_sizer.AddGrowableCol(2)
        container_panel.SetSizer(container_sizer)

    def OnNew(self, e):
        self.OnCreate(self.name_project_textctrl.Value)

    def OnKeyUp(self, e):

        if self.presenter.IsNameValido(self.name_project_textctrl.Value):
            self.ok_button.Enable(True)
            self.ConfigEnableLabel()

            if wx.WXK_RETURN == e.GetKeyCode():
                self.OnCreate(self.name_project_textctrl.Value)
        else:
            self.ok_button.Disable()
            self.ConfigDisableLabel()

    def ConfigEnableLabel(self):
        self.description_text.SetLabel(_(C.NPD_ENP))
        self.description_text.SetForegroundColour((0, 0, 0))
        self.name_project_textctrl.SetBackgroundColour((255, 255, 255))

    def ConfigDisableLabel(self):
        self.description_text.SetLabel(_(C.NPD_PAE))
        self.description_text.SetForegroundColour((255, 0, 0))
        self.name_project_textctrl.SetBackgroundColour("Pink")

    def OnCreate(self, nameProject):
        self.presenter.OnNew(nameProject)
        self.OnClose()

    def OnCancel(self, e):
        self.Close(True)

    def OnClose(self):
        self.Close(True)
