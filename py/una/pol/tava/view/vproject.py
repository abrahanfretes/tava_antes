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
from py.una.pol.tava.presenter.pproject import UnHideProjectDialogPresenter
from py.una.pol.tava.presenter.pproject import CheckListCtrlPresenter
from py.una.pol.tava.presenter.pproject import AddFileDialogPresenter
import py.una.pol.tava.view.vi18n as C
import py.una.pol.tava.view.vimages as I


class NewProjectDialog(wx.Dialog):

    def __init__(self, parent):
        super(NewProjectDialog, self).__init__(parent, size=(600, 250))

        self.presenter = NewProjectDialogPresenter(self)

        self.InitUI()
        self.Centre()
        self.ShowModal()

    def InitUI(self):
        panel_in = wx.Panel(self)
        sizer_in = wx.GridBagSizer(5, 5)

        #titulo de Proyecto Tava
        font1 = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font1.SetWeight(wx.BOLD)
        font1.SetPointSize(14)
        title_h1 = wx.StaticText(panel_in, label=_(C.NPD_TP))
        title_h1.SetFont(font1)
        sizer_in.Add(title_h1, pos=(0, 0), flag=wx.TOP | wx.LEFT, border=15)

        #Figura de tava
        execute_bmp4 = wx.StaticBitmap(panel_in, bitmap=I.exec_png)
        sizer_in.Add(execute_bmp4, pos=(0, 4),
                     flag=wx.ALIGN_RIGHT | wx.RIGHT, border=15)

        #Texto Descriptivo que cambia
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        self.name_alert = wx.StaticText(panel_in)
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

        #Boton Ayuda
        help_button = wx.Button(panel_in, label=_(C.NPD_HELP))
        sizer_in.Add(help_button, pos=(5, 0), flag=wx.LEFT, border=15)
        self.help_button = help_button

        #Boton Cancelar
        cancel_button = wx.Button(panel_in, label=_(C.NPD_CAN))
        cancel_button.Bind(wx.EVT_BUTTON, self.OnCancel)
        sizer_in.Add(cancel_button, pos=(5, 3),
                     flag=wx.ALIGN_RIGHT | wx.RIGHT, border=15)

        #Boton OK
        self.ok_button = wx.Button(panel_in, label=_(C.NPD_OK))
        self.ok_button.Disable()
        self.ok_button.Bind(wx.EVT_BUTTON, self.OnCreateProject)
        self.ok_button.Disable()
        sizer_in.Add(self.ok_button, pos=(5, 4),
                     flag=wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT, border=15)

        panel_in.Bind(wx.EVT_CHAR, self.OnKeyDown)

        #configuracion del sizer
        sizer_in.AddGrowableCol(2)
        panel_in.SetSizer(sizer_in)

        self.ConfigEnableLabel()

    def OnKeyUp(self, e):

        if(self.presenter.IsNameValido(self.name.Value)):
            if wx.WXK_RETURN == e.GetKeyCode():
                self.presenter.CreateProject(self.name.Value)

    def ConfigEnableLabel(self):
        self.name_alert.SetLabel(_(C.NPD_ENP))
        self.IconCorrect()
        self.name.SetBackgroundColour((255, 255, 255))

    def ConfigProjectNameEmpty(self):
        self.name_alert.SetLabel(_(C.NPD_PNE))
        self.IconWarning()
        self.name.SetBackgroundColour('#F9EDED')

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

    def ConfigExistingHideProject(self):
        self.name_alert.SetLabel(_(C.NPD_HPAE))
        self.IconError()
        self.SetNameErrorBackground()

    def OnCreateProject(self, e):
        self.presenter.CreateProject(self.name.Value)

    def ContainsSlash(self):
        return '/' in self.name.Value

    def IconError(self):
        self.execute_bmp6.SetBitmap(I.errornewproject_png)

    def IconWarning(self):
        self.execute_bmp6.SetBitmap(I.warningnewproject_png)

    def IconCorrect(self):
        self.execute_bmp6.SetBitmap(I.execute_png)

    def SetNameErrorBackground(self):
        self.name.SetBackgroundColour((237, 93, 93))

    def CleanNameProject(self, name_project):
        return name_project.strip(' ')

    def OnCancel(self, e):
        self.Close(True)

    def OnKeyDown(self, e):
        key = e.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.Close()


