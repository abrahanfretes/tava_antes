'''
Created on 30/08/2014

@author: abrahan
'''

import  os
from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.model.mresult import ResultModel as rm
from py.una.pol.tava.base.tavac import nid_error, nip_error, correct
import topic as T
import py.una.pol.tava.view.vimages as I


class AddFileDialogPresenter():
    def __init__(self, iview):
        self.iview = iview
        self.countItem = 0
        self.listNamesError = []
        self.existing_names = self.GetNamesResultInProject()

    def addListPath(self):

        self.EnableAllRadioButthon()
        self.iview.o_button.Enable(True)

        for path in self.iview.dlg.GetPaths():
            path_file, name_file = os.path.split(path)

            valid = self.IsValidFile(path_file, name_file)
            if valid != correct:
                self.listNamesError.append(name_file)
                icon = I.errornewproject_png
                error = self.iview.getLabelError(valid)
                self.DisableAllRadioButthon()
                self.iview.o_button.Enable(False)
            else:
                icon = I.ok_png
                error = self.iview.getLabelError(correct)

            row = [icon, name_file, path_file, error]
            self.iview.dvlc.AppendItem(row)
            self.countItem += 1

    def IsValidFile(self, path, name):
        if  self.name_in_datetable(name):
            return nid_error
        if name in self.existing_names:
            return nip_error
        file_valid = self.CorrectStyleFormat(os.path.join(path, name))
        if file_valid != 0:
            return file_valid
        return correct

    def name_in_datetable(self, name):

        for row in range(self.countItem):
            if self.iview.dvlc.GetTextValue(row, 1) == name:
                return True
        return False

    def deletedOneFile(self):
        row = self.iview.dvlc.GetSelectedRow()
        self.iview.dvlc.DeleteItem(row)
        self.countItem -= 1

        if self.isConsistente():
            self.iview.o_button.Enable(True)
            self.EnableAllRadioButthon()
        else:
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
        self.listNamesError = []
        self.iview.o_button.Enable(False)
        self.DisableAllRadioButthon()
        #self.iview.rb.EnableItem(0, False)

    def isConsistente(self):
        if self.countItem == 0:
            return False
        not_error = self.iview.getLabelError(correct)
        for row in range(self.countItem):
            if self.iview.dvlc.GetTextValue(row, 3) != not_error:
                return False
        return  True

    def getPath(self, row):

        return os.path.join(self.iview.dvlc.GetTextValue(row, 2),
            self.iview.dvlc.GetTextValue(row, 1))

    def isAnyRowSelected(self):
        for row in range(self.countItem):
            if self.iview.dvlc.IsRowSelected(row):
                return True
        return False

    def Close(self):
        self.iview.Close(True)

    #------ funciones que interactuan con el modelo ---------------------------

    def GetNamesResultInProject(self):
        return rm().getNamesResultForProject(self.iview.project)

    def CorrectStyleFormat(self, path_file):
        style = self.iview.rb.GetSelection()
        return rm().fastVerificationStyle(path_file, style)

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

    #-----------------------------------------------------------------
