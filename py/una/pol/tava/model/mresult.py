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
            styleVon.procesarArchivo(list_path_file, project)

        # aca se debe agregar las funciones para otros estilos
        #if style == otro:
            #otro.procesarArchivo(list_path_file, project)

    def fastVerificationStyle(self, path_file, style):
        if style == vonlucken:
            return styleVon.fastVerification(path_file)

    def delete(self, result):
        dresult.delete(result)

    def getResultsByProject(self, project):
        return dresult.getResultsByProject(project)

    def getResultById(self, id_result):
        return dresult.getResultById(id_result)

    def getResultByName(self, name_result):
        return dresult.getResultByName(name_result)

    def getNamesResultForProject(self, project):
        listNames = []
        for name in dresult.getNamesResultForProject(project):
            listNames.append(list(name).pop())

        return listNames
