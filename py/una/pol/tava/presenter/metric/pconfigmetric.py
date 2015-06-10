'''
Created on 7/6/2015

@author: abrahan
'''
from py.una.pol.tava.model.mmetric import MetricModel as mm


# ------------------- Clase Presentador de Figura Coordenadas Paralelas  ------
# -------------------                                  ------------------------
class ConfigMetricPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        print self.test

        self.options_problems = []
        self.options_objectives = []
        self.options_evolutionarys = []
        self.options_threads = []
        self.options_parallels = []
        self.options_metrics = []
        self.options_populations = []
        self.options_iterations = []

        self.problem = None
        self.objective = None
        self.evolutionary = None
        self.thread = None
        self.parallel = None
        self.metric = None
        self.population = None
        self.iteration = None

        self.__setInitVar()
        self.setOptionProblems()

    def setOptionProblems(self):
        self.problems = mm().getProblems(self.test.result_metric_id)
        for pro in self.problems:
            self.options_problems.append(pro.name)

    def setSelectedProblems(self, index):
        self.problem = self.problems[index]
        self.__setInitVar(1)
        self.setOptionObjectives()


    def setOptionObjectives(self):
        self.objectives = mm().getNumberObjectives(self.problem.id)
        for obj in self.objectives:
            self.options_objectives.append(obj.value)

    def setSelectedObjectives(self, index):
        self.objective = self.objectives[index]
        self.__setInitVar(2)
        self.setOptionEvolutionarys()


    def setOptionEvolutionarys(self):
        self.evolutionarys = mm().getEvolutionaryMethods(self.objective.id)
        for evo in self.evolutionarys:
            self.options_evolutionarys.append(evo.name)

    def setSelectedEvolutionary(self, index):
        self.evolutionary = self.evolutionarys[index]
        self.__setInitVar(3)
        self.setOptionThreads()


    def setOptionThreads(self):
        self.threads = mm().getThreads(self.evolutionary.id)
        for thr in self.threads:
            self.options_threads.append(thr.value)

    def setSelectedThreads(self, index):
        self.thread = self.threads[index]
        self.__setInitVar(4)
        self.setOptionParallel()


    def setOptionParallel(self):
        self.parallels = mm().getParallelizationMethods(self.thread.id)
        for par in self.parallels:
            self.options_parallels.append(par.name)

    def setSelectedParallel(self, index):
        self.parallel = self.parallels[index]
        self.__setInitVar(5)
        self.setOptionMetric()


    def setOptionMetric(self):
        self.metrics = mm().getMetrics(self.parallel.id)
        for m in self.metrics:
            self.options_metrics.append(m.name)

    def setSelectedMetric(self, index):
        self.metric = self.metrics[index]
        self.__setInitVar(6)
        self.setOptionPopulation()


    def setOptionPopulation(self):
        self.populations = mm().getPopulations(self.metric.id)
        for ps in self.populations:
            self.options_populations.append(ps.value)

    def setSelectedPopulation(self, index):
        self.population = self.populations[index]
        self.__setInitVar(7)
        self.setOptionIteration()


    def setOptionIteration(self):
        self.iterations = mm().getValueMetrics(self.population.id)
        for i in self.iterations:
            self.options_iterations.append(i.iteration)

    def setSelectedIteration(self, index):
        self.iteration = self.iterations[index]


    def __setInitVar(self, option=0):
        if option < 1:
            self.problems = []
        if option < 2:
            self.objectives = []
        if option < 3:
            self.evolutionarys = []
        if option < 4:
            self.threads = []
        if option < 5:
            self.parallels = []
        if option < 6:
            self.metrics = []
        if option < 7:
            self.populations = []
        if option < 8:
            self.iterations = []

            #===================================================================
            # print pro
            # for n_o in pro.number_objectives:
            #     print n_o
            #     for e_m in n_o.evolutionary_methods:
            #         print e_m
            #         for n_t in e_m.number_threadss:
            #             print n_t
            #             for p_m in n_t.parallelization_methods:
            #                 print p_m
            #                 for m in p_m.metrics:
            #                     print m
            #                     for pp in m.populations:
            #                         print pp
            #                         print pp.value_metrics
            #                         #--------------- for vm in pp.value_metrics:
            #                             #----------------------------- print vm.
            #===================================================================