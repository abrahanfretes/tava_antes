# -*- coding: utf-8 -*-
'''
Created on 27/06/2014

@author: aferreira
'''
import wx
from FramePrincipal import FramePrincipal
from py.una.pol.tava.model.bd import base


def main():
    '''
    Método principal de ejecución del programa
    '''
    base.createDb()
    ex = wx.App()
    FramePrincipal(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()
