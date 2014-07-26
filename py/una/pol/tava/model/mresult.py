'''
Created on 28/06/2014

@author: abrahan
'''
from py.una.pol.tava.model.processor import styleVon
from py.una.pol.tava.model.bd import query
from py.una.pol.tava.model.bd import abm


class ResultModel(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def add(self, list_path_file, project):
        styleVon.procesarArchivo(list_path_file, project)

    def delete(self, result):
        abm.delete(result)

    def getResultsByProject(self, project):
        return query.getResultsByProject(project)

    def getResultById(self, id_result):
        return query.getResultById(id_result)
