#  -*- coding: utf-8 -*-
'''
Created on 7/6/2015

@author: abrahan
'''
import wx
from py.una.pol.tava.view.com.tcombobox import TComboBox
from py.una.pol.tava.presenter.metric.pconfigmetric import\
    ConfigMetricPresenter


# ------------------- Arbol de Archvivos e Iteraciones ------------------------
# -------------------                                  ------------------------
class ConfigMetric(wx.Panel):
    def __init__(self, parent, page_main, page_figure, test):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.page_main = page_main
        self.page_figure = page_figure
        self.presenter = ConfigMetricPresenter(self, test)

        self.c_problem = TComboBox(self, 'Problema :', self.presenter.options_problems)
        self.c_objective = TComboBox(self, 'Numero Objetivo :', self.presenter.options_objectives)
        self.c_evolutionary = TComboBox(self, 'Metodo Evolutivo :', self.presenter.options_evolutionarys)
        self.c_thread = TComboBox(self, 'Numero de Hilos :', self.presenter.options_threads)
        self.c_parallel = TComboBox(self, 'Metodo Paralelo :', self.presenter.options_parallels)
        self.c_metric = TComboBox(self, 'Metrica :', self.presenter.options_metrics)
        self.c_population = TComboBox(self, 'Poblacion :', self.presenter.options_populations)
        self.c_iteration = TComboBox(self, 'Iteracion :', self.presenter.options_iterations)

        self.b_view = wx.Button(self, label='visualizar')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.c_problem, 0)
        sizer.Add(self.c_objective, 0)
        sizer.Add(self.c_evolutionary, 0)
        sizer.Add(self.c_thread, 0)
        sizer.Add(self.c_parallel, 0)
        sizer.Add(self.c_metric, 0)
        sizer.Add(self.c_population, 0)
        sizer.Add(self.c_iteration, 0)

        sizer.Add(self.b_view, 0)

        self.SetBackgroundColour('#AABBCC')
        self.SetSizer(sizer)

        self.c_problem.Bind(wx.EVT_COMBOBOX, self.OnChangeProblem)
        self.c_objective.Bind(wx.EVT_COMBOBOX, self.OnChangeObjective)
        self.c_evolutionary.Bind(wx.EVT_COMBOBOX, self.OnChangeEvolutionary)
        self.c_thread.Bind(wx.EVT_COMBOBOX, self.OnChangeThread)
        self.c_parallel.Bind(wx.EVT_COMBOBOX, self.OnChangeParallel)
        self.c_metric.Bind(wx.EVT_COMBOBOX, self.OnChangeMetric)
        self.c_population.Bind(wx.EVT_COMBOBOX, self.OnChangePopulation)
        self.c_iteration.Bind(wx.EVT_COMBOBOX, self.OnChangeIteration)

        self.b_view.Bind(wx.EVT_BUTTON, self.OnVisualize)

    def OnChangeProblem(self, event):
        print self.c_problem.getTSeleccion()
        self.presenter.setSelectedProblems(self.c_problem.getTSeleccion())
        self.c_objective.tappend(self.presenter.options_objectives)

    def OnChangeObjective(self, event):
        print self.c_objective.getTSeleccion()
        self.presenter.setSelectedObjectives(self.c_objective.getTSeleccion())
        self.c_evolutionary.tappend(self.presenter.options_evolutionarys)

    def OnChangeEvolutionary(self, event):
        print self.c_evolutionary.getTSeleccion()
        self.presenter.setSelectedEvolutionary(self.c_evolutionary.getTSeleccion())
        self.c_thread.tappend(self.presenter.options_threads)

    def OnChangeThread(self, event):
        print self.c_thread.getTSeleccion()
        self.presenter.setSelectedThreads(self.c_thread.getTSeleccion())
        self.c_parallel.tappend(self.presenter.options_parallels)

    def OnChangeParallel(self, event):
        print self.c_parallel.getTSeleccion()
        self.presenter.setSelectedParallel(self.c_parallel.getTSeleccion())
        self.c_metric.tappend(self.presenter.options_metrics)

    def OnChangeMetric(self, event):
        print self.c_metric.getTSeleccion()
        self.presenter.setSelectedMetric(self.c_metric.getTSeleccion())
        self.c_population.tappend(self.presenter.options_populations)

    def OnChangePopulation(self, event):
        print self.c_population.getTSeleccion()
        self.presenter.setSelectedPopulation(self.c_population.getTSeleccion())
        self.c_iteration.tappend(self.presenter.options_iterations)

    def OnChangeIteration(self, event):
        print self.c_iteration.getTSeleccion()
        self.presenter.setSelectedIteration(self.c_iteration.getTSeleccion())

    def OnVisualize(self, event):
        print 'se visualiza'
        p = self.presenter
        self.page_figure.presenter.initFigure(p.problem, p.objective,
                                              p.evolutionary, p.thread,
                                              p.parallel, p.metric,
                                              p.population, p.iteration)
