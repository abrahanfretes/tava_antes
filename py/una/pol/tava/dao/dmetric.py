'''
Created on 14/5/2015

@author: abrahan
'''
from py.una.pol.tava.base import base, abm
from py.una.pol.tava.base.entity import ResultMetric as rmp
from py.una.pol.tava.base.entity import TestMetric as tm

from py.una.pol.tava.base.entity import NumberObjective
from py.una.pol.tava.base.entity import EvolutionaryMethod
from py.una.pol.tava.base.entity import NumberThreads
from py.una.pol.tava.base.entity import ParallelizationMethod
from py.una.pol.tava.base.entity import Metric
from py.una.pol.tava.base.entity import Population
from py.una.pol.tava.base.entity import ValueMetric

from py.una.pol.tava.base.entity import ResultMetric as rm
from py.una.pol.tava.base.entity import MoeaProblem as mp
from py.una.pol.tava.base.entity import NumberObjective as nobj
from py.una.pol.tava.base.entity import EvolutionaryMethod as evm
from py.una.pol.tava.base.entity import NumberThreads as nthr
from py.una.pol.tava.base.entity import ParallelizationMethod as pmt
from py.una.pol.tava.base.entity import Metric as mtr
from py.una.pol.tava.base.entity import Population as pop
from py.una.pol.tava.base.entity import ValueMetric as vm
from sqlalchemy import func, distinct

session = base.getSession()


def add(data):
    return abm.add(data)


def delete(data):
    abm.delete(data)


def upDate(data):
    return abm.add(data)


def getResultMetricById(result_metric_id):
    return session.query(rm).filter_by(id=result_metric_id).one()


def getFilesNamesResultMetricByProject(p):
    return session.query(rmp.filename).filter_by(project_id=p.id).all()


def getResultMetricByProjectId(project_id):
    return session.query(rmp).filter_by(project_id=project_id).all()

    # Funciones Para TestMetric


def getTestMetrics(project_id):
    return session.query(tm).filter_by(project_id=project_id).all()

    # Funciones Para MoeaProblem


def getProblemByResultId(result_id):
    return session.query(mp).filter_by(result_metric=result_id).all()

    # Funciones Para NumberObjective


def getNumberObjectiveByProblemId(problem_id):
    return session.query(NumberObjective).\
        filter_by(moea_problem_id=problem_id).all()

    # Funciones Para EvolutionaryMethod


def getEvolutionaryMethodByNObjectiveId(n_objevtive_id):
    return session.query(EvolutionaryMethod).\
        filter_by(number_objective_id=n_objevtive_id).all()

    # Funciones Para NumberThreads


def getNumberThreadsByEMethodId(e_method_id):
    return session.query(NumberThreads).\
        filter_by(evolutionary_method_id=e_method_id).all()


def getNumberThreadsByValue(e_method_id, v_thread):
    return session.query(NumberThreads)\
        .filter(NumberThreads.evolutionary_method_id == e_method_id,
                NumberThreads.value == v_thread).first()
    # Funciones Para ParallelizationMethod


def getParallelizationMethodByNThreadId(n_thread_id):
    return session.query(ParallelizationMethod).\
        filter_by(number_threads_id=n_thread_id).all()


def getParallelizationMethodByValue(n_thread_id, v_method):
    return session.query(ParallelizationMethod)\
        .filter(ParallelizationMethod.number_threads_id == n_thread_id,
                ParallelizationMethod.name == v_method).first()

    # Funciones Para Metric


def getMetricByPMethodId(p_method_id):
    return session.query(Metric).\
        filter_by(parallelization_method_id=p_method_id).all()


def getMetricByValue(p_method_id, v_value):
    return session.query(Metric)\
        .filter(Metric.parallelization_method_id == p_method_id,
                Metric.name == v_value).first()
    # Funciones Para Population


def getPopulationByMetricId(metric_id):
    return session.query(Population).filter_by(metric_id=metric_id).all()


def getPopulationByValue(metric_id, v_value):
    return session.query(Population).filter(Population.metric_id == metric_id,
                                            Population.value == v_value)\
                                            .first()


# Funciones Para ValueMetric
def getValueMetricByPopulationId(population_id):
    return session.query(ValueMetric).filter_by(
                                            population_id=population_id).all()


def getMoeaProblemByProjectId(project_id):
    return session.query(mp).filter_by(project_id=project_id).all()


