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
        pub.subscribe(self.HideProjectPub, 'PROJECT.HIDE')
        pub.subscribe(self.UnHideProjectPub, 'PROJECT.UNHIDE')

    def OnNewProjectBarPub(self, message):
        self.iview.OnBarNewProject()

    def OnRenameProjectPub(self, message):
        self.iview.OnRenameProject(message)

    def OnDeleteSelectProjectPub(self, message):
        self.iview.OnDeleteSelectedProject(message)

    def ShowProjectProperties(self, message):
        if self.project_selected is not None:
            self.iview.OnShowProjectProperties(self.project_selected)

    def EnglishLanguageSelected(self, message):
        self.iview.i18n.EnglishLanguageSelected()
        pub.sendMessage(t.LANGUAGE_CHANGED)

    def SpanishLanguageSelected(self, message):
        self.iview.i18n.SpanishLanguageSelected()
        pub.sendMessage(t.LANGUAGE_CHANGED)

    def ProjectSelected(self, message):
        self.project_selected = message.data

    def HideProjectPub(self, message):
        self.iview.OnHideProject(message)

    def UnHideProjectPub(self, message):
        self.iview.UnHideProject(message)
