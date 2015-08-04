#  -*- coding: utf-8 -*-
'''
Created on 24/6/2015

@author: abrahan
'''

import numpy as np
import scipy.stats as st
from pandas import DataFrame

from py.una.pol.tava.model.mmetric import MetricModel as mm


class StatisticSingPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        self.figure_axes = None
        self.title_g = ''
        self.ite_list = []

    def initFigure(self, problem, objective, evolutionary, thread, parallel,
                   metric, population, iteration, evo_selected):

        result = {}
        win = 0
        loss = 0
        tie = 0
        p_ = []

        valores_reales = []
        values_pivot = mm().getValueMetrics(population.id)
        cabeceras_reales = [str(i) for i in range(len(values_pivot))]

        for e_method in evo_selected:
            values_other = mm().\
                getValueMetricsByEvolutionaryMethod(e_method,
                                                    thread.value,
                                                    parallel.name,
                                                    metric.name,
                                                    population.value)

            valores_reales_aux = []
            for i in range(len(values_pivot)):
                pivot = values_pivot[i]
                other = values_other[i]
                if pivot > other:
                    win += 1
                elif pivot < other:
                    loss += 1
                else:
                    tie += 1

                valores_reales_aux.append(other.value)

            valores_reales.append(valores_reales_aux)

            if tie > 1:
                win += int(tie/2)
                loss += int(tie/2)
            diff = np.round_(st.binom_test(win, len(values_pivot), 0.5), 2)
            p_.append(diff)

            result[e_method.name] = (str(win), str(loss), str(diff))
            win = 0
            loss = 0
            tie = 0

        labelc = [evolutionary.name]
        char_w = ['Wins (+)']
        char_l = ['Loses (-)']
        char_t = ['Differences']
        for key in result.keys():
            var_t = result[key]
            labelc.append(key)
            char_w.append(var_t[0])
            char_l.append(var_t[1])
            char_t.append(var_t[2])

        for name in labelc:
            self.iview.t_table.AppendTextColumn(name)

        self.iview.t_table.AppendItem(char_w)
        self.iview.t_table.AppendItem(char_l)
        self.iview.t_table.AppendItem(char_t)

        axe = self.iview.figure.gca()
        df = DataFrame(valores_reales, columns=cabeceras_reales)
        df.plot(kind='box', ax=axe, table=False)
        self.iview.canvas.draw()
        return axe
