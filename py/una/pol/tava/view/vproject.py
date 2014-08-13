# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''

import wx
from wx import GetTranslation as _
from py.una.pol.tava.presenter.pproject import NewProjectDialogPresenter
from py.una.pol.tava.presenter.pproject import RenameProjectDialogPresenter
from py.una.pol.tava.presenter.pproject import DeleteProjectDialogPresenter
import py.una.pol.tava.view.vi18n as C


class NewProjectDialog(wx.Dialog):

    def __init__(self, parent):
        super(NewProjectDialog, self).__init__(parent, size=(600, 250))

        self.presenter = NewProjectDialogPresenter(self)

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel_in = wx.Panel(self)
        sizer_in = wx.GridBagSizer(5, 5)

        #titulo para Creacion de Proyecto
        font1 = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font1.SetWeight(wx.BOLD)
        font1.SetPointSize(14)
        title_h1 = wx.StaticText(panel_in, label=_(C.NPD_TP))
        title_h1.SetFont(font1)
        sizer_in.Add(title_h1, pos=(0, 0), flag=wx.TOP | wx.LEFT, border=15)

        #Figura de tava
        execute_bmp4 = wx.StaticBitmap(panel_in,
                               bitmap=wx.Bitmap('view/icons/exec.png'))
        sizer_in.Add(execute_bmp4, pos=(0, 4),
                     flag=wx.ALIGN_RIGHT | wx.RIGHT, border=15)

        #Texto Descriptivo que cambia
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        self.name_alert = wx.StaticText(panel_in,
                                        label='Crear un nuevo Proyecto Tava')
        self.name_alert.SetFont(font)
        self.execute_bmp6 = wx.StaticBitmap(panel_in)
        hbox1.Add(self.execute_bmp6, flag=wx.LEFT, border=2)
        hbox1.Add(self.name_alert, flag=wx.LEFT, border=2)
        sizer_in.Add(hbox1, pos=(1, 0), span=(1, 3), flag=wx.TOP |
                            wx.LEFT | wx.BOTTOM, border=15)

        #Linea estatica
        line = wx.StaticLine(panel_in)
        sizer_in.Add(line, pos=(2, 0), span=(1, 5),
            flag=wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, border=15)

        #Nombre del Proyecto
        name_project_text = wx.StaticText(panel_in, label=_(C.NPD_NAP))
        sizer_in.Add(name_project_text, pos=(3, 0),
                     flag=wx.LEFT | wx.EXPAND | wx.RIGHT, border=15)

        #Campo para la entrada del nombre de proyecto
        self.name = wx.TextCtrl(panel_in)
        self.name.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.name.SetFocus()
        sizer_in.Add(self.name, pos=(3, 1), span=(1, 4),
                     flag=wx.EXPAND | wx.RIGHT, border=15)

        help_button = wx.Button(panel_in, label=_(C.NPD_HELP))
        sizer_in.Add(help_button, pos=(5, 0), flag=wx.LEFT, border=15)
        self.help_button = help_button

        #Boton Cancelar
        cancel_button = wx.Button(panel_in, label=_(C.NPD_CAN))
        cancel_button.Bind(wx.EVT_BUTTON, self.OnCancel)
        sizer_in.Add(cancel_button, pos=(5, 3),
                     flag=wx.ALIGN_RIGHT | wx.RIGHT, border=15)
        #cancel_button.SetDefault()

        #Boton OK
        self.ok_button = wx.Button(panel_in, label=_(C.NPD_OK))
        self.ok_button.Disable()
        self.ok_button.Bind(wx.EVT_BUTTON, self.OnNew)
        self.ok_button.Disable()
        sizer_in.Add(self.ok_button, pos=(5, 4),
                     flag=wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT, border=15)

        #configuracion del sizer
        sizer_in.AddGrowableCol(2)
        panel_in.SetSizer(sizer_in)

        self.ConfigEnableLabel()

    def OnKeyUp(self, e):

        if(self.presenter.IsNameValido(self.name.Value)):
            if wx.WXK_RETURN == e.GetKeyCode():
                self.OnCreate(self.name.Value)

    def ConfigEnableLabel(self):
        self.name_alert.SetLabel(_(C.NPD_ENP))
        self.IconCorrect()
        self.name_alert.SetForegroundColour((0, 0, 0))
        self.name.SetBackgroundColour((255, 255, 255))

    def ConfigProjectNameEmpty(self):
        self.name_alert.SetLabel(_(C.NPD_PNE))
        self.IconWarning()
        self.name.SetBackgroundColour('#F9EDED')

    def ConfigSlashProjectName(self):
        self.name_alert.SetLabel(_(C.NPD_PNSI))
        self.IconError()
        self.name.SetBackgroundColour((237, 93, 93))

    def ConfigInitPointProjectName(self):
        self.name_alert.SetLabel(_(C.NPD_PNPI))
        self.IconError()
        self.name.SetBackgroundColour((237, 93, 93))

    def ConfigInvalidLenProjectName(self):
        self.name_alert.SetLabel(_(C.NPD_PNLI))
        self.IconError()
        self.name.SetBackgroundColour((237, 93, 93))

    def ConfigExistingProject(self):
        self.name_alert.SetLabel(_(C.NPD_PAE))
        self.IconError()
        self.name.SetBackgroundColour((237, 93, 93))

    def OnNew(self, e):
        self.OnCreate(self.name.Value)

    def ContainsSlash(self):
        return '/' in self.name.Value

    def IconError(self):
        self.execute_bmp6.SetBitmap(
                                wx.Bitmap('view/icons/errornewproject.png'))

    def IconWarning(self):
        self.execute_bmp6.SetBitmap(
                                wx.Bitmap('view/icons/warningnewproject.png'))

    def IconCorrect(self):
        self.execute_bmp6.SetBitmap(
                                wx.Bitmap('view/icons/execute.png'))

    def OnCreate(self, name_project):
        self.presenter.OnNew(self.CleanNameProject(name_project))
        self.OnClose()

    def CleanNameProject(self, name_project):
        return name_project.strip(' ')

    def OnCancel(self, e):
        self.Close(True)

    def OnClose(self):
        self.Close(True)