def getValueMetricByMoea(parallel_method_id, metric_name, value_population,
                   iteration):

    value_metric = session.query(vm).\
                    select_from(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    filter(pmt.id == parallel_method_id,
                           mtr.name == metric_name,
                           pop.value == value_population,
                           vm.iteration == iteration).\
                    first()
    return value_metric


def getValueMetricByParallelMethod(number_objective_id,
                                   moea_name,
                                   number_thread,
                                   parallel_method_name,
                                   metric_name,
                                   value_population,
                                   iteration):

    value_metric = session.query(vm).\
                    select_from(nobj).\
                    join(evm).\
                    join(nthr).\
                    join(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    filter(nobj.id == number_objective_id,
                           evm.name == moea_name,
                           nthr.value == number_thread,
                           pmt.name == parallel_method_name,
                           mtr.name == metric_name,
                           pop.value == value_population,
                           vm.iteration == iteration).\
                    first()
    return value_metric


def getMaxValueMetric(number_thread_id, value_population, metric_name):

    subq = session.query(func.max(vm.value).label('mv')).\
                    select_from(nthr).\
                    join(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    filter(nthr.id == number_thread_id,
                           mtr.name == metric_name,
                           pop.value == value_population).\
                    subquery()
    metric = session.query(vm).\
                    select_from(nthr).\
                    join(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    join(subq, subq.c.mv == vm.value).\
                    filter(nthr.id == number_thread_id,
                           mtr.name == metric_name,
                           pop.value == value_population).\
                    first()
    return metric


def getMinValueMetric(number_thread_id, value_population, metric_name):

    subq = session.query(func.min(vm.value).label('mv')).\
                    select_from(nthr).\
                    join(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    filter(nthr.id == number_thread_id,
                           mtr.name == metric_name,
                           pop.value == value_population).\
                    subquery()
    metric = session.query(vm).\
                    select_from(nthr).\
                    join(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    join(subq, subq.c.mv == vm.value).\
                    filter(nthr.id == number_thread_id,
                           mtr.name == metric_name,
                           pop.value == value_population).\
                    first()
    return metric


def getMaxValueMetricByParallelMethod(number_objective_id,
                                      parallel_method_name,
                                      metric_name,
                                      value_population):

    subq = session.query(func.max(vm.value).label('mv')).\
                    select_from(nobj).\
                    join(evm).\
                    join(nthr).\
                    join(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    filter(nobj.id == number_objective_id,
                           pmt.name == parallel_method_name,
                           mtr.name == metric_name,
                           pop.value == value_population).\
                    subquery()
    metric = session.query(vm).\
                    select_from(nobj).\
                    join(evm).\
                    join(nthr).\
                    join(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    join(subq, subq.c.mv == vm.value).\
                    filter(nobj.id == number_objective_id,
                           pmt.name == parallel_method_name,
                           mtr.name == metric_name,
                           pop.value == value_population).\
                    first()
    return metric


def getMinValueMetricByParallelMethod(number_objective_id,
                                      parallel_method_name,
                                      metric_name,
                                      value_population):

    subq = session.query(func.min(vm.value).label('mv')).\
                    select_from(nobj).\
                    join(evm).\
                    join(nthr).\
                    join(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    filter(nobj.id == number_objective_id,
                           pmt.name == parallel_method_name,
                           mtr.name == metric_name,
                           pop.value == value_population).\
                    subquery()
    metric = session.query(vm).\
                    select_from(nobj).\
                    join(evm).\
                    join(nthr).\
                    join(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    join(subq, subq.c.mv == vm.value).\
                    filter(nobj.id == number_objective_id,
                           pmt.name == parallel_method_name,
                           mtr.name == metric_name,
                           pop.value == value_population).\
                    first()
    return metric


def getDistinctMetrics(id_result_metric):
    metrics = session.query(distinct(mtr.name))\
                     .select_from(rm)\
                     .join(mp)\
                     .join(nobj)\
                     .join(evm)\
                     .join(nthr)\
                     .join(pmt)\
                     .join(mtr)\
                     .filter(rm.id == id_result_metric)\
                     .all()
    return metrics


def getDistinctParallelMethodsByNumberObjective(number_objective_id):
    parallel_methods = session.query(distinct(pmt.name)).\
                        select_from(nobj).\
                        join(evm).\
                        join(nthr).\
                        join(pmt).\
                        filter(nobj.id == number_objective_id).\
                        all()
    return parallel_methods


def getMaxValuePopulation(metric_id):
    return session.query(func.max(pop.value)).filter(mtr.id == metric_id).one()


def getPopulation(metric_id, value_population):
    return session.query(Population).filter_by(metric_id=metric_id,
                                               value=value_population).one()
