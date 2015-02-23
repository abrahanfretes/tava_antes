# -*- encoding: utf-8 -*-
'''
Created on 23/09/2014

@author: abrahan
'''
from py.una.pol.tava.dao import dtestconfig
from py.una.pol.tava.model.mparallel_analizer import ParallelAnalizerModel
from datetime import date


class TestConfigModel():

    def __init__(self):
        '''
        Constructor
        '''

    def add(self, test_config):
        '''
        Función que agrega un TestConfig a la base de datos.

        :param test_config: String, representa un TestConfig.
        :description: TestConfig, representa el TestConfig a agregar.
        :return: TestConfig.
        '''
        test_config.creation_date = date.today()
        new_test_config = dtestconfig.add(test_config)
        ParallelAnalizerModel().add(new_test_config)
        return new_test_config

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
