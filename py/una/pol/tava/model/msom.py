'''
Created on 09/12/2014

@author: arsenioferreira
'''
from py.una.pol.tava.dao import dsom


class SomModel():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def add(self, som):
        '''
        Funcion que agrega un SOM a la base de datos.

        :param som: representa un Som.
        :description: Som, representa el Som a agregar.
        :return: Som.
        '''
        return dsom.add(som)

    def getSomById(self, id_som):
        return  dsom.getSomById(id_som)
