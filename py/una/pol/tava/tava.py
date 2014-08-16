# -*- coding: utf-8 -*-
'''
Created on 27/06/2014

@author: aferreira
'''
import wx
from py.una.pol.tava.base import base
from py.una.pol.tava.view.vframe import MainFrame


def main():
    '''
    Método principal de ejecución del programa
    '''
    base.createDb()
    ex = wx.App()
    frame = MainFrame(None)
    frame.Centre()
    ex.MainLoop()

if __name__ == '__main__':
    main()
