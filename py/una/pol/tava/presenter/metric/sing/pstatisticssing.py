#  -*- coding: utf-8 -*-
'''
Created on 24/6/2015

@author: abrahan
'''

import numpy as np
import scipy.stats as st

from matplotlib.table import table
from matplotlib.font_manager import FontProperties

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

        values_pivot = mm().getValueMetrics(population.id)

        print evolutionary
        for e_method in evo_selected:

            print e_method.name
            values_other = mm().\
                getValueMetricsByEvolutionaryMethod(e_method,
                                                    thread.value,
                                                    parallel.name,
                                                    metric.name,
                                                    population.value)

            for i in range(len(values_pivot)):
                pivot = values_pivot[i]
                other = values_other[i]
                print str(pivot.iteration) + ' - ' + str(pivot.value) + '--' + str(other.iteration) + ' - ' + str(other.value)
                if pivot > other:
                    win += 1
                elif pivot < other:
                    loss += 1
                else:
                    tie += 1
            if tie > 1:
                win += int(tie/2)
                loss += int(tie/2)
            diff = np.round_(st.binom_test(win, len(values_pivot), 0.5), 2)
            p_.append(diff)

            result[e_method.name] = (str(win), str(loss), str(diff))
            win = 0
            loss = 0
            tie = 0

            print result

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

        chars = [char_w, char_l, char_t]

        colors = [[(0.95, 0.95, 0.95) for c in range(len(result.keys()) + 1)] for r in range(3)]
        colors[0][0] = '#FFE4C4'
        colors[1][0] = '#FFE4C4'
        colors[2][0] = '#FFE4C4'
        lightgrn = (0.5, 0.8, 0.5)
        lightgrns = [lightgrn]*16
        lightgrns[0] = (0.95, 0.95, 0.95)
        lightgrns[0] = '#DEB887'

        axe = self.iview.figure.gca()

        tab = axe.table(cellText=chars,
                        colLabels=labelc,
                        colColours=lightgrns,
                        cellColours=colors,
                        cellLoc='center',
                        loc='upper left')

        font_use = FontProperties(family='serif',
                                  style='normal',
                                  variant='normal',
                                  weight='medium',
                                  stretch='ultra-expanded',
                                  size='xx-large',
                                  fname=None)
        for key, cell in tab.get_celld().items():
            row, col = key
            if row > 0 and col > 0:
                cell.set_text_props(fontproperties=font_use)
                cell.set_fontsize(50)

        axe.axison = False
        self.iview.canvas.draw()
        return axe
