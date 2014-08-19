'''
Created on 28/07/2014

@author: afretes
'''
from py.una.pol.tava.model.mproject import ProjectModel as pro
from wx.lib.pubsub import Publisher as pub
import topic as T


class NewProjectDialogPresenter():
    def __init__(self, iview):
        self.iview = iview
        self.listNamesProject = self.GetNamesProject()
        self.listNamesHideProject = self.GetNamesHideProject()

    def GetNamesProject(self):
        return pro().getNamesProject()

    def GetNamesHideProject(self):
        return pro().getNamesHideProject()

    def CreateProject(self, name):
        project = pro().add(name.strip(' '))
        pub.sendMessage(T.PROJECT_NEW, project)
        self.iview.Close(True)

    def IsNameValido(self, name):

        self.iview.ok_button.Disable()

        if len(name.strip(' ')) == 0:
            self.iview.ConfigProjectNameEmpty()
            return False
        if '/' in name:
            self.iview.ConfigSlashProjectName()
            return False
        if name[0] == '.':
            self.iview.ConfigInitPointProjectName()
            return False
        if len(name.strip(' ')) == 0:
            self.iview.ConfigProjectNameEmpty()
            return False
        if len(name.strip(' ')) > 100:
            self.iview.ConfigInvalidLenProjectName()
            return False
        if name in self.listNamesProject:
            self.iview.ConfigExistingProject()
            return False
        if name in self.listNamesHideProject:
            self.iview.ConfigExistingHideProject()
            return False

        #correct name
        self.iview.ok_button.Enable()
        self.iview.ConfigEnableLabel()
        return True


class RenameProjectDialogPresenter():
    def __init__(self, iview):
        self.iview = iview
        self.listNamesProject = self.GetNamesProject()
        self.listNamesHideProject = self.GetNamesHideProject()

    def IsNameValido(self, name, previus_name):

        self.iview.ok_button.Disable()

        if len(name.strip(' ')) == 0:
            self.iview.ConfigProjectNameEmpty()
            return False
        if '/' in name:
            self.iview.ConfigSlashProjectName()
            return False
        if name[0] == '.':
            self.iview.ConfigInitPointProjectName()
            return False
        if len(name.strip(' ')) == 0:
            self.iview.ConfigProjectNameEmpty()
            return False
        if len(name.strip(' ')) > 100:
            self.iview.ConfigInvalidLenProjectName()
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

    def OnUpDateName(self, new_name):
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

    def OnDeleteOk(self):
        pub.sendMessage(T.PROJECT_DELETE_OK)


class CheckListCtrlPresenter():
    def __init__(self, iview):
        self.iview = iview

    def OnClickCheckbox(self):
        return pub.sendMessage('PROJECT.CLICKCHECKBOXLIST')


class UnHideProjectDialogPresenter():
    def __init__(self, iview):
        self.iview = iview
        pub.subscribe(self.ClickCheckboxPub, 'PROJECT.CLICKCHECKBOXLIST')

    def GetHideProject(self):
        return pro().getHideProject()

    def ClickCheckboxPub(self, message):
        self.iview.apply_change.Enable(False)
        num = self.iview.list.GetItemCount()
        for i in range(num):
            if self.iview.list.IsChecked(i):
                self.iview.apply_change.Enable(True)

    def ExitDialog(self):
        pub.unsubscribe(self.ClickCheckboxPub, 'PROJECT.CLICKCHECKBOXLIST')
        self.iview.Close()

    def Restore(self):

        num = self.iview.list.GetItemCount()
        for i in range(num):
            if self.iview.list.IsChecked(i):
                print self.iview.list.GetItemText(i)
                print self.iview.list.Get

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
