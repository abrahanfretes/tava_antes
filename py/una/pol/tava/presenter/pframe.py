'''
Created on 04/08/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
import topic as t


class FramePresenter:
    def __init__(self, iview):
        self.iview = iview
        self.project_selected = None

        pub.subscribe(self.OnNewProjectBarPub, t.BAR_PROJECT_NEW)
        pub.subscribe(self.OnRenameProjectPub, t.PROJECT_RENAME)
        pub.subscribe(self.OnDeleteSelectProjectPub, t.PROJECT_DELETE_SELECT)
        pub.subscribe(self.ShowProjectProperties, t.PROJECT_PROPERTIES)
        pub.subscribe(self.EnglishLanguageSelected, t.ENGLISH_SELECTED)
        pub.subscribe(self.SpanishLanguageSelected, t.SPANISH_SELECTED)
        pub.subscribe(self.ProjectSelected, t.PROJECT_SELECTED)
        pub.subscribe(self.UnHideProjectPub, 'PROJECT.UNHIDE')

    def OnNewProjectBarPub(self, message):
        self.iview.ShowNewProjectDialog()

    def OnRenameProjectPub(self, message):
        self.iview.ShowRenameProjectDialog(message.data)

    def OnDeleteSelectProjectPub(self, message):
        self.iview.ShowDeleteProjectDialog()

    def ShowProjectProperties(self, message):
        if self.project_selected is not None:
            self.iview.ShowProjectProperties(self.project_selected)

    def EnglishLanguageSelected(self, message):
        self.iview.i18n.EnglishLanguageSelected()
        pub.sendMessage(t.LANGUAGE_CHANGED)

    def SpanishLanguageSelected(self, message):
        self.iview.i18n.SpanishLanguageSelected()
        pub.sendMessage(t.LANGUAGE_CHANGED)

    def ProjectSelected(self, message):
        self.project_selected = message.data

    def UnHideProjectPub(self, message):
        self.iview.ShowUnHideProjectDialog()
