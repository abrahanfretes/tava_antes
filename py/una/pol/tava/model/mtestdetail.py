'''
Created on 03/10/2014

@author: abrahan
'''
from py.una.pol.tava.dao import dtestdetail


class TestDetailModel():

    def __init__(self):
        '''
        Constructor
        '''

    def getTestDetailsByTestConfig(self, test_config):
        return self.getTestDetailsByTestConfigId(test_config.id)

    def getTestDetailsByTestConfigId(self, test_config_id):
        return dtestdetail.getTestDetailByTestConfigId(test_config_id)
