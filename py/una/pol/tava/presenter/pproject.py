'''
Created on 28/07/2014

@author: afretes
'''
import wx
from py.una.pol.tava.model.mproject import ProjectModel as pro
from py.una.pol.tava.model.mresult import ResultModel as res
from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.base.entity import OPEN
import topic as T
import  os
import py.una.pol.tava.view.vimages as I
from py.una.pol.tava.base.tavac import correct, nid_error
from py.una.pol.tava.model.mresult import ResultModel as rm


class NewProjectDialogPresenter():
    def __init__(self, iview):
        self.iview = iview
        self.listNamesProject = self.GetNamesProject()
        self.listNamesHideProject = self.GetNamesHideProject()

        #para control de agregar archivos
        self.countItem = 0

    #-- maneja eventos desde teclado -----------------------
    def keyboardEvents(self, key_code):

        if key_code == wx.WXK_ESCAPE:
            self.ExitDialog()

        elif key_code == wx.WXK_RETURN:
            self.tryToCreate()

        else:
            self.setStateComponets()
    #---------------------------------------------

    #-- creacoin de nuevo Proyecto -----------------------
    def tryToCreate(self):
        if self.isValidProject():
            self.CreateProject()

    def CreateProject(self):
        name = self.iview.name_project_textctrl.Value
        project = pro().add(name.strip(' '))
        list_path_file = self.getListPath()
        if len(list_path_file) != 0:
            style = self.iview.rb.GetSelection()
            res().add(list_path_file, project, style)
        pub.sendMessage(T.PROJECT_NEW, project)
        self.iview.Close(True)
    #---------------------------------------------

    #-- validaciones del nuevo proyecto -----------------
    def isValidProject(self):
        if not self.isValidNameProject():
            return False
        if not self.isValidAllFiles():
            return False
        return True

    def isValidNameProject(self):
        if 0 == self.keyValidName():
            return True
        return False

    # codigo de validacion para nombre de proyecto
    def keyValidName(self):
        name = self.iview.name_project_textctrl.Value

        if len(name.strip(' ')) == 0:
            return 1
        if '/' in name:
            return 2
        if name[0] == '.':
            return 3
        if len(name.strip(' ')) > 100:
            return 4
        if name in self.listNamesProject:
            return 5
        if name in self.listNamesHideProject:
            return 6
        return 0
    #---------------------------------------------

    #-- validaciones de componetes de la vista -----------------
    def setStateComponets(self):
        valid = 0

        #verifica si el nombre es correcto
        key_name = self.keyValidName()
        if key_name != valid:
            self.iview.UpDateHiderLabel(key_name)
            self.disablesButtonsProject()
            return None

        self.enableButtonsProject()
        self.setStateComponetsFile()
        return None

    def enableButtonsProject(self):
        self.iview.ok_button.Enable()
        self.iview.UpDateHiderLabel(0)
        self.iview.browse.Enable()
        self.iview.scrolled_panel.Enable()

    def disablesButtonsProject(self):
        self.iview.ok_button.Disable()
        self.iview.browse.Enable(False)
        self.iview.scrolled_panel.Enable(False)
        self.disableStyles()

    def enableStyles(self):
        for i in range(self.iview.rb.GetCount()):
            self.iview.rb.EnableItem(i, True)

    def disableStyles(self):
        for i in range(self.iview.rb.GetCount()):
            self.iview.rb.EnableItem(i, False)
    #---------------------------------------------

    #--Funciones para agregar archivos ----------------------------------------

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
            self.iview.ok_button.Enable()
            self.iview.UpDateHiderLabel(0)
        else:
            self.iview.ok_button.Disable()
            self.iview.UpDateHiderLabel(7)

        self.setStateComponentsStyle()

    def setStateComponentsStyle(self):
        if self.countItem == 0:
            self.disableStyles()
        else:
            self.enableStyles()

    def IsValidFile(self, path, name):
        #nombres no repetidos
        if  self.nameInDatetable(name):
            return nid_error

        #estilo correcto
        fpath = os.path.join(path, name)
        fvalid = self.CorrectStyleFormat(fpath)
        if fvalid != 0:
            return fvalid
        return correct

    def nameInDatetable(self, name):
        for row in range(self.countItem):
            if self.iview.dvlc.GetTextValue(row, 1) == name:
                return True
        return False

    def CorrectStyleFormat(self, path_file):
        style = self.iview.rb.GetSelection()
        return rm().fastVerificationStyle(path_file, style)

    def isValidAllFiles(self):
        not_error = self.iview.getLabelError(correct)
        for row in range(self.countItem):
            if self.iview.dvlc.GetTextValue(row, 3) != not_error:
                return False
        return  True

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

    def isAnyRowSelected(self):
        for row in range(self.countItem):
            if self.iview.dvlc.IsRowSelected(row):
                return True
        return False

    #----------------------------------------------------

    #---- Funciones que interactuan con el model de proyecto ----
    def GetNamesProject(self):
        return pro().getNamesProject()

    def GetNamesHideProject(self):
        return pro().getNamesHideProject()
    #----------------------------------------------------

    #---- cerrar dialogo ------------------------------------
    def ExitDialog(self):
        self.iview.Close()
    #----------------------------------------------------


