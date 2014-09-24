# -*- coding: utf-8 -*-
'''
Created on 27/06/2014

@author: aferreira
'''
import wx
from py.una.pol.tava.base.entity import createDB


def main():
    '''
    Método principal de ejecución del programa---
    '''
    createDB()
    ex = wx.App()
    from py.una.pol.tava.view.vframe import MainFrame
    frame = MainFrame(None)
    frame.Centre(wx.BOTH)
    ex.MainLoop()

if __name__ == '__main__':
    main()