class RenameProjectDialog(wx.Dialog):

    def __init__(self, parent, project):
        super(RenameProjectDialog, self).__init__(parent,
            title=_(C.RPD_RN), size=(550, 220))

        self.project = project
        self.previous_name = self.project.name

        self.presenter_re = RenameProjectDialogPresenter(self)

        self.InitUI()
        self.Centre()
        self.ShowModal()()

    def InitUI(self):

        cpanel = wx.Panel(self)
        csizer = wx.GridBagSizer(3, 4)

        #Figura de tava
        fig_bmp = wx.StaticBitmap(cpanel, bitmap=I.exec_png)
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

        cpanel.Bind(wx.EVT_CHAR, self.OnKeyDown)

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

    def ConfigExistingHideProject(self):
        self.name_alert.SetLabel(_(C.NPD_HPAE))
        self.IconError()
        self.SetNameErrorBackground()

    def SetNameErrorBackground(self):
        self.new_name.SetBackgroundColour((237, 93, 93))

    def IconError(self):
        self.fig_alet_bmp.SetBitmap(I.errornewproject_png)

    def IconWarning(self):
        self.fig_alet_bmp.SetBitmap(I.warningnewproject_png)

    def IconRename(self):
        self.fig_alet_bmp.SetBitmap(I.renamenewproject_png)

    def OnOkRenameEvent(self, event):
        self.presenter_re.OnUpDateName(self.new_name.Value)

    def OnCancel(self, e):
        self.Close(True)

    def OnKeyDown(self, e):
        key = e.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.Close()


class DeleteProjectDialog():
    def __init__(self):

        self.presenter_re1 = DeleteProjectDialogPresenter(self)

        result = wx.MessageBox(_(C.PM_DEL_MESS), _(C.PM_DEL_PRO),
                      style=wx.CENTER | wx.ICON_WARNING | wx.YES_NO)
        if result == wx.YES:
            self.presenter_re1.OnDeleteOk()


class PropertiesProjectDialog(wx.Dialog):

    def __init__(self, parent, project):
        super(PropertiesProjectDialog, self).__init__(parent,
                            title=_(C.PPD_PF), size=(450, 200))

        self.project = project
        self.InitUI()
        self.Centre()
        self.ShowModal()

    def InitUI(self):

        panel = wx.Panel(self)

        sizer = wx.GridBagSizer(5, 5)

        font1 = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font1.SetWeight(wx.BOLD)
        font1.SetPointSize(14)
        title_h1 = wx.StaticText(panel, label=_(C.NPD_TP))
        title_h1.SetFont(font1)
        sizer.Add(title_h1, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                  border=15)

        top_line = wx.StaticLine(panel)
        sizer.Add(top_line, pos=(1, 0), span=(1, 5),
            flag=wx.EXPAND | wx.BOTTOM, border=10)

        name_text = wx.StaticText(panel, label=_(C.PPD_NA))
        sizer.Add(name_text, pos=(2, 0), flag=wx.LEFT, border=10)

        name_value_text = wx.StaticText(panel, label=self.project.name)
        name_value_text.Disable()
        sizer.Add(name_value_text, pos=(2, 1), span=(1, 4), flag=wx.RIGHT |
                  wx.EXPAND)

        creation_date_text = wx.StaticText(panel, label=_(C.PPD_CD))
        sizer.Add(creation_date_text, pos=(3, 0), flag=wx.LEFT, border=10)

        creation_date_value_text = wx.StaticText(panel,
                                        label=str(self.project.creation_date))
        creation_date_value_text.Disable()
        sizer.Add(creation_date_value_text, pos=(3, 1), span=(1, 4),
                  flag=wx.RIGHT | wx.EXPAND)

        bottom_line = wx.StaticLine(panel)
        sizer.Add(bottom_line, pos=(5, 0), span=(1, 5),
            flag=wx.EXPAND | wx.BOTTOM, border=10)

        cancel_button = wx.Button(panel, label=_(C.PPD_CAN))
        sizer.Add(cancel_button, pos=(6, 3),
            flag=wx.BOTTOM | wx.RIGHT, border=5)

        ok_button = wx.Button(panel, label=_(C.PPD_OK))
        ok_button.SetFocus()
        ok_button.Bind(wx.EVT_BUTTON, self.OnClose)
        sizer.Add(ok_button, pos=(6, 4), flag=wx.ALIGN_RIGHT
                  | wx.LEFT, border=5)

        panel.Bind(wx.EVT_CHAR, self.OnKeyDown)

        sizer.AddGrowableCol(2)

        panel.SetSizer(sizer)

    def OnClose(self, e):
        self.Close(True)

    def OnKeyDown(self, e):
        key = e.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.Close()