class RenameProjectDialogPresenter():
    def __init__(self, iview):
        self.iview = iview
        self.listNamesProject = self.GetNamesProject()
        self.listNamesHideProject = self.GetNamesHideProject()

    def IsValidName(self, name, previus_name):

        self.iview.ok_button.Disable()

        if len(name.strip(' ')) == 0:
            self.iview.ConfigEmptyNameProject()
            return False
        if '/' in name:
            self.iview.ConfigNameProjectWithSlash()
            return False
        if name[0] == '.':
            self.iview.ConfigNameProjectStartWithPoint()
            return False
        if len(name.strip(' ')) == 0:
            self.iview.ConfigEmptyNameProject()
            return False
        if len(name.strip(' ')) > 100:
            self.iview.ConfigNameProjectInvalidLength()
            return False
        if name.strip(' ') in self.listNamesProject and name != previus_name:
            self.iview.ConfigExistingProject()
            return False
        if name in self.listNamesHideProject:
            self.iview.ConfigExistingHideProject()
            return False

        #correct name
        self.iview.ok_button.Enable()
        self.iview.ConfigEnableLabel()
        return True

    def UpdateName(self, new_name):
        if self.iview.previous_name != new_name.strip(' '):
            self.iview.project.name = new_name.strip(' ')
            project = pro().upDate(self.iview.project)
            pub.sendMessage(T.PROJECT_RENAME_UP, project)
        self.iview.Close(True)

    def GetNamesProject(self):
        return pro().getNamesProject()

    def GetNamesHideProject(self):
        return pro().getNamesHideProject()


class DeleteProjectDialogPresenter():
    def __init__(self, iview):
        self.iview = iview

    def DeleteProject(self):
        pub.sendMessage(T.PROJECT_DELETE_OK)


class CheckListCtrlPresenter():
    def __init__(self, iview):
        self.iview = iview

    def OnClickCheckbox(self):
        return pub.sendMessage(T.PROJECT_CLICKCHECKBOXLIST)


class UnHideProjectDialogPresenter():
    def __init__(self, iview):
        self.iview = iview
        pub.subscribe(self.ClickCheckboxPub, T.PROJECT_CLICKCHECKBOXLIST)

    def GetHideProjects(self):
        hidden = pro().getHideProject()
#         print hidden
        if [] == hidden:
            self.iview.IsEmptyList()
            return

        for project in hidden:
            self.iview.AddItemToList(project.name, str(project.creation_date))

    def ClickCheckboxPub(self, message):
        self.iview.apply_change_btn.Enable(False)
        num = self.iview.list.GetItemCount()
        for i in range(num):
            if self.iview.list.IsChecked(i):
                self.iview.apply_change_btn.Enable(True)

    def ExitDialog(self):
        pub.unsubscribe(self.ClickCheckboxPub, T.PROJECT_CLICKCHECKBOXLIST)
        self.iview.Close()

    def Restore(self):
        list_checked = []
        num = self.iview.list.GetItemCount()
        for i in range(num):
            if self.iview.list.IsChecked(i):
                name_project = self.iview.list.GetItemText(i)
                list_checked.append(name_project)
                project = pro().getProjectForName(name_project)
                project.state = OPEN
                pro().upDate(project)

        pub.sendMessage(T.PROJECT_LISTRESTORE, tuple(list_checked))
        self.ExitDialog()

    def SelectAll(self):
        num = self.iview.list.GetItemCount()
        for i in range(num):
            self.iview.list.CheckItem(i)

    def DeselectAll(self):
        num = self.iview.list.GetItemCount()
        for i in range(num):
            self.iview.list.CheckItem(i, False)
            self.iview.list.GetItem
