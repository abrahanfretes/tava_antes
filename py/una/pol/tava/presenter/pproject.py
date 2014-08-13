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

    def GetNamesProject(self):
        return pro().getNamesProject()

    def OnNew(self, name):
        project = pro().add(name)
        pub.sendMessage(T.PROJECT_NEW, project)

    def IsNameValido(self, name):

        self.iview.ok_button.Disable()

        if len(name) == 0:
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
        if len(name) > 100:
            self.iview.ConfigInvalidLenProjectName()
            return False
        if name in self.listNamesProject:
            self.iview.ConfigExistingProject()
            return False

        #nombre correcto
        self.iview.ok_button.Enable()
        self.iview.ConfigEnableLabel()
        return True


class RenameProjectDialogPresenter():
    def __init__(self, iview):
        self.iview = iview
        self.listNamesProject = self.GetNamesProject()

    def IsNameValido(self, name):
        return name not in self.listNamesProject and bool(name)

    def OnUpDateName(self, new_name, project):
        project.name = new_name
        project = pro().upDate(project)
        pub.sendMessage(T.PROJECT_RENAME_UP, project)

    def GetNamesProject(self):
        return pro().getNamesProject()


class DeleteProjectDialogPresenter():
    def __init__(self, iview):
        self.iview = iview

    def OnDeleteOk(self):
        pub.sendMessage(T.PROJECT_DELETE_OK)