class RenameProjectDialog(wx.Dialog):

    def __init__(self, parent, message):
        super(RenameProjectDialog, self).__init__(parent,
            title=_(C.RPD_RN), size=(550, 220))

        self.project = message.data
        self.previous_name = self.project.name

        self.presenter_re = RenameProjectDialogPresenter(self)

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):

        cpanel = wx.Panel(self)
        csizer = wx.GridBagSizer(3, 4)

        #Figura de tava
        fig_bmp = wx.StaticBitmap(cpanel,
                                  bitmap=wx.Bitmap('view/icons/exec.png'))
        csizer.Add(fig_bmp, pos=(0, 4),
                   flag=wx.ALIGN_RIGHT | wx.RIGHT, border=15)

        #Texto Descriptivo que cambia
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        self.name_alert = wx.StaticText(cpanel)
        self.name_alert.SetFont(font)
        self.fig_alet_bmp = wx.StaticBitmap(cpanel)
        hbox1.Add(self.fig_alet_bmp, flag=wx.LEFT, border=2)
        hbox1.Add(self.name_alert, flag=wx.LEFT, border=2)
        csizer.Add(hbox1, pos=(0, 0), span=(0, 3), flag=wx.TOP |
                            wx.LEFT | wx.BOTTOM, border=15)

        #Linea estatica
        line = wx.StaticLine(cpanel)
        csizer.Add(line, pos=(1, 0), span=(1, 5),
            flag=wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, border=15)

        level_name_text = wx.StaticText(cpanel, label=_(C.RPD_NN))
        csizer.Add(level_name_text, pos=(2, 0), flag=wx.LEFT | wx.TOP,
                   border=15)
        self.level_name_text = level_name_text

        self.new_name = wx.TextCtrl(cpanel, value=self.previous_name)
        csizer.Add(self.new_name, pos=(2, 1), span=(1, 4),
                   flag=wx.BOTTOM | wx.TOP | wx.RIGHT | wx.EXPAND, border=15)

        self.ok_button = wx.Button(cpanel, label=_(C.RPD_OK))
        csizer.Add(self.ok_button, pos=(3, 4),
                flag=wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT | wx.TOP, border=15)

        self.cancel_button = wx.Button(cpanel, label=_(C.RPD_CAN))
        csizer.Add(self.cancel_button, pos=(3, 3),
                   flag=wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, border=15)

        csizer.AddGrowableCol(2)
        cpanel.SetSizer(csizer)

        self.new_name.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.ok_button.Bind(wx.EVT_BUTTON, self.OnOkRenameEvent)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.OnCancel)

        self.ConfigEnableLabel()

    def OnKeyUp(self, e):

        if(self.presenter_re.IsNameValido(
                                    self.new_name.Value, self.previous_name)):
            if wx.WXK_RETURN == e.GetKeyCode():
                self.presenter_re.OnUpDateName(self.new_name.Value)

    def ConfigEnableLabel(self):
        self.name_alert.SetLabel('RenameProyect')
        self.IconRename()
        self.new_name.SetBackgroundColour((255, 255, 255))

    def ConfigProjectNameEmpty(self):
        self.name_alert.SetLabel(_(C.NPD_PNE))
        self.IconWarning()
        self.new_name.SetBackgroundColour('#F9EDED')

    def ConfigSlashProjectName(self):
        self.name_alert.SetLabel(_(C.NPD_PNSI))
        self.IconError()
        self.SetNameErrorBackground()

    def ConfigInitPointProjectName(self):
        self.name_alert.SetLabel(_(C.NPD_PNPI))
        self.IconError()
        self.SetNameErrorBackground()

    def ConfigInvalidLenProjectName(self):
        self.name_alert.SetLabel(_(C.NPD_PNLI))
        self.IconError()
        self.SetNameErrorBackground()

    def ConfigExistingProject(self):
        self.name_alert.SetLabel(_(C.NPD_PAE))
        self.IconError()
        self.SetNameErrorBackground()

    def SetNameErrorBackground(self):
        self.new_name.SetBackgroundColour((237, 93, 93))

    def IconError(self):
        self.fig_alet_bmp.SetBitmap(
                                wx.Bitmap('view/icons/errornewproject.png'))

    def IconWarning(self):
        self.fig_alet_bmp.SetBitmap(
                                wx.Bitmap('view/icons/warningnewproject.png'))

    def IconRename(self):
        self.fig_alet_bmp.SetBitmap(
                                wx.Bitmap('view/icons/renamenewproject.png'))

    def OnOkRenameEvent(self, event):
        self.presenter_re.OnUpDateName(self.new_name.Value)

    def OnCancel(self, e):
        self.Close(True)


class DeleteProjectDialog():
    def __init__(self, parent, message):

        self.presenter_re1 = DeleteProjectDialogPresenter(self)

        result = wx.MessageBox(_(C.PM_DEL_MESS), _(C.PM_DEL_PRO),
                      style=wx.CENTER | wx.ICON_WARNING | wx.YES_NO)
        if result == wx.YES:
            self.presenter_re1.OnDeleteOk()
