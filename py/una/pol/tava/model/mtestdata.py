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

    def getTestDatasByTestDetail(self, test_detail):
        return self.getTestDatasByTestDetailId(test_detail.id)

    def getTestDatasByTestDetailId(self, test_detail_id):
        return dtestdata.getTestDatasByTestDetailId(test_detail_id)