import sys
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1,
                             style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)

        self.presenter_List = CheckListCtrlPresenter(self)

    def OnCheckItem(self, index, flag):
        self.presenter_List.OnClickCheckbox()


class UnHideProjectDialog(wx.Dialog):
    def __init__(self, parent):
        super(UnHideProjectDialog, self).__init__(parent,
                                title=_(C.UHPD_T), size=(600, 500))
        _(C.PPD_CD)

        self.presenter_hide = UnHideProjectDialogPresenter(self)
        self.InitUI()
        self.Centre()
        self.ShowModal()

    def InitUI(self):

        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        #parte cabecera
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetWeight(wx.BOLD)
        font.SetPointSize(9)
        self.description = wx.StaticText(panel,
                            label=_(C.UHPD_STD))
        self.description.SetFont(font)
        self.bmp = wx.StaticBitmap(panel)
        self.bmp.SetBitmap(I.hide_left_png)
        bmp1 = wx.StaticBitmap(panel, bitmap=I.exec_png)
        hbox1.Add(self.bmp, 1, wx.RIGHT, 10)
        hbox1.Add(self.description, wx.RIGHT, 10)
        hbox1.Add(bmp1, 1, wx.LEFT, 220)
        vbox.Add(hbox1, 1, wx.ALIGN_LEFT | wx.ALL, 10)

        #parte del checList
        self.list = CheckListCtrl(panel)
        self.list.InsertColumn(0, _(C.UHPD_CLN), width=300)
        self.list.InsertColumn(1, _(C.UHPD_CLD), width=175)
        self.list.InsertColumn(2, _(C.UHPD_CLS), width=105)

        is_empty = True
        for p in self.presenter_hide.GetHideProject():
            is_empty = False
            index = self.list.InsertStringItem(sys.maxint, p.name)
            self.list.SetStringItem(index, 1, str(p.creation_date))
            self.list.SetStringItem(index, 2, _(C.UHPD_CLCS))

        vbox.Add(self.list, 8, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        if(is_empty):
            self.IsEmptyList()

        # parte de los botones
        sb = wx.StaticBox(panel, label=_(C.UHPD_SBL))
        boxsizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        sel = wx.Button(panel, -1, _(C.UHPD_BSAL))
        des = wx.Button(panel, -1, _(C.UHPD_BDSAL))
        hboxl = wx.BoxSizer(wx.HORIZONTAL)
        hboxl.Add(sel, 1, wx.ALL, 10)
        hboxl.Add(des, 1, wx.ALL, 10)
        boxsizer.Add(hboxl, 1,  wx.EXPAND | wx.RIGHT, 350)
        vbox.Add(boxsizer, 1,
                wx.EXPAND | wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        self.apply_change = wx.Button(panel, -1, _(C.UHPD_BRL))
        cancel = wx.Button(panel, -1, _(C.UHPD_BCL))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(cancel, 1, wx.RIGHT, 10)
        hbox.Add(self.apply_change)

        vbox.Add(hbox, 1, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        panel.SetSizer(vbox)

        #Eventos
        self.Bind(wx.EVT_BUTTON, self.OnSelectAll, id=sel.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, id=des.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnApply, id=self.apply_change.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=cancel.GetId())

        #disable bottom al inicio
        self.apply_change.Enable(False)

        panel.Bind(wx.EVT_CHAR, self.OnKeyDown)

        self.Centre()
        self.Show(True)

    def OnSelectAll(self, event):
        self.presenter_hide.SelectAll()

    def OnDeselectAll(self, event):
        self.presenter_hide.DeselectAll()

    def OnApply(self, event):
        self.presenter_hide.Restore()

    def OnCancel(self, event):
        self.presenter_hide.ExitDialog()

    def IsEmptyList(self):
        self.description.SetLabel(_(C.UHPD_STDE))
        self.bmp.SetBitmap(I.warningnewproject_png)

    def OnKeyDown(self, e):
        key = e.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.Close()

import os
import wx.dataview as dv
#-------------------------- list style existing -------------------------------
styleNameList = ['Von Lucken', 'otro']
#---------------------------------------------------------------------------

#-------------------- pre-establish a file filter -----------------------------
wildcard = "Python source (*.py)|*.py|"     \
           "Compiled Python (*.pyc)|*.pyc|" \
           "SPAM files (*.spam)|*.spam|"    \
           "Egg file (*.egg)|*.egg|"        \
           "All files (*.*)|*.*"
#---------------------------------------------------------------------------


class AddFileDialog(wx.Dialog):
    def __init__(self, parent):
        super(AddFileDialog, self).__init__(parent,
                                title='hola', size=(600, 500))

        self.presenter = AddFileDialogPresenter(self)
        panel = wx.Panel(self, -1, size=(595, 495))
        self.g_sizer = wx.BoxSizer(wx.VERTICAL)

        #------ header title description --------------------------------------
        ht_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #f_bmp = wx.StaticBitmap(panel,bitmap=wx.Bitmap('/icons/add_file.png'))
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        header = wx.StaticText(panel, label='Agregar archivo al proyecto')
        header.SetFont(font)

        #bmp = wx.StaticBitmap(panel, bitmap=wx.Bitmap('/icons/exec.png'))

        #ht_sizer.Add(f_bmp, flag=wx.ALIGN_LEFT | wx.RIGHT, border=5)
        ht_sizer.Add(header, flag=wx.ALIGN_LEFT)
        #ht_sizer.Add(bmp, flag=wx.LEFT, border=386)
        #----------------------------------------------------

        #------ list DataViewListCtrl file ------------------------------------
        l_sizer = wx.BoxSizer()
        self.dvlc = dv.DataViewListCtrl(panel)
        self.dvlc.AppendTextColumn('Name', width=220)
        self.dvlc.AppendTextColumn('directorio', width=100)
        l_sizer.Add(self.dvlc, 1, wx.EXPAND)
        #------------------------------------------------------------------

        #------ button open  file ---------------------------------------------
        b_sizer = wx.BoxSizer()
        add_button = wx.Button(panel, -1, "Seleccionar Archivo")
        b_sizer.Add(add_button, flag=wx.ALIGN_BOTTOM | wx.ALIGN_LEFT)
        self.Bind(wx.EVT_BUTTON, self.OnButton, add_button)
        #----------------------------------------------------

        #------------ list radio button styles ----------------------------
        s_sizer = wx.BoxSizer()
        dimension = len(styleNameList)
        self.rb = wx.RadioBox(
                panel, -1, "Seleccione el estilo", wx.DefaultPosition,
                (600, 50), styleNameList, dimension, wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, self.rb)
        s_sizer.Add(self.rb, 1, wx.EXPAND)

        #------------------------------------------------------------------

        #------ button add and cancel add file --------------------------------
        boc_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.o_button = wx.Button(panel, label='Ok')
        self.c_button = wx.Button(panel, label='Cancel')
        boc_sizer.Add(self.c_button)
        boc_sizer.Add(self.o_button)

        #----------------------------------------------------

        #------ add sizer global ----------------------------------------------
        self.g_sizer.Add(ht_sizer, 0.7, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM |
                         wx.LEFT | wx.TOP, border=10)
        self.g_sizer.Add(b_sizer, 0.5,
                         wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, 10)
        self.g_sizer.Add(l_sizer, 5,
                         wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.g_sizer.Add(s_sizer, 1, wx.ALL, 10)
        self.g_sizer.Add(boc_sizer, 1, wx.ALL | wx.ALIGN_RIGHT, 10)
        panel.SetSizer(self.g_sizer)

        #----------------------------------------------------

        #------ add event -----------------------------------------------------
        self.o_button.Bind(wx.EVT_BUTTON, self.OnAddFile)
        self.c_button.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.dvlc.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.OnRightClick)
        #----------------------------------------------------

        #------ start config --------------------------------------------------
        self.o_button.Enable(False)
        self.rb.EnableItem(0, False)
        self.rb.EnableItem(1, False)
        #----------------------------------------------------
        self.Show()

    def OnCancel(self, event):
        self.presenter.Close()

    def OnAddFile(self, event):
        self.presenter.AddFile()

    def EvtRadioBox(self, event):
        print 'EvtRadioBox: %d\n' % event.GetInt()

    def OnButton(self, evt):

        self.dlg = wx.FileDialog(
            self, message="Seleccione archivos",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )

        if self.dlg.ShowModal() == wx.ID_OK:
            self.presenter.addListPath()

        self.dlg.Destroy()

    def OnRightClick(self, event):

        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnDeletedOneFile, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnDeletedAllFile, id=self.popupID2)

        # make a menu
        menu = wx.Menu()
        menu.Append(self.popupID1, "Delete File Selected")
        menu.Append(self.popupID2, "Delete All File")

        self.PopupMenu(menu)
        menu.Destroy()

    def OnDeletedOneFile(self, event):
        self.presenter.deletedOneFile()

    def OnDeletedAllFile(self, event):
        self.presenter.deletedAllFile()
