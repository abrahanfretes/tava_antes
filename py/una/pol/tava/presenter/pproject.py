'''
Created on 28/07/2014

@author: afretes
'''
from py.una.pol.tava.model.mproject import ProjectModel as pro
from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.base.entity import OPEN
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

    def IsValidName(self, name):

        self.iview.ok_button.Disable()

        if len(name.strip(' ')) == 0:
            self.iview.ConfigEmptyNameProject()
            return False
        if '/' in name:
            self.iview.ConfigNameProjectWithSlash()
            return False
        if name[0] == '.':
            self.iview.ConfigNameProjectInvalidLength()
            return False
        if len(name.strip(' ')) == 0:
            self.iview.ConfigEmptyNameProject()
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
        print hidden
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
