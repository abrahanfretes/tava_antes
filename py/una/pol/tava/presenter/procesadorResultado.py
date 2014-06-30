'''
Created on 28/06/2014

@author: abrahan
'''
from py.una.pol.tava.model.entity import Resultado
from datetime import date


def procesarArchivo(path):
    resultado = Resultado('resultado2', 20, 'etiqueta1', 'etiqueta2',
                          'etiqueta3', 'etiqueta4', 'nombreProblema', 10, 14,
                          800, date.today())
    return resultado
