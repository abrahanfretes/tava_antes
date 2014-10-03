'''
Created on 23/09/2014

@author: abrahan
'''
from py.una.pol.tava.dao import dtestdata


class TestDataModel():

    def __init__(self):
        '''
        Constructor
        '''

    def getTestDatasByTestConfig(self, test_config):
        return self.getTestDatasByTestConfigId(test_config.id)

    def getTestDatasByTestConfigId(self, test_config_id):
        return dtestdata.getTestDatasByTestConfigId(test_config_id)
