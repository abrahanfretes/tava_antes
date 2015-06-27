'''
Created on 14/5/2015

@author: abrahan
'''
from py.una.pol.tava.base import base, abm
from py.una.pol.tava.base.entity import ResultMetric as rmp
from py.una.pol.tava.base.entity import TestMetric as tm
from py.una.pol.tava.base.entity import MoeaProblem as mp

from py.una.pol.tava.base.entity import NumberObjective
from py.una.pol.tava.base.entity import EvolutionaryMethod
from py.una.pol.tava.base.entity import NumberThreads
from py.una.pol.tava.base.entity import ParallelizationMethod
from py.una.pol.tava.base.entity import Metric
from py.una.pol.tava.base.entity import Population
from py.una.pol.tava.base.entity import ValueMetric

from py.una.pol.tava.base.entity import ResultMetric as rm
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
    return session.query(NumberObjective).filter_by(moea_problem_id=problem_id).all()

    # Funciones Para EvolutionaryMethod


def getEvolutionaryMethodByNObjectiveId(n_objevtive_id):
    return session.query(EvolutionaryMethod).filter_by(number_objective_id=n_objevtive_id).all()

    # Funciones Para NumberThreads


def getNumberThreadsByEMethodId(e_method_id):
    return session.query(NumberThreads).filter_by(evolutionary_method_id=e_method_id).all()

    # Funciones Para ParallelizationMethod


def getParallelizationMethodByNThreadId(n_thread_id):
    return session.query(ParallelizationMethod).filter_by(number_threads_id=n_thread_id).all()

    # Funciones Para Metric


def getMetricByPMethodId(p_method_id):
    return session.query(Metric).filter_by(parallelization_method_id=p_method_id).all()

    # Funciones Para Population


def getPopulationByMetricId(metric_id):
    return session.query(Population).filter_by(metric_id=metric_id).all()

    # Funciones Para ValueMetric

def getValueMetricByPopulationId(population_id):
    return session.query(ValueMetric).filter_by(population_id=population_id).all()

def getMoeaProblemByProjectId(project_id):
    return session.query(mp).filter_by(project_id=project_id).all()

def getMaxValueMetricByMoea(id_parallel_method, metric_name, valuePopulation):

    subq = session.query(func.max(vm.value).label('mv')).\
                    select_from(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    filter(pmt.id == id_parallel_method,
                           mtr.name == metric_name,
                           pop.value == valuePopulation).\
                    subquery()
    metric = session.query(vm).\
                    select_from(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    join(subq, subq.c.mv == vm.value).\
                    filter(pmt.id == id_parallel_method,
                           mtr.name == metric_name,
                           pop.value == valuePopulation).\
                    first()
    return metric

def getMaxValueMetricByParallelMethod(idMoea, metric_name, valuePopulation):

    subq = session.query(func.max(vm.value).label('mv')).\
                    select_from(evm).\
                    join(nthr).\
                    join(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    filter(evm.id == idMoea,
                           mtr.name == metric_name,
                           pop.value == valuePopulation).\
                    subquery()
    metric = session.query(vm).\
                    select_from(evm).\
                    join(nthr).\
                    join(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    join(subq, subq.c.mv == vm.value).\
                    filter(evm.id == idMoea,
                           mtr.name == metric_name,
                           pop.value == valuePopulation).\
                    first()
    return metric

def getMinValueMetricByMoea(id_parallel_method, metric_name, valuePopulation):

    subq = session.query(func.min(vm.value).label('mv')).\
                    select_from(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    filter(pmt.id == id_parallel_method,
                           mtr.name == metric_name,
                           pop.value == valuePopulation).\
                    subquery()
    metric = session.query(vm).\
                    select_from(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    join(subq, subq.c.mv == vm.value).\
                    filter(pmt.id == id_parallel_method,
                           mtr.name == metric_name,
                           pop.value == valuePopulation).\
                    first()
    return metric

def getMinValueMetricByParallelMethod(idMoea, metric_name, valuePopulation):

    subq = session.query(func.min(vm.value).label('mv')).\
                    select_from(evm).\
                    join(nthr).\
                    join(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    filter(evm.id == idMoea,
                           mtr.name == metric_name,
                           pop.value == valuePopulation).\
                    subquery()
    metric = session.query(vm).\
                    select_from(evm).\
                    join(nthr).\
                    join(pmt).\
                    join(mtr).\
                    join(pop).\
                    join(vm).\
                    join(subq, subq.c.mv == vm.value).\
                    filter(evm.id == idMoea,
                           mtr.name == metric_name,
                           pop.value == valuePopulation).\
                    first()
    return metric

def getDistinctMetrics():
    metrics = session.query(distinct(mtr.name)).all()
    return metrics

def getDistinctParallelMethodsByResultMetric():
    pass