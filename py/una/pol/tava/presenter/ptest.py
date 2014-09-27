'''
Created on 21/09/2014

@author: arsenioferreira
'''
from py.una.pol.tava.model.mresult import ResultModel as rm


class GraphicWizardPresenter():
    def __init__(self, iview):
        self.iview = iview


class WizardFirstPagePresenter():
    def __init__(self, iview):
        self.iview = iview

    def GetListItems(self):
        return rm().getNamesResultForProject(self.iview.GetParent().project)
