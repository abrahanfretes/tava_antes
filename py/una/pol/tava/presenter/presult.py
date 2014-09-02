'''
Created on 30/08/2014

@author: abrahan
'''

import  os
from wx.lib.pubsub import Publisher as pub
import topic as T
from py.una.pol.tava.model.mresult import ResultModel as rm


class AddFileDialogPresenter():
    def __init__(self, iview):
        self.iview = iview
        self.countItem = 0

    def addListPath(self):

        for path in self.iview.dlg.GetPaths():
            dir_name = os.path.split(path)
            dir_name_add = list(dir_name)
            dir_name_add.reverse()
            self.iview.dvlc.AppendItem(dir_name_add)
            self.countItem += 1

        self.iview.o_button.Enable(True)
        self.EnableAllRadioButthon()

    def Close(self):
        self.iview.Close(True)

    def AddFile(self):
        list_path = []
        list_names = []
        for i in range(self.countItem):
            path = self.getPath(i)
            list_path.append(path)
            list_names.append(os.path.basename(path))

        rm().add(list_path, self.iview.project, self.iview.rb.GetSelection())
        pub.sendMessage(T.ADDEDFILE_PROJECT, list_names)
        self.Close()

    def getPath(self, row):

        return os.path.join(self.iview.dvlc.GetTextValue(row, 1),
            self.iview.dvlc.GetTextValue(row, 0))

    def deletedOneFile(self):
        self.iview.dvlc.DeleteItem(self.iview.dvlc.GetSelectedRow())
        self.countItem -= 1
        if self.countItem == 0:
            self.iview.o_button.Enable(False)
            self.DisableAllRadioButthon()

    def DisableAllRadioButthon(self):
        for r in range(self.iview.rb.GetCount()):
            self.iview.rb.EnableItem(r, False)

    def EnableAllRadioButthon(self):
        for r in range(self.iview.rb.GetCount()):
            self.iview.rb.EnableItem(r, True)

    def deletedAllFile(self):
        self.iview.dvlc.DeleteAllItems()
        self.countItem = 0
        self.iview.o_button.Enable(False)
        self.DisableAllRadioButthon()
        #self.iview.rb.EnableItem(0, False)
