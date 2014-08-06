'''
Created on 29/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
import topic as T
import py.una.pol.tava.view.vi18n as C
from wx import GetTranslation as _


class ToolBarPresenter:
    def __init__(self, iview):
        self.iview = iview

        pub.subscribe(self.OnDisableOpenPub, T.PROJECT_SELECTED_OPEN)
        pub.subscribe(self.OnDisableClosePub, T.PROJECT_SELECTED_CLOSE)

        pub.subscribe(self.OnDisableIcomProjectAllPub, T.PROJECT_CLOSE)
        pub.subscribe(self.OnDisableIcomProjectAllPub, T.PROJECT_OPEN)
        pub.subscribe(self.OnDisableIcomProjectAllPub, T.PROJECT_DELETE)
        pub.subscribe(self.OnUpdateLabels, T.LANGUAGE_CHANGED)

    def OnDisableIcomProjectAll(self):
        self.iview.OnAllDisable()

    def OnCloseProjectSend(self):
        pub.sendMessage(T.PROJECT_CLOSE)

    def OnNewProject(self):
        pub.sendMessage(T.BAR_PROJECT_NEW)

    def OnOpenProject(self):
        pub.sendMessage(T.PROJECT_OPEN)

    def OnDeleteProject(self):
        pub.sendMessage(T.PROJECT_DELETE_CLICK)

    def OnDisableOpenPub(self, message):
        self.iview.OnOpenDisable()

    def OnDisableClosePub(self, message):
        self.iview.OnCloseDisable()

    def OnDisableIcomProjectAllPub(self, message):
        self.OnDisableIcomProjectAll()

    def OnUpdateLabels(self, message):
        self.iview.SetToolShortHelp(self.iview.ID_NEW_PRO, _(C.MTB_NP))
        self.iview.SetToolShortHelp(self.iview.ID_OPEN_PRO, _(C.MTB_OP))
        self.iview.SetToolShortHelp(self.iview.ID_CLOSE_PRO, _(C.MTB_CP))
        self.iview.SetToolShortHelp(self.iview.ID_DEL_PRO, _(C.MTB_DP))
        self.iview.SetToolShortHelp(self.iview.ID_BLOG_PRO, _(C.MTB_BP))
        self.iview.SetToolShortHelp(self.iview.ID_EXIT_PRO, _(C.MTB_EX))
