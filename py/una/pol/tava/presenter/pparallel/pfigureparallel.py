#  -*- coding: utf-8 -*-
'''
Created on 5/5/2015

@author: abrahan
'''
from py.una.pol.tava.base import tavac as tvc
from py.una.pol.tava.model.mparallel_analizer import\
    ParallelAnalizerModel as pam


# ------------------- Clase Presentador de Figura Coordenadas Paralelas  ------
# -------------------                                  ------------------------
class ParallelFigurePresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        self.figure_axes = None
        self.title_g = ''
        self.ite_list = []

        self.Init()

    def Init(self):

        pa = self.__getPA()
        colors = pa.colors_backgrounds.split(',')
        self.setBackGround(colors[1], colors[2])

    # ---- Metodos usados No Localmente -----------
    # ---                               -----------
    def newFigure(self, ite_list):
        self.ite_list = ite_list
        self.newFigureTest(self.ite_list)

    def newFigureTest(self, ite_list, suptitle=''):
        pa = self.__getPA()
        self.color_g = (pa.color_lines,)
        self.legend_g = pa.legent
        self.__cleanParallelFigure()
        suptitle = self.title_g
        self.figure_axes = self._initFigurePaint(ite_list, suptitle)

    def getParalelAnalizer(self):
        return self.__getPA()

    # ---- Metodos usados Localmente -----------
    # ---                            -----------

    def __getPA(self):
        return pam().getParallelAnalizerByIdTest(self.test.id)

    def setBackGround(self, color_one, color_to):
        self.iview.figure.set_facecolor(color_one)
        self.iview.SetBackgroundColour(color_to)
        self.iview.toolbar.SetBackgroundColour(color_to)
        self.iview.canvas.draw()

    def __cleanParallelFigure(self):
        if not(self.figure_axes is None):
            self.iview.figure.delaxes(self.iview.figure.gca())

    def _initFigurePaint(self, ite_list, suptitle='', sp_axe=None):
        axe = None
        if sp_axe is None:
            axe = self.iview.figure.gca()
        else:
            axe = self.iview.figure.add_subplot(sp_axe)
        self.iview.figure.suptitle(suptitle)
        axe = self._figurePaint(axe, ite_list)
        return axe

    def _figurePaint(self, axe, ite_list, count_last=0):
        _pos = 0 + count_last
        _len = len(ite_list) + count_last
        for iteration in ite_list:
            axe = pam().getParallelAxe(iteration, _len, _pos, axe,
                                       self.legend_g, self.color_g)
            pa = self.__getPA()
            axe = self._setAddConfigGrip(axe, pa.figure_grid)

            self.iview.canvas.draw()
            _pos += 1
        self.iview.canvas.draw()
        return axe
    # --------------------------------------------------------------------------

    def _setAddConfigGrip(self, axe, figure_grid):
        fg = figure_grid
        if fg.grid:
            o_axis = tvc.ORIENTATION_LINE_AL[fg.orientation]
            s_linestyle = tvc.STYLE_LINE_AL[fg.red_style]
            axe.grid(b=True,  which='major', axis=o_axis,
                     color=fg.red_color, linestyle=s_linestyle,
                     linewidth=fg.red_width)
        else:
            axe.grid(fg.grid)
        return axe

    def containsFilter(self):
        pa = self.__getPA()
        return not (pa.maxs_objetive is None or pa.mins_objetive is None)
