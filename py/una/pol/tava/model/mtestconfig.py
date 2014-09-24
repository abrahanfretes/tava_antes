'''
Created on 23/09/2014

@author: abrahan
'''
from py.una.pol.tava.base.entity import TestConfig
from py.una.pol.tava.dao import dtestconfig
from datetime import date


class TestConfigModel():

    def __init__(self):
        '''
        Constructor
        '''

    def add(self, name, description):
        '''
        Función que agrega un TestConfig a la base de datos.

        :param name: String, representa el name de un TestConfig.
        :description: String, representa la descripcion de un TestConfig.
        :return: TestConfig.
        '''

        test_config = TestConfig()
        test_config.name = name
        test_config.description = description
        test_config.creation_date = date.today()

        return dtestconfig.add(test_config)
