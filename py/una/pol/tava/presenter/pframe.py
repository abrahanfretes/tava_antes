'''
Created on 04/08/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
import topic as T


class FramePresenter:
    def __init__(self, iview):
        self.iview = iview
        #verificar luego si esta correcto
        self.project_selected = None

        pub.subscribe(self.ShowNewProjectDialogPub, T.BAR_PROJECT_NEW)
        pub.subscribe(self.ShowRenameProjectDialogPub, T.PROJECT_RENAME)
        pub.subscribe(self.ShowDeleteProjectDialogPub, T.PROJECT_DELETE_SELECT)
        pub.subscribe(self.ShowProjectProperties, T.PROJECT_PROPERTIES)
        pub.subscribe(self.EnglishLanguageSelected, T.ENGLISH_SELECTED)
        pub.subscribe(self.SpanishLanguageSelected, T.SPANISH_SELECTED)
        pub.subscribe(self.ProjectSelected, T.PROJECT_SELECTED)
        pub.subscribe(self.UnHideProjectPub, T.PROJECT_UNHIDE)
        pub.subscribe(self.AddFileInProjectPub, T.PROJECT_ADDFILE)
        pub.subscribe(self.ShowGraphicWizard, T.GRAPHIC_WIZARD)

    def ShowNewProjectDialogPub(self, message):
        self.iview.ShowNewProjectDialog()

    def ShowRenameProjectDialogPub(self, message):
        self.iview.ShowRenameProjectDialog(message.data)

    def ShowDeleteProjectDialogPub(self, message):
        self.iview.ShowDeleteProjectDialog()

    def ShowProjectProperties(self, message):
        if self.project_selected is not None:
            self.iview.ShowProjectProperties(self.project_selected)

    def EnglishLanguageSelected(self, message):
        self.iview.i18n.EnglishLanguageSelected()
        pub.sendMessage(T.LANGUAGE_CHANGED)

    def SpanishLanguageSelected(self, message):
        self.iview.i18n.SpanishLanguageSelected()
        pub.sendMessage(T.LANGUAGE_CHANGED)

    def ProjectSelected(self, message):
        self.project_selected = message.data

    def UnHideProjectPub(self, message):
        self.iview.ShowUnHideProjectDialog()

    def AddFileInProjectPub(self, message):
        self.iview.ShowAddFileInProjectDialog(message.data)

    def ShowGraphicWizard(self, message):
        if self.project_selected is not None:
            self.iview.ShowGraphicWizard(self.project_selected)
