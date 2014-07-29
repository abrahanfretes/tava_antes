'''
Created on 29/07/2014

@author: afretes
'''
from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.model.mproject import ProjectModel


class ProjectMenuPresenter:
    def __init__(self, iview):
        self.iview = iview

    def OnDelete(self, project, item):
        ProjectModel().delete(project)
        pub.sendMessage('PROJECT.DELETE', item)
