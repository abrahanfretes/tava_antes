'''
Created on 14/5/2015

@author: abrahan
'''
from py.una.pol.tava.base import base, abm
from py.una.pol.tava.base.entity import ResultMetric as rmp

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
