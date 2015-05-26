# -*- coding: utf-8 -*-
'''
Created on 14/5/2015

@author: abrahan
'''

import os
import wx
import wx.dataview as dv
from py.una.pol.tava.presenter.pmetricfile import AddMetricFileDialogPresenter
from py.una.pol.tava.base.tavac import correct, nid_error, fos_error, fva_Error
from py.una.pol.tava.base.tavac import fio_error, fuk_error, nip_error
from py.una.pol.tava.base.tavac import content_error
from py.una.pol.tava.base.tavac import style_list as styleNameList
from py.una.pol.tava.base.tavac import wildcard
import py.una.pol.tava.view.vimages as I
from wx import GetTranslation as _
from py.una.pol.tava.base.tavac import vonlucken
import py.una.pol.tava.view.vi18n as C


class AddMetricFileDialog(wx.Dialog):
    def __init__(self, parent, project):
        wx.Dialog.__init__(self, parent, title=_(C.AFD_T), size=(600, 590))

        self.project = project
        self.presenter = AddMetricFileDialogPresenter(self, project)

        self.InitUI()
        self.Centre()
        self.ShowModal()
        # ----------------------------------------------------

    def InitUI(self):
        panel = wx.Panel(self, -1, size=(400, 300))

        # ------ header title description -------------------------------------
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        self.f_bmp = wx.StaticBitmap(panel)
        self.text_header = wx.StaticText(panel)
        self.text_header.SetFont(font)
        bmp = wx.StaticBitmap(panel, bitmap=I.exec_png)

        h_sizer.Add(self.f_bmp, flag=wx.ALIGN_LEFT | wx.RIGHT, border=5)
        h_sizer.Add(self.text_header, flag=wx.ALIGN_LEFT)
        h_sizer.Add(bmp, flag=wx.LEFT, border=353)

        # ------ button open file ---------------------------------------------
        b_sizer = wx.BoxSizer()
        browse = wx.Button(panel, -1, _(C.AFD_BB))
        b_sizer.Add(browse, flag=wx.ALIGN_BOTTOM | wx.ALIGN_LEFT)
        browse.Bind(wx.EVT_BUTTON, self.OnButtonBrowse)

        # ------ list DataViewListCtrl file in ScrolledPanel ------------------
        l_sizer = wx.BoxSizer()
        self.dvlc = dv.DataViewListCtrl(panel)
        self.dvlc.AppendBitmapColumn(_(C.AFD_TCC), 0, width=60)
        self.dvlc.AppendTextColumn(_(C.AFD_TCN), width=250)
        self.dvlc.AppendTextColumn(_(C.AFD_TCD), width=150)
        self.dvlc.AppendTextColumn(_(C.AFD_TCE), width=400)
        l_sizer.Add(self.dvlc, 1, wx.EXPAND)

        # ------------ list radio button styles ----------------------------
        s_sizer = wx.BoxSizer()
        dimension = len(styleNameList)
        self.rb = wx.RadioBox(panel, -1, _(C.AFD_RBT), wx.DefaultPosition,
                              (580, 50), styleNameList, dimension,
                              wx.RA_SPECIFY_COLS)
        self.rb.Bind(wx.EVT_RADIOBOX, self.OnSelectStyle)
        s_sizer.Add(self.rb, 1, wx.EXPAND)

        # ----- button add and cancel add file --------------------------------
        boc_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.o_button = wx.Button(panel, label=_(C.AFD_BO))
        self.c_button = wx.Button(panel, label=_(C.AFD_BC))
        boc_sizer.Add(self.c_button, flag=wx.RIGHT | wx.LEFT, border=10)
        boc_sizer.Add(self.o_button, flag=wx.RIGHT | wx.LEFT, border=10)

        # ------ add sizer global ---------------------------------------------
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(h_sizer, 0.7, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM |
                       wx.LEFT | wx.TOP, border=10)
        self.sizer.Add(b_sizer, 0.5, wx.ALIGN_LEFT | wx.BOTTOM | wx.LEFT, 10)
        self.sizer.Add(l_sizer, 6, wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.sizer.Add(s_sizer, 1, wx.ALIGN_RIGHT | wx.RIGHT |
                       wx.LEFT | wx.TOP, 10)
        self.sizer.Add(boc_sizer, 1, wx.ALIGN_RIGHT | wx.ALL, 10)
        panel.SetSizer(self.sizer)

        # ------ add event ----------------------------------------------------
        self.o_button.Bind(wx.EVT_BUTTON, self.OnAddFile)
        self.c_button.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.dvlc.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.OnRightClick)
        # ----------------------------------------------------

        # ------ start config -------------------------------------------------
        self.setInitValues()
        # ----------------------------------------------------

        self.Centre()
        self.Show(True)

    def setInitValues(self):
        self.o_button.Disable()
        self.UpDateHiderLabel(0)
        self.rb.EnableItem(vonlucken, False)

    def UpDateHiderLabel(self, key):
        if key == 0:
            # self.text_header.SetLabel(label=_(C.AFD_STLH))
            text = 'Agregar Archivos con Resultados de Métricas'
            self.text_header.SetLabel(label=text)
            self.f_bmp.SetBitmap(I.add_file_png)
            return None

        if key == 1:
            self.f_bmp.SetBitmap(I.errornewproject_png)
            return None

    def OnCancel(self, event):
        self.presenter.Close()

    def OnAddFile(self, event):
        self.presenter.AddFile()

    def OnButtonBrowse(self, evt):

        self.dlg = wx.FileDialog(self, message=_(C.AFD_FDM),
                                 defaultDir=os.path.expanduser("~"),
                                 defaultFile="", wildcard=wildcard,
                                 style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
        if self.dlg.ShowModal() == wx.ID_OK:
            self.presenter.updateGridFile(self.dlg.GetFilenames(),
                                          self.dlg.GetPaths())
        self.dlg.Destroy()

    def getLabelError(self, error):
        if error == correct:
            return _(C.AFD_EN)
        elif error == nid_error:
            return _(C.AFD_EDNG)
        elif error == nip_error:
            return _(C.AFD_EDNP)
        elif error == fos_error:
            return _(C.AFD_ERS)
        elif error == fva_Error:
            return _(C.AFD_EFF)
        elif error == fio_error:
            return _(C.AFD_EOF)
        elif error == fuk_error:
            return _(C.AFD_EUE)
        elif error == content_error:
            return 'Error de Contenido'

    def OnRightClick(self, event):
        if self.presenter.isAnyRowSelected():
            if not hasattr(self, "popupID1"):
                self.popupID1 = wx.NewId()
                self.popupID2 = wx.NewId()

                self.Bind(wx.EVT_MENU, self.OnDeletedOneFile, id=self.popupID1)
                self.Bind(wx.EVT_MENU, self.OnDeletedAllFile, id=self.popupID2)

            # make a menu
            menu = wx.Menu()
            menu.Append(self.popupID1, _(C.AFD_FDMD))
            menu.Append(self.popupID2, _(C.AFD_FDMDA))

            self.PopupMenu(menu)
            menu.Destroy()

    def OnDeletedOneFile(self, event):
        self.presenter.deletedOneFile()

    def OnDeletedAllFile(self, event):
        self.presenter.deletedAllFile()
        self.setInitValues()

    def OnSelectStyle(self, event):
        self.presenter.checkStyle()
