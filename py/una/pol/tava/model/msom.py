'''
Created on 09/12/2014

@author: arsenioferreira
'''
from py.una.pol.tava.dao import dsom
from py.una.pol.tava.base.entity import SomConfig


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

    def addWithTestConfig(self, testConfig):
        som = SomConfig()
        som.learning_rate = 0.5
        som.sigma = 0.5
        som.columns = 6
        som.rows = 6
        som.map_initialization = "random"
        som.iterations = 100
        som.test_config_id = testConfig.id
        return dsom.add(som)

    def getSomById(self, id_som):
        return dsom.getSomById(id_som)

    def get_som_by_test_config_id(self, id_test_config):
        return dsom.get_som_by_test_config_id(id_test_config)
