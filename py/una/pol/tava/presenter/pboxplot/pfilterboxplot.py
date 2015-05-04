#  -*- coding: utf-8 -*-
'''
Created on 3/5/2015

@author: abrahan
'''
from py.una.pol.tava.model.mboxplot import BoxPlotModel as bpm


class BoxPlotFilterPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        self.InitUI()

    def InitUI(self):

        # inicialización para valores de variables
        bp = bpm().getBoxPlotByTestId(self.test.id)
        v_names = bp.name_variable
        columns = v_names.split(',')
        self.countColumn = len(columns)
        self.iview.var.AppendTextColumn('key', width=50)
        for name in columns:
            self.iview.var.AppendTextColumn(name, width=110)

        # inicialización para valores de objetivos
        o_names = bp.order_name_obj
        columns = o_names.split(',')
        self.countColumn = len(columns)
        self.iview.obj.AppendTextColumn('key', width=50)
        for name in columns:
            self.iview.obj.AppendTextColumn(name, width=150)

    def updateValuesList(self, ite_list):
        ite = ite_list[0]
        self.iview.deltePages()

        self.iview.InitUI()
        self.InitUI()

        # actualizacion de variables
        for var in bpm().getListVariables(ite):
            self.iview.var.AppendItem(var)

        # actualizacion de objetivos
        for obj in bpm().getListObjectives(ite):
            self.iview.obj.AppendItem(obj)

        # actualizacion de Objetivos
        # filtro las variables correspondientes
        vmin, vmax = bpm().getMinMaxObjective(ite)

        # obtengo los nombres
        bp = bpm().getBoxPlotByTestId(self.test.id)
        names = bp.order_name_obj.split(',')

        # creo los filtros
        self.values = []

        if len(names) == len(vmin):
            for index in range(len(names)):
                value = self.iview.addItemFil(vmin[index], vmax[index],
                                              names[index], vmin[index],
                                              vmax[index])
                self.values.append(value)
        # actualizo la vista
        self.iview.addSiserHere()
        self.updateBeforeValues()

    def updateBeforeValues(self):
        self.min_before = []
        self.max_before = []
        for value in self.values:
            self.min_before.append(value.getMinValue())
            self.max_before.append(value.getMaxValue())

    def isFilterModified(self):

        for index in range(len(self.values)):
            if self.values[index].getMinValue() != self.min_before[index]:
                return True
            if self.values[index].getMaxValue() != self.max_before[index]:
                return True
        return False

    def getListValues(self):

        max_list = []
        min_list = []
        for fil in self.values:
            max_list.append(str(fil.getMaxValue()))
            min_list.append(str(fil.getMinValue()))
        return ','.join(max_list), ','.join(min_list)
