# -*- encoding: utf-8 -*-
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

    def add(self, name):
        '''
        Función que agrega un TestConfig a la base de datos.

        :param name: String, representa el name de un TestConfig.
        :description: String, representa la descripcion de un TestConfig.
        :return: TestConfig.
        '''

        test_config = TestConfig()
        test_config.name = name
        test_config.creation_date = date.today()

        return dtestconfig.add(test_config)

    def upDate(self, test):
        '''
        Función que actualiza un TestConfig de la base de datos.

        :param test: TestConfig, representa un TestConfig en la base de datos.
        :return: TestConfig.
        '''
        return dtestconfig.add(test)

    def getTestConfigByProject(self, project):
        return self.getTestConfigByProjectId(project.id)

    def getTestConfigByProjectId(self, project_id):
        return dtestconfig.getTestConfigByProjectId(project_id)

    def getTestConfigById(self, test_config_id):
        return dtestconfig.getTestConfigById(test_config_id)
