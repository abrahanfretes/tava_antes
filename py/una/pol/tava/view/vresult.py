'''
Created on 30/08/2014

@author: abrahan
'''

import os
import wx
import wx.dataview as dv
from py.una.pol.tava.presenter.presult import AddFileDialogPresenter
import py.una.pol.tava.view.vimages as I
from wx import GetTranslation as _
import py.una.pol.tava.view.vi18n as C

#-------------------------- list style existing -------------------------------
styleNameList = ['Von Lucken', 'otro']
#---------------------------------------------------------------------------

#-------------------- pre-establish a file filter -----------------------------
wildcard = "All files (*.*)|*.*"
#---------------------------------------------------------------------------


class AddFileDialog(wx.Dialog):
    def __init__(self, parent):
        super(AddFileDialog, self).__init__(parent,
                                title=_(C.AFD_T), size=(600, 500))

        #------ Definiciones iniciales ----------------------------------------
        self.presenter = AddFileDialogPresenter(self)

        self.InitUI()
        self.Centre()
        self.ShowModal()
        #----------------------------------------------------

    def InitUI(self):
        panel = wx.Panel(self, -1, size=(595, 495))
        self.g_sizer = wx.BoxSizer(wx.VERTICAL)

        #------ header title description --------------------------------------
        ht_sizer = wx.BoxSizer(wx.HORIZONTAL)
        f_bmp = wx.StaticBitmap(panel, bitmap=I.add_file_png)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        header = wx.StaticText(panel, label=_(C.AFD_STLH))
        header.SetFont(font)

        bmp = wx.StaticBitmap(panel, bitmap=I.exec_png)

        ht_sizer.Add(f_bmp, flag=wx.ALIGN_LEFT | wx.RIGHT, border=5)
        ht_sizer.Add(header, flag=wx.ALIGN_LEFT)
        ht_sizer.Add(bmp, flag=wx.LEFT, border=353)
        #----------------------------------------------------

        #------ list DataViewListCtrl file ------------------------------------
        l_sizer = wx.BoxSizer()
        self.dvlc = dv.DataViewListCtrl(panel)
        self.dvlc.AppendTextColumn(_(C.AFD_TCN), width=220)
        self.dvlc.AppendTextColumn(_(C.AFD_TCD), width=100)
        l_sizer.Add(self.dvlc, 1, wx.EXPAND)
        #------------------------------------------------------------------

        #------ button open file ----------------------------------------------
        b_sizer = wx.BoxSizer()
        browse = wx.Button(panel, -1, _(C.AFD_BB))
        b_sizer.Add(browse, flag=wx.ALIGN_BOTTOM | wx.ALIGN_LEFT)
        self.Bind(wx.EVT_BUTTON, self.OnButtonBrowse, browse)
        #----------------------------------------------------

        #------------ list radio button styles ----------------------------
        s_sizer = wx.BoxSizer()
        dimension = len(styleNameList)
        self.rb = wx.RadioBox(
                panel, -1, _(C.AFD_RBT), wx.DefaultPosition,
                (600, 50), styleNameList, dimension, wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, self.rb)
        s_sizer.Add(self.rb, 1, wx.EXPAND)

        #------------------------------------------------------------------

        #------ button add and cancel add file --------------------------------
        boc_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.o_button = wx.Button(panel, label=_(C.AFD_BO))
        self.c_button = wx.Button(panel, label=_(C.AFD_BC))
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

        self.Centre()
        self.Show(True)

    def OnCancel(self, event):
        self.presenter.Close()

    def OnAddFile(self, event):
        self.presenter.AddFile()

    def EvtRadioBox(self, event):
        print 'EvtRadioBox: %d\n' % event.GetInt()

    def OnButtonBrowse(self, evt):

        self.dlg = wx.FileDialog(self, message=_(C.AFD_FDM),
            defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)

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
        menu.Append(self.popupID1, _(C.AFD_FDMD))
        menu.Append(self.popupID2, _(C.AFD_FDMDA))

        self.PopupMenu(menu)
        menu.Destroy()

    def OnDeletedOneFile(self, event):
        self.presenter.deletedOneFile()

    def OnDeletedAllFile(self, event):
        self.presenter.deletedAllFile()
