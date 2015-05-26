'''
Created on 30/08/2014

@author: abrahan
'''

import os
import wx
import wx.dataview as dv
import wx.lib.scrolledpanel as scrolled
from py.una.pol.tava.presenter.presult import AddFileDialogPresenter
from py.una.pol.tava.base.tavac import correct, nid_error, fos_error, fva_Error
from py.una.pol.tava.base.tavac import fio_error, fuk_error, nip_error
from py.una.pol.tava.base.tavac import style_list as styleNameList
from py.una.pol.tava.base.tavac import wildcard
import py.una.pol.tava.view.vimages as I
from wx import GetTranslation as _
from py.una.pol.tava.base.tavac import vonlucken
import py.una.pol.tava.view.vi18n as C


class AddFileDialog(wx.Dialog):
    def __init__(self, parent, project):
        super(AddFileDialog, self).__init__(parent,
                                title=_(C.AFD_T), size=(600, 590))

        #------ Definiciones iniciales ----------------------------------------
        self.project = project
        self.presenter = AddFileDialogPresenter(self)

        self.InitUI()
        self.Centre()
        self.ShowModal()
        #----------------------------------------------------

    def InitUI(self):
        panel = wx.Panel(self, -1, size=(400, 300))
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        #------ header title description --------------------------------------
        ht_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.f_bmp = wx.StaticBitmap(panel)
        #f_bmp = wx.StaticBitmap(panel, bitmap=I.add_file_png)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        self.header = wx.StaticText(panel)
        #header = wx.StaticText(panel, label=_(C.AFD_STLH))
        self.header.SetFont(font)

        bmp = wx.StaticBitmap(panel, bitmap=I.exec_png)

        ht_sizer.Add(self.f_bmp, flag=wx.ALIGN_LEFT | wx.RIGHT, border=5)
        ht_sizer.Add(self.header, flag=wx.ALIGN_LEFT)
        ht_sizer.Add(bmp, flag=wx.LEFT, border=353)
        #----------------------------------------------------

        #------ button open file ----------------------------------------------
        b_sizer = wx.BoxSizer()
        browse = wx.Button(panel, -1, _(C.AFD_BB))
        b_sizer.Add(browse, flag=wx.ALIGN_BOTTOM | wx.ALIGN_LEFT)
        self.Bind(wx.EVT_BUTTON, self.OnButtonBrowse, browse)
        #----------------------------------------------------

        #------ list DataViewListCtrl file in ScrolledPanel -------------------
        scrolled_panel = scrolled.ScrolledPanel(panel, -1, size=(800, 300),
                    style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)

        l_sizer = wx.BoxSizer()
        self.dvlc = dv.DataViewListCtrl(scrolled_panel)
        self.dvlc.AppendBitmapColumn(_(C.AFD_TCC), 0, width=60)
        self.dvlc.AppendTextColumn(_(C.AFD_TCN), width=250)
        self.dvlc.AppendTextColumn(_(C.AFD_TCD), width=150)
        self.dvlc.AppendTextColumn(_(C.AFD_TCE), width=400)
        l_sizer.Add(self.dvlc, 1, wx.EXPAND)

        scrolled_panel.SetSizer(l_sizer)
        scrolled_panel.SetAutoLayout(1)
        scrolled_panel.SetupScrolling()
        #------------------------------------------------------------------

        #------------ list radio button styles ----------------------------
        s_sizer = wx.BoxSizer()
        dimension = len(styleNameList)
        self.rb = wx.RadioBox(
                panel, -1, _(C.AFD_RBT), wx.DefaultPosition,
                (580, 50), styleNameList, dimension, wx.RA_SPECIFY_COLS)
        self.rb.Bind(wx.EVT_RADIOBOX, self.OnSelectStyle)
        s_sizer.Add(self.rb, 1, wx.EXPAND)

        #------------------------------------------------------------------

        #------ button add and cancel add file --------------------------------
        boc_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.o_button = wx.Button(panel, label=_(C.AFD_BO))
        self.c_button = wx.Button(panel, label=_(C.AFD_BC))
        boc_sizer.Add(self.c_button, flag=wx.RIGHT | wx.LEFT, border=10)
        boc_sizer.Add(self.o_button, flag=wx.RIGHT | wx.LEFT, border=10)

        #----------------------------------------------------

        #------ add sizer global ----------------------------------------------
        self.sizer.Add(ht_sizer, 0.7, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM |
                         wx.LEFT | wx.TOP, border=10)
        self.sizer.Add(b_sizer, 0.5,
                         wx.ALIGN_LEFT | wx.BOTTOM | wx.LEFT, 10)
        self.sizer.Add(scrolled_panel, 6,
                        wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.sizer.Add(s_sizer, 1, wx.ALIGN_RIGHT | wx.RIGHT |
                         wx.LEFT | wx.TOP, 10)
        self.sizer.Add(boc_sizer, 1, wx.ALIGN_RIGHT | wx.ALL, 10)
        panel.SetSizer(self.sizer)

        #----------------------------------------------------

        #------ add event -----------------------------------------------------
        self.o_button.Bind(wx.EVT_BUTTON, self.OnAddFile)
        self.c_button.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.dvlc.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.OnRightClick)
        #----------------------------------------------------

        #------ start config --------------------------------------------------
        self.o_button.Enable(False)
        self.UpDateHiderLabel(0)
        self.rb.EnableItem(vonlucken, False)
        #----------------------------------------------------

        self.Centre()
        self.Show(True)

    def UpDateHiderLabel(self, key):
        if key == 0:
            self.header.SetLabel(label=_(C.AFD_STLH))
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
            defaultDir=os.path.expanduser("~"), defaultFile="", wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)

        if self.dlg.ShowModal() == wx.ID_OK:
            self.presenter.udDateGridFile(self.dlg.GetPaths())
            #self.presenter.addListPath()

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

    def OnSelectStyle(self, event):
        self.presenter.checkStyle()
