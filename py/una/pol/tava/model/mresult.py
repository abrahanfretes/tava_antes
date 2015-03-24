'''
Created on 28/06/2014

@author: abrahan
'''
from py.una.pol.tava.model.processor import styleVon
from py.una.pol.tava.dao import dresult
from py.una.pol.tava.base.tavac import vonlucken


class ResultModel(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def add(self, list_path_file, project, style):

        if style == vonlucken:
            return styleVon.procesarArchivo(list_path_file, project)

        # aca se debe agregar las funciones para otros estilos
        # if style == otro:
        # otro.procesarArchivo(list_path_file, project)

    def fastVerificationStyle(self, path_file, style):
        if style == vonlucken:
            return styleVon.fastVerification(path_file)

    def delete(self, result):
        dresult.delete(result)

    def getResultsByProject(self, project):
        return self.getResultsByProjectId(project.id)

    def getResultsByProjectId(self, project_id):
        return dresult.getResultsByProject(project_id)

    def getResultById(self, id_result):
        return dresult.getResultById(id_result)

    def getResultByName(self, name_result):
        return dresult.getResultByName(name_result)

    def getResultWithIterations(self, result):
        return dresult.getResultWithIterations(result)

    def getNamesResultForProject(self, project):
        listNames = []
        for name in dresult.getNamesResultForProject(project):
            listNames.append(list(name).pop())

        return listNames

    def getResultByProjectAndFileName(self, project, reult_name):
        return self.getResultByProjectIdAndFileName(project.id, reult_name)

    def getResultByProjectIdAndFileName(self, project_id, reult_name):
        return dresult.getResultByProjectIdAndFileName(project_id, reult_name)

    def getNameById(self, id_result):
        return self.getResultById(id_result).name

    def getNumberObjetivetById(self, id_result):
        return dresult.getResultById(id_result).number_objectives

    def getNamesObjetivestById(self, r_id):
        return dresult.getResultById(r_id).name_objectives
