'''
Created on 7/6/2015

@author: abrahan
'''
from py.una.pol.tava.model.mmetric import MetricModel as mm


# ------------------- Clase Presentador de Figura Coordenadas Paralelas  ------
# -------------------                                  ------------------------
class ConfigMetricSingPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        print self.test

        self.options_problems = []
        self.options_objectives = []
        self.options_evolutionarys_pivot = []
        self.options_evolutionarys_options = []
        self.options_threads = []
        self.options_parallels = []
        self.options_metrics = []
        self.options_populations = []
        self.options_iterations = []

        self.problem = None
        self.objective = None
        self.evolutionary_pivot = None
        self.evolutionary_options = []
        self.thread = None
        self.parallel = None
        self.metric = None
        self.population = None
        self.iteration = None

        self.setOptionProblems()

    def setOptionProblems(self):
        self.problems = mm().getProblems(self.test.result_metric_id)
        for pro in self.problems:
            self.options_problems.append(pro.name)

    def setSelectedProblems(self, index):
        self.problem = self.problems[index]
        self.objectives = mm().getNumberObjectives(self.problem.id)
        self.options_objectives = []
        for obj in self.objectives:
            self.options_objectives.append(obj.value)

    def setSelectedObjectives(self, index):
        self.objective = self.objectives[index]
        self.evolutionarys = mm().getEvolutionaryMethods(self.objective.id)
        self.options_evolutionarys_pivot = []
        for evo in self.evolutionarys:
            self.options_evolutionarys_pivot.append(evo.name)

    def setSelectedEvolutionaryP(self, index):
        self.evolutionary_pivot = self.evolutionarys[index]
        self.options_evolutionarys_options = []
        self.evolutionary_options = []
        for i in range(len(self.evolutionarys)):
            if i != index:
                evo = self.evolutionarys[i]
                self.options_evolutionarys_options.append(evo.name)
                self.evolutionary_options.append(evo)

        self.threads = mm().getThreads(self.evolutionary_pivot.id)
        self.options_threads = []
        for thr in self.threads:
            self.options_threads.append(thr.value)

    def setSelectedThreads(self, index):
        self.thread = self.threads[index]
        self.parallels = mm().getParallelizationMethods(self.thread.id)
        self.options_parallels = []
        for par in self.parallels:
            self.options_parallels.append(par.name)

    def setSelectedParallel(self, index):
        self.parallel = self.parallels[index]
        self.metrics = mm().getMetrics(self.parallel.id)
        self.options_metrics = []
        for m in self.metrics:
            self.options_metrics.append(m.name)

    def setSelectedMetric(self, index):
        self.metric = self.metrics[index]
        self.populations = mm().getPopulations(self.metric.id)
        self.options_populations = []
        for ps in self.populations:
            self.options_populations.append(ps.value)

    def setSelectedPopulation(self, index):
        self.population = self.populations[index]
        self.iterations = mm().getValueMetrics(self.population.id)
        self.options_iterations = []
        for i in self.iterations:
            self.options_iterations.append(i.iteration)

    def setSelectedIteration(self, index):
        self.iteration = self.iterations[index]

    def getEvoSelected(self, indexs):
        ret = []
        for index in indexs:
            ret.append(self.evolutionary_options[index])
        return ret
