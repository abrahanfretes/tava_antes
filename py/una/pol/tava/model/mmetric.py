'''
Created on 14/5/2015

@author: abrahan
'''
from py.una.pol.tava.base.tavac import vonlucken
from py.una.pol.tava.model.processor import styleVon
from py.una.pol.tava.dao import dmetric


class MetricModel():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def add(self, paths, project, style):

        if style == vonlucken:
            return styleVon.processMetricsFile(paths, project)

        # aca se debe agregar las funciones para otros estilos
        # if style == otro:
        # otro.procesarArchivo(list_path_file, project)
        pass

    def quickCheckStyle(self, path, style):
        if style == vonlucken:
            return styleVon.quickCheckStyleMetric(path)

    def getFilesNames(self, project):
        listNames = []
        print dmetric.getFilesNamesResultMetricByProject(project)
        for name in dmetric.getFilesNamesResultMetricByProject(project):
            listNames.append(list(name).pop())

        return listNames

    # Funciones Para ResultMetric
    def getResultMetricByProjectId(self, project_id):
        return dmetric.getResultMetricByProjectId(project_id)

    def getNamesMetricResults(self, project_id):
        to_ret = []
        for mr in self.getResultMetricByProjectId(project_id):
            to_ret.append(mr.filename)
        return to_ret

    # Funciones Para NumberObjective
    def getNumberObjectives(self, problem_id):
        return dmetric.getNumberObjectiveByProblemId(problem_id)

        # Funciones Para EvolutionaryMethod
    def getEvolutionaryMethods(self, n_objevtive_id):
        return dmetric.getEvolutionaryMethodByNObjectiveId(n_objevtive_id)

    def getEvolutionaryMethodsDistinct(self, evolutionary_method):
        mms = self.getEvolutionaryMethods(evolutionary_method.number_objective)
        ret = []
        for m in mms:
            if m.id != evolutionary_method.id:
                ret.append(m)
        return ret

        # Funciones Para NumberThreads
    def getThreads(self, e_method_id):
        return dmetric.getNumberThreadsByEMethodId(e_method_id)

    def getThreadsByValue(self, e_method_id, v_thread):
        return dmetric.getNumberThreadsByValue(e_method_id, v_thread)

        # Funciones Para ParallelizationMethod
    def getParallelizationMethods(self, n_thread_id):
        return dmetric.getParallelizationMethodByNThreadId(n_thread_id)

    def getParallelizationMethodByValue(self, n_thread_id, v_method):
        return dmetric.getParallelizationMethodByValue(n_thread_id, v_method)

        # Funciones Para Metric
    def getMetrics(self, p_method_id):
        return dmetric.getMetricByPMethodId(p_method_id)

    def getMetricsByValue(self, p_method_id, v_value):
        return dmetric.getMetricByValue(p_method_id, v_value)

        # Funciones Para Population
    def getPopulations(self, metric_id):
        return dmetric.getPopulationByMetricId(metric_id)

    def getPopulationsByValue(self, metric_id, v_value):
        return dmetric.getPopulationByValue(metric_id, v_value)

        # Funciones Para ValueMetric
    def getValueMetrics(self, population_id):
        return dmetric.getValueMetricByPopulationId(population_id)

    def getValueMetricsByEvolutionaryMethod(self, e_method, v_thread,
                                            v_parallel, v_metric,
                                            v_population):

        thread = self.getThreadsByValue(e_method.id, v_thread)
        parallel = self.getParallelizationMethodByValue(thread.id, v_parallel)
        metric = self.getMetricsByValue(parallel.id, v_metric)
        population = self.getPopulationsByValue(metric.id, v_population)

        return self.getValueMetrics(population.id)

        # Funciones Para TestMetric
    def getTestMetricByProjectId(self, project_id):
        return dmetric.getTestMetrics(project_id)

    def getNamesTestMetric(self, project_id):
        to_ret = []
        for tm in self.getTestMetricByProjectId(project_id):
            to_ret.append(tm.name)
        print to_ret
        return to_ret

    def addTestMetric(self, test_metric):
        dmetric.add(test_metric)

        # MoeaProblem

    def getProblems(self, result_id):
        return dmetric.getProblemByResultId(result_id)
