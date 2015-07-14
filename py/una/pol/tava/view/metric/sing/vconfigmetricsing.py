#  -*- coding: utf-8 -*-
'''
Created on 7/6/2015

@author: abrahan
'''
import wx
import wx.lib.agw.pycollapsiblepane as PCP

from py.una.pol.tava.view.com.tcombobox import TComboBox, TSpinCtrlDouble
from py.una.pol.tava.presenter.metric.sing.pconfigmetricsing import\
    ConfigMetricSingPresenter


# ------------------- Arbol de Archvivos e Iteraciones ------------------------
# -------------------                                  ------------------------
class ConfigMetricSing(wx.Panel):
    def __init__(self, parent, page_main, page_statistic, test):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.page_main = page_main
        self.page_statistic = page_statistic
        presenter = ConfigMetricSingPresenter(self, test)
        self.p = presenter

        title_cont = 'Configuración de la Comparación'
        self.title = wx.StaticText(self, label=title_cont,
                                   style=wx.ALIGN_CENTRE)
        name_cont = 'Comparción en Pares - Sing Test'
        self.name_test = wx.StaticText(self, label=name_cont,
                                       style=wx.ALIGN_CENTRE)

        # Componentes
        self.spin_t = TSpinCtrlDouble(self, 'Nivel de Significación: ')

        self.c_problem = TComboBox(self, 'Problema:',
                                   self.p.options_problems)

        self.c_objective = TComboBox(self, 'Numero Objetivo :',
                                     self.p.options_objectives)

        self.c_evolutionary_pivot = TComboBox(self, 'Metodo Evolutivo Pivot:',
                                              self.p.options_evolutionarys_pivot)

        self.cpStyle = wx.CP_NO_TLW_RESIZE
        self.cp = PCP.PyCollapsiblePane(self, label='Metodo Evolutivo 1',
                                        agwStyle=self.cpStyle)
        self.cp.SetBackgroundColour('#AABBCC')
        self.MakePaneContent(self.cp.GetPane(), self.p.options_evolutionarys_options)
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, self.cp)

        self.c_thread = TComboBox(self, 'Numero de Hilos :', self.p.options_threads)
        self.c_parallel = TComboBox(self, 'Metodo Paralelo :', self.p.options_parallels)
        self.c_metric = TComboBox(self, 'Metrica :', self.p.options_metrics)
        self.c_population = TComboBox(self, 'Poblacion :', self.p.options_populations)
        self.c_iteration = TComboBox(self, 'Iteracion :', self.p.options_iterations)

        self.b_view = wx.Button(self, label='visualizar')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.title, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 5)
        sizer.Add(self.name_test, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        sizer.Add(self.spin_t, 0)

        sizer.Add(self.c_problem, 0)
        sizer.Add(self.c_objective, 0)

        sizer.Add(self.c_evolutionary_pivot, 0)
        sizer.Add(self.cp,  0, wx.EXPAND)

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
        self.c_evolutionary_pivot.Bind(wx.EVT_COMBOBOX, self.OnChangeEvolutionaryP)
        self.c_thread.Bind(wx.EVT_COMBOBOX, self.OnChangeThread)
        self.c_parallel.Bind(wx.EVT_COMBOBOX, self.OnChangeParallel)
        self.c_metric.Bind(wx.EVT_COMBOBOX, self.OnChangeMetric)
        self.c_population.Bind(wx.EVT_COMBOBOX, self.OnChangePopulation)
        self.c_iteration.Bind(wx.EVT_COMBOBOX, self.OnChangeIteration)

        self.b_view.Bind(wx.EVT_BUTTON, self.OnVisualize)

        self.ini = 0
        self.initializeDefaultsValues()

    def OnChangeProblem(self, event):
        # self.p.resetVariables(1)
        self.p.setSelectedProblems(self.c_problem.getTSeleccion())
        self.c_objective.tappend(self.p.options_objectives)
        self.resetComponents(2)

    def OnChangeObjective(self, event):
        # self.p.resetVariables(2)
        self.p.setSelectedObjectives(self.c_objective.getTSeleccion())
        self.c_evolutionary_pivot.tappend([])
        self.c_evolutionary_pivot.tappend(self.p.options_evolutionarys_pivot)
        self.c_evolutionary_pivot.combo.Enable()
        self.cp.Enable()
        self.resetComponents(3)

    def OnChangeEvolutionaryP(self, event):
        # self.p.resetVariables(3)
        aux = self.c_evolutionary_pivot
        self.p.setSelectedEvolutionaryP(aux.getTSeleccion())
        self.Rebuild(self.p.options_evolutionarys_options)
        self.c_thread.tappend([])
        self.c_thread.tappend(self.p.options_threads)
        self.c_thread.combo.Enable()
        self.resetComponents(4)

    def OnChangeThread(self, event):
        # self.p.resetVariables(4)
        self.p.setSelectedThreads(self.c_thread.getTSeleccion())
        self.c_parallel.tappend([])
        self.c_parallel.tappend(self.p.options_parallels)
        self.c_parallel.combo.Enable()
        self.resetComponents(5)

    def OnChangeParallel(self, event):
        # self.p.resetVariables(5)
        self.p.setSelectedParallel(self.c_parallel.getTSeleccion())
        self.c_metric.tappend([])
        self.c_metric.tappend(self.p.options_metrics)
        self.c_metric.combo.Enable()
        self.resetComponents(6)

    def OnChangeMetric(self, event):
        # self.p.resetVariables(6)
        self.p.setSelectedMetric(self.c_metric.getTSeleccion())
        self.c_population.tappend([])
        self.c_population.tappend(self.p.options_populations)
        self.c_population.combo.Enable()
        self.resetComponents(7)

    def OnChangePopulation(self, event):
        # self.p.resetVariables(7)
        self.p.setSelectedPopulation(self.c_population.getTSeleccion())
        self.c_iteration.tappend([])
        self.c_iteration.tappend(self.p.options_iterations)
        self.c_iteration.combo.Enable()
        self.resetComponents(8)

    def OnChangeIteration(self, event):
        # self.p.resetVariables(7)
        self.p.setSelectedIteration(self.c_iteration.getTSeleccion())
        self.b_view.Enable()

    def OnVisualize(self, event):
        print 'se visualiza'
        p = self.p
        print self.lb.GetChecked()
        evo_selected = p.getEvoSelected(self.lb.GetChecked())
        self.page_statistic.p.initFigure(p.problem, p.objective,
                                         p.evolutionary_pivot,
                                         p.thread,
                                         p.parallel, p.metric,
                                         p.population, p.iteration,
                                         evo_selected)

    def OnPaneChanged(self, event=None):
        self.Layout()

    def MakePaneContent(self, pane, evolutionarys):
        '''Just make a few controls to put on the collapsible pane'''

        self.size_list = len(evolutionarys)
        self.lb = wx.CheckListBox(pane, -1, wx.DefaultPosition, (30, 10),
                                  evolutionarys)
        self.lb.SetChecked(range(self.size_list))

        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        mar_all = wx.Button(pane, label='Marcar Todo')
        des_all = wx.Button(pane, label='Desmarcar Todo')
        sizer_button.Add(mar_all)
        sizer_button.Add(des_all)

        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(self.lb, 5, wx.EXPAND | wx.ALL, 5)
        border.Add(sizer_button, 1, wx.EXPAND | wx.ALL, 5)

        pane.SetSizer(border)

        mar_all.Bind(wx.EVT_BUTTON, self.OnCheckAll)
        des_all.Bind(wx.EVT_BUTTON, self.OnUnCheckAll)
        self.lb.Bind(wx.EVT_CHECKLISTBOX, self.OnCheckListBox)

    def OnCheckListBox(self, event):
        if self.lb.GetChecked() == ():
            self.resetComponents(3)
        else:
            self.c_thread.combo.Enable()

    def OnCheckAll(self, event):
        self.lb.SetChecked(range(self.size_list))
        self.c_thread.combo.Enable()

    def OnUnCheckAll(self, event):
        for i in range(self.size_list):
            self.lb.Check(i, False)
        self.resetComponents(3)

    def Rebuild(self, evolutionarys):

        # isExpanded = self.cp.IsExpanded()
        self.Freeze()
        cp = PCP.PyCollapsiblePane(self, label='Metodo Evolutivo 1',
                                   agwStyle=self.cpStyle)
        cp.SetBackgroundColour('#AABBCC')
        cp.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)
        self.MakePaneContent(cp.GetPane(), evolutionarys)

        self.GetSizer().Replace(self.cp, cp)
        self.cp.Destroy()
        self.cp = cp

        self.cp.Expand()
        self.Thaw()
        if self.ini == 1:
            self.Layout()
        else:
            self.ini = 1

    def resetComponents(self, option):
        if option < 1:
            self.c_problem.combo.Disable()
        if option < 2:
            self.c_objective.combo.Disable()
        if option < 3:
            self.c_evolutionary_pivot.combo.Disable()
            self.cp.Disable()
        if option < 4:
            self.c_thread.combo.Disable()
        if option < 5:
            self.c_parallel.combo.Disable()
        if option < 6:
            self.c_metric.combo.Disable()
        if option < 7:
            self.c_population.combo.Disable()
        if option < 8:
            self.c_iteration.combo.Disable()
        if option < 8:
            self.b_view.Disable()

    def initializeDefaultsValues(self):
        self.c_problem.combo.SetSelection(0)
        self.OnChangeProblem(None)

        self.c_objective.combo.SetSelection(0)
        self.OnChangeObjective(None)

        self.c_evolutionary_pivot.combo.SetSelection(0)
        self.OnChangeEvolutionaryP(None)

        self.c_thread.combo.SetSelection(0)
        self.OnChangeThread(None)

        self.c_parallel.combo.SetSelection(0)
        self.OnChangeParallel(None)

        self.c_metric.combo.SetSelection(0)
        self.OnChangeMetric(None)

        self.c_population.combo.SetSelection(0)
        self.OnChangePopulation(None)

        self.c_iteration.combo.SetSelection(0)
        self.OnChangeIteration(None)
