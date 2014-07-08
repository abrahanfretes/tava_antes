'''
Created on 04/07/2014

@author: abrahan
'''
from pandas import read_csv
from pandas.tools.plotting import parallel_coordinates
from py.una.pol.tava.model.bd import query
import os

path = os.getcwd()
pathFileTemp = path + '/temp.csv'


def __getObjetivosOfIterations(listIteracion):

    individuos = []
    for ite in listIteracion:
        individuos.append(query.getIdenObjOfIndividuoByIteracion(ite))
    return individuos


def __getIden(iden):
    return ',iteracion-' + str(iden) + '\n'


def __getHeader(namesObjetives):
    return namesObjetives + ',Name\n'


def __getCsv(listIteracion, resultado):

    iteraciones = __getObjetivosOfIterations(listIteracion)
    f = open(pathFileTemp, 'w')

    f.write(__getHeader(resultado.nombreObjetivos))
    pos = 0
    for individuos in iteraciones:
        identificador = listIteracion[pos].identificador
        for individuo in individuos:
            linea = individuo.objetivos + __getIden(identificador)
            f.write(linea)
        pos += 1
    f.close()
    return pathFileTemp


def getAxis(axes, listIteration, resultado):

    df = read_csv(__getCsv(listIteration, resultado))
    return parallel_coordinates(df, 'Name', None, axes)
    #return 'Se genero: ' + __getCsv(listIteration, resultado)
