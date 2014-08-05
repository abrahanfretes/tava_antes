'''
Created on 05/08/2014

@author: aferreira
'''
from wx.lib.pubsub import Publisher as pub
import topic as T
import py.una.pol.tava.view.vi18n as C
from wx import GetTranslation as _


class MainMenuBarPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.OnUpdateLabels, T.LANGUAGE_CHANGED)

    def OnSelectEnglishLanguage(self):
        pub.sendMessage(T.ENGLISH_SELECTED)

    def OnSelectSpanishLanguage(self):
        pub.sendMessage(T.SPANISH_SELECTED)

    def OnUpdateLabels(self, message):
        self.iview.new_project_menu_item.SetText(_(C.MMB_NP))
        self.iview.open_menu_item.SetText(_(C.MMB_OP))
        self.iview.exit_menu_item.SetText(_(C.MMB_EXIT))
        self.iview.english_language_menu_item.SetText(_(C.MMB_EN_US_LA))
        self.iview.spanish_language_menu_item.SetText(_(C.MMB_ES_PY_LA))
        self.iview.about_menu_item.SetText(_(C.MMB_ABOUT_TAVA))
        self.iview.SetMenuLabel(0, _(C.MMB_FILE))
        self.iview.SetMenuLabel(1, _(C.MMB_LANGUAGE))
        self.iview.SetMenuLabel(2, _(C.MMB_HELP))
