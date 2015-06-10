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
session = base.getSession()


def add(data):
    return abm.add(data)


def delete(data):
    abm.delete(data)


def upDate(data):
    return abm.add(data)


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
    return session.query(NumberObjective).filter_by(moea_problem=problem_id).all()

    # Funciones Para EvolutionaryMethod


def getEvolutionaryMethodByNObjectiveId(n_objevtive_id):
    return session.query(EvolutionaryMethod).filter_by(number_objective=n_objevtive_id).all()

    # Funciones Para NumberThreads


def getNumberThreadsByEMethodId(e_method_id):
    return session.query(NumberThreads).filter_by(evolutionary_method=e_method_id).all()

    # Funciones Para ParallelizationMethod


def getParallelizationMethodByNThreadId(n_thread_id):
    return session.query(ParallelizationMethod).filter_by(number_thread=n_thread_id).all()

    # Funciones Para Metric


def getMetricByPMethodId(p_method_id):
    return session.query(Metric).filter_by(parallelization_method=p_method_id).all()

    # Funciones Para Population


def getPopulationByMetricId(metric_id):
    return session.query(Population).filter_by(metric=metric_id).all()

    # Funciones Para ValueMetric


def getValueMetricByPopulationId(population_id):
    return session.query(ValueMetric).filter_by(population=population_id).all()
