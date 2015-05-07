#  -*- coding: utf-8 -*-
'''
Created on 5/5/2015

@author: abrahan
'''

from wx.lib.pubsub import Publisher as pub

from py.una.pol.tava.presenter import topic as T
from py.una.pol.tava.model.mparallel_analizer import\
    ParallelAnalizerModel as pam


class ParallelConfigPresenter:
    def __init__(self, iview, pa):
        self.iview = iview
        self.pa = pa
        self.setLessValue(pa)

    def setApplyConfig(self):

        pa_aux = pam().getParallelAnalizerById(self.pa.id)

        # TabBackGroung
        update_backcolor = False
        back_color = self.iview.tab_backGround.getValuesTab()
        if pa_aux.colors_backgrounds != back_color:
            pa_aux.colors_backgrounds = back_color
            self._setViewsBackGroung(back_color)
            pa_aux = pam().upDate(pa_aux)
            update_backcolor = True

        # TabFigureGrip
        update_grip = False
        list_arg = self.iview.tab_figure_grid.getValuesTab()
        fg = pa_aux.figure_grid
        if(list_arg[0] != fg.grid):
            pa_aux.figure_grid.grid = list_arg[0]
            update_grip = True
        if list_arg[0]:
            if(list_arg[1] != fg.orientation):
                pa_aux.figure_grid.orientation = list_arg[1]
                update_grip = True
            if(list_arg[2] != fg.red_color):
                pa_aux.figure_grid.red_color = list_arg[2]
                update_grip = True
            if(list_arg[3] != fg.red_width):
                pa_aux.figure_grid.red_width = list_arg[3]
                update_grip = True
            if(list_arg[4] != fg.red_style):
                pa_aux.figure_grid.red_style = list_arg[4]
                update_grip = True

        color_legend = False
        if(list_arg[5] != pa_aux.color_lines):
            pa_aux.color_lines = list_arg[5]
            color_legend = True
        if(list_arg[6] != pa_aux.legent):
            pa_aux.legent = list_arg[6]
            color_legend = True

        # Orden de objetivos
        sort_name = self.iview.tab_sort_objetive.getValuesTab()
        sort_true = False

        # Seleccción de objetivos, habilitados para mostrar
        enables = self.iview.tab_selected_obj.getValuesTab()
        enable_true = False
        if pa_aux.enable_objectives != enables[0]:
            pa_aux.enable_objectives = enables[0]
            pa_aux.order_objective = enables[1]
            pa_aux.order_name_obj = enables[2]
            self.iview.tab_sort_objetive.updateDate(pa_aux)
            enable_true = True
        elif pa_aux.order_name_obj != sort_name[0]:
            pa_aux.order_name_obj = sort_name[0]
            pa_aux.order_objective = sort_name[1]
            self.iview.tab_sort_objetive.updateDate(pa_aux)
            sort_true = True

        # Verificación de nuevos nombres para objetivos
        new_names_obj = False
        names_objs = self.iview.tab_rename.getValuesTab()
        if self.isNewNames(names_objs):
            # modifico el order_name_obj
            new_names = pa_aux.order_name_obj.split(',')
            for index in range(len(new_names)):
                if names_objs[index] != '':
                    new_names[index] = names_objs[index]
            pa_aux.order_name_obj = ','.join(new_names)

            # modifico el name_objetive
            new_names_ = pa_aux.name_objetive.split(',')
            index_name = [int(i) for i in pa_aux.order_objective.split(',')]
            for i in range(len(new_names)):
                new_names_[index_name[i]] = new_names[i]
            pa_aux.name_objetive = ','.join(new_names_)
            new_names_obj = True
            self.iview.tab_rename.updateRename(pa_aux)

        # Verificación de nuevos nombres para variables
        new_names_var = False
        names_variables = self.iview.tab_rename_var.getValuesTab()
        if self.isNewNames(names_variables):
            new_names = pa_aux.name_variable.split(',')
            for index in range(len(new_names)):
                if names_variables[index] != '':
                    new_names[index] = names_variables[index]
            pa_aux.name_variable = ','.join(new_names)
            new_names_var = True
            self.iview.tab_rename_var.updateRenameVar(pa_aux)

        if sort_true or enable_true or new_names_obj or new_names_var or color_legend:
            pa_aux = pam().upDate(pa_aux)
            return [True, update_backcolor]
        if update_grip or update_backcolor:
            pa_aux = pam().upDate(pa_aux)
            return [False, True]
        return [False, False]

    def setCancel(self):
        update_backcolor = False
        if self.pa.colors_backgrounds != self.less_colors_backgrounds:
            update_backcolor = True

        if self.isChangeSomeValue():
            self.pa = pam().upDate(self.getLessValue(self.pa))
            return [True, update_backcolor]
        return [False, update_backcolor]

    def setSave(self):
        return self.setApplyConfig()

    def _setViewsBackGroung(self, backColor):
        self.iview.setBackGroundLB(backColor.split(',')[2])

    def setLessValue(self, pa):

        self.less_name_objetive = pa.name_objetive
        self.less_name_variable = pa.name_variable

        self.less_enable_objectives = pa.enable_objectives
        self.less_order_objective = pa.order_objective

        self.less_order_name_obj = pa.order_name_obj
        self.less_order_objective = pa.order_objective

        self.less_legent = pa.legent
        self.less_color_lines = pa.color_lines
        self.less_grid = pa.figure_grid.grid
        self.less_orientation = pa.figure_grid.orientation
        self.less_red_color = pa.figure_grid.red_color
        self.less_red_width = pa.figure_grid.red_width
        self.less_red_style = pa.figure_grid.red_style

        self.less_colors_backgrounds = pa.colors_backgrounds

    def getLessValue(self, pa):

        pa.name_objetive = self.less_name_objetive
        pa.name_variable = self.less_name_variable

        pa.enable_objectives = self.less_enable_objectives
        pa.order_objective = self.less_order_objective

        pa.order_name_obj = self.less_order_name_obj
        pa.order_objective = self.less_order_objective

        pa.legent = self.less_legent
        pa.color_lines = self.less_color_lines
        pa.figure_grid.grid = self.less_grid
        pa.figure_grid.orientation = self.less_orientation
        pa.figure_grid.red_color = self.less_red_color
        pa.figure_grid.red_width = self.less_red_width
        pa.figure_grid.red_style = self.less_red_style

        pa.colors_backgrounds = self.less_colors_backgrounds
        return pa

    def isChangeSomeValue(self):

        if self.less_name_objetive != self.pa.name_objetive:
            return True
        elif self.less_name_variable != self.pa.name_variable:
            return True
        elif self.less_enable_objectives != self.pa.enable_objectives:
            return True
        elif self.less_order_objective != self.pa.order_objective:
            return True

        elif self.less_order_name_obj != self.pa.order_name_obj:
            return True
        elif self.less_order_objective != self.pa.order_objective:
            return True

        elif self.pa.legent != self.less_legent:
            return True

        elif self.pa.color_lines != self.less_color_lines:
            return True
        elif self.pa.figure_grid.grid != self.less_grid:
            return True
        elif self.pa.figure_grid.orientation != self.less_orientation:
            return True
        elif self.pa.figure_grid.red_color != self.less_red_color:
            return True
        elif self.pa.figure_grid.red_width != self.less_red_width:
            return True
        elif self.pa.figure_grid.red_style != self.less_red_style:
            return True
        return False

    def isNewNames(self, news_names):
        for name in news_names:
            if name != '':
                return True
        return False
