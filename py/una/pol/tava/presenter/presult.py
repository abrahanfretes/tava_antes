'''
Created on 30/08/2014

@author: abrahan
'''

import  os
from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.model.mresult import ResultModel as rm
import topic as T
import py.una.pol.tava.view.vimages as I


class AddFileDialogPresenter():
    def __init__(self, iview):
        self.iview = iview
        self.countItem = 0
        self.existing_names = self.GetNamesResultInProject()

    def GetNamesResultInProject(self):
        return rm().getNamesResultForProject(self.iview.project)

    def addListPath(self):

        self.EnableAllRadioButthon()
        self.iview.o_button.Enable(True)

        for path in self.iview.dlg.GetPaths():
            path_file, name_file = os.path.split(path)
            print name_file
            print  self.existing_names
            if name_file in self.existing_names:
                icon = I.errornewproject_png
                self.DisableAllRadioButthon()
                self.iview.o_button.Enable(False)
            else:
                icon = I.ok_png

            row = [icon, name_file, path_file]
            self.iview.dvlc.AppendItem(row)
            self.countItem += 1

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

        return os.path.join(self.iview.dvlc.GetTextValue(row, 2),
            self.iview.dvlc.GetTextValue(row, 1))

    def deletedOneFile(self):
        self.iview.dvlc.DeleteItem(self.iview.dvlc.GetSelectedRow())
        self.countItem -= 1
        if self.countItem != 0 and self.NamesValid():
            self.iview.o_button.Enable(True)
            self.EnableAllRadioButthon()

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

    def NamesValid(self):
        for row in range(self.countItem):
            if self.iview.dvlc.GetTextValue(row, 1) in self.existing_names:
                return False
        return  True
