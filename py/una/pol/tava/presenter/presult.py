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
        self.existing_names = self.GetNamesResultInProject()

    def udDateGridFile(self, list_path):
        self.addListPath(list_path)
        self.setStateComponetsFile()

    def addListPath(self, list_path):

        for path in list_path:

            path_file, name_file = os.path.split(path)
            valid = self.IsValidFile(path_file, name_file)
            if valid != correct:
                icon, label_error = self.getIconAndLabelFileError(valid)

            else:
                icon, label_error = self.getIconAndLabelFileCorrect(correct)

            row = [icon, name_file, path_file, label_error]
            self.iview.dvlc.AppendItem(row)
            self.countItem += 1

    def getIconAndLabelFileError(self, key_error):
        return  I.errornewproject_png, self.iview.getLabelError(key_error)

    def getIconAndLabelFileCorrect(self, key_correct):
        return  I.ok_png, self.iview.getLabelError(key_correct)

    def setStateComponetsFile(self):
        if self.isValidAllFiles():
            self.iview.o_button.Enable()
            self.iview.UpDateHiderLabel(0)
            if self.isEmptyGrip():
                self.iview.o_button.Disable()
        else:
            self.iview.o_button.Disable()
            self.iview.UpDateHiderLabel(1)

        self.setStateComponentsStyle()

    def isEmptyGrip(self):
        if self.countItem == 0:
            return True
        return False

    def setStateComponentsStyle(self):
        if self.isEmptyGrip():
            self.disableStyles()
        else:
            self.enableStyles()

    def IsValidFile(self, path, name):
        if  self.nameInDatetable(name):
            return nid_error
        if name in self.existing_names:
            return nip_error
        file_valid = self.CorrectStyleFormat(os.path.join(path, name))
        if file_valid != 0:
            return file_valid
        return correct

    def isValidAllFiles(self):
        not_error = self.iview.getLabelError(correct)
        for row in range(self.countItem):
            if self.iview.dvlc.GetTextValue(row, 3) != not_error:
                return False
        return  True

    def nameInDatetable(self, name):

        for row in range(self.countItem):
            if self.iview.dvlc.GetTextValue(row, 1) == name:
                return True
        return False

    def deletedOneFile(self):
        row = self.iview.dvlc.GetSelectedRow()
        self.iview.dvlc.DeleteItem(row)
        self.countItem -= 1
        self.setStateComponetsFile()

    def deletedAllFile(self):
        self.iview.dvlc.DeleteAllItems()
        self.countItem = 0
        self.setStateComponetsFile()

    def checkStyle(self):
        list_path = self.getListPath()
        self.deletedAllFile()
        self.udDateGridFile(list_path)

    def getListPath(self):
        list_path = []
        for row in range(self.countItem):
            name = self.iview.dvlc.GetTextValue(row, 1)
            path = self.iview.dvlc.GetTextValue(row, 2)
            fpath = os.path.join(path, name)
            list_path.append(fpath)

        return list_path

    def enableStyles(self):
        for i in range(self.iview.rb.GetCount()):
            self.iview.rb.EnableItem(i, True)

    def disableStyles(self):
        for i in range(self.iview.rb.GetCount()):
            self.iview.rb.EnableItem(i, False)

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
        style = self.iview.rb.GetSelection()
        for i in range(self.countItem):
            path = self.getPath(i)
            list_path.append(path)
            list_names.append(os.path.basename(path))
        project = rm().add(list_path, self.iview.project, style)
        pub.sendMessage(T.ADDEDFILE_PROJECT, project)
        self.Close()

    def getPath(self, row):

        return os.path.join(self.iview.dvlc.GetTextValue(row, 2),
            self.iview.dvlc.GetTextValue(row, 1))
    #-----------------------------------------------------------------
