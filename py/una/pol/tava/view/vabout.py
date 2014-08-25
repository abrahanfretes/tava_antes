# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''

import wx
import py.una.pol.tava.view.vimages as I


class AboutDialog(wx.AboutDialogInfo):
    '''
    Clase que representa a la ventana que despliega información acerca de
    detalles del programa.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        super(AboutDialog, self).__init__()

        description = """TAVA es una herramienta para el soporte de
        visualización de archivos resultados de algoritmos evolutivos.
        Sus caracteristicas incluyen facilidad de uso, interacción, incluye
        una amplia gama de componentes gráficos utilizados para las pruebas de
        analisis."""

        licence = """        TAVA es free software; usted puede redistribuirlo
        y/o modificarlo bajo los términos de GNU General Public License según
        lo publicado por la Free Software Foundation; ya sea la versión 2 de la
        Licencia, o (a su elección) cualquier versión posterior.
        """

        self.SetIcon(I.tava_png)
        self.SetName('TAVA')
        self.SetVersion('1.0')
        self.SetDescription(description)
        self.SetCopyright('(C) 2013 - 2014 Arsenio Ferreira')
        self.SetWebSite('http://www.tava.com.py')
        self.SetLicence(licence)
        self.AddDeveloper('Arsenio Ferreira')
        self.AddDeveloper('Abrahan Fretes')
        self.AddDocWriter('Arsenio Ferreira')
        self.AddDocWriter('Abrahan Fretes')
        self.AddTranslator('Arsenio Ferreira')

        wx.AboutBox(self)
