'''
Created on 29/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.base.entity import OPEN
from py.una.pol.tava.base.entity import CLOSED


class ToolBarPresenter:
    def __init__(self, iview):
        self.iview = iview

        self.project_selected = None
        self.item_selected = None
        pub.subscribe(self.OnDisablePub, 'PROJECT.SELECTED')

        pub.subscribe(self.OnDisableIcomProjectAllPub, 'PROJECT.CLOSED')
        pub.subscribe(self.OnDisableIcomProjectAllPub, 'PROJECT.OPEN')
        pub.subscribe(self.OnDisableIcomProjectAllPub, 'PROJECT.DELETE')

    def OnDisableIcomProjectAll(self):
        self.iview.OnAllDisable()

    def OnCloseProject(self):
        pub.sendMessage('PROJECT.CLOSED',
                        (self.project_selected, self.item_selected))

    def OnNewProject(self):
        pub.sendMessage('BAR.PROJECT.NEW', 'NEWPROJECT')

    def OnOpenProject(self):
        pub.sendMessage('PROJECT.OPEN',
                        (self.project_selected, self.item_selected))

    def OnDeleteProject(self):
        pub.sendMessage('PROJECT.DELETE',
                        (self.project_selected, self.item_selected))

    def OnDisablePub(self, message):

        project_item = message.data
        self.project_selected = project_item[0]
        self.item_selected = project_item[1]

        if self.project_selected.state == OPEN:
            self.iview.OnOpenDisable()

        if self.project_selected.state == CLOSED:
            self.iview.OnCloseDisable()

    def OnDisableIcomProjectAllPub(self, message):
        self.OnDisableIcomProjectAll()
