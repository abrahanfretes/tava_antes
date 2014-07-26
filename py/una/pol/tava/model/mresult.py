'''
Created on 28/06/2014

@author: abrahan
'''
from py.una.pol.tava.model.processor import styleVon
from py.una.pol.tava.dao import dresult


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
        dresult.delete(result)

    def getResultsByProject(self, project):
        return dresult.getResultsByProject(project)

    def getResultById(self, id_result):
        return dresult.getResultById(id_result)
