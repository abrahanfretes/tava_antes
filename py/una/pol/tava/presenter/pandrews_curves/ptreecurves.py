#  -*- coding: utf-8 -*-
'''
Created on 2/5/2015

@author: abrahan
'''
import wx
from py.una.pol.tava.model.mcurves import AndrewsCurvesModel as acm


class CurvesTreePresenter:
    def __init__(self, iview, test):

        self.iview = iview
        self.old_item = None
        self.current_item = None

        self.InitUI(test)

        #  Inicializacion del arbol de proyectos
    def InitUI(self, test):
        ac = acm().getCurvesByTestId(test.id)
        self.__setBackGround(ac.colors_backgrounds)

        for_tree = acm().getFormatTree(test)

        # inicializamos el arbol
        for r_name in for_tree.keys():
            td_item = self.iview.AppendItem(self.iview.root, r_name)
            self.iview.SetItemPyData(td_item, '')
            self.iview.SetItemImage(td_item, 0, wx.TreeItemIcon_Normal)

            for ite_data in for_tree[r_name]:
                tda_item = self.iview.AppendItem(td_item, ite_data[0])
                self.iview.SetItemPyData(tda_item, ite_data[1])
                self.iview.CheckItem(tda_item, False)
                self.iview.SetItemImage(tda_item, 2)

        # ordenamos el arbol
        self.iview.SortChildren(self.iview.root)
        # expandimos el arbol
        for item in self.iview.root.GetChildren():
            self.iview.Expand(item)

    # ---- Metodos usados No Localmente -----------
    # ---                               -----------

    def isValidItem(self):
        if self.old_item is None or self.old_item != self.current_item:
            return True
        return False

    # ---- Metodos usados Localmente -----------
    # ---                            -----------

    def __setBackGround(self, backColor):
        self.iview.SetBackgroundColour(backColor.split(',')[0])
