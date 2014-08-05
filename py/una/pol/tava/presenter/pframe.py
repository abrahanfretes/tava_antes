'''
Created on 04/08/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
import topic as t


class FramePresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.OnNewProjectBarPub, t.BAR_PROJECT_NEW)
        pub.subscribe(self.OnRenameProjectPub, t.PROJECT_RENAME)
        pub.subscribe(self.EnglishLanguageSelected, t.ENGLISH_SELECTED)
        pub.subscribe(self.SpanishLanguageSelected, t.SPANISH_SELECTED)

    def OnNewProjectBarPub(self, message):
        self.iview.OnBarNewProject()

    def OnRenameProjectPub(self, message):
        self.iview.OnRenameProject(message)

    def EnglishLanguageSelected(self, message):
        self.iview.i18n.EnglishLanguageSelected()
        pub.sendMessage(t.LANGUAGE_CHANGED)

    def SpanishLanguageSelected(self, message):
        self.iview.i18n.SpanishLanguageSelected()
        pub.sendMessage(t.LANGUAGE_CHANGED)
