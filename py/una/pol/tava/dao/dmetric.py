'''
Created on 14/5/2015

@author: abrahan
'''
from py.una.pol.tava.base import base, abm
from py.una.pol.tava.base.entity import MoeaProblem as mp

session = base.getSession()


def add(data):
    return abm.add(data)


def delete(data):
    abm.delete(data)


def upDate(data):
    return abm.add(data)


def getFilesNamesMoeaProblemByProject(p):
    return session.query(mp.name_file).filter_by(project_id=p.id).all()
