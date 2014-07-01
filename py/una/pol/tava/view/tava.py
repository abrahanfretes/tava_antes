# -*- coding: utf-8 -*-
'''
Created on 27/06/2014

@author: aferreira
'''
import wx
from FramePrincipal import FramePrincipal


def main():
    '''
    Método principal de ejecución del programa
    '''
    ex = wx.App()
    FramePrincipal(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()
