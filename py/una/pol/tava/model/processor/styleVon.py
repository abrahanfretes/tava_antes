'''
Created on 28/06/2014

@author: abrahan
'''
from py.una.pol.tava.base.entity import Result, Iteration, Individual
from py.una.pol.tava.dao import dproject, diteration
from datetime import date
import os


def __getValue__(string):
    listaValores = string.split('\n')
    return listaValores[0]


def __getObjetiosString(listObjetivos):

    stringObjetivos = []
    for valor in listObjetivos:
        stringObjetivos.append(str(float.fromhex(valor)))

    return ",".join(stringObjetivos)


def __getAlias(proyecto):
    return 'file-' + str(len(proyecto.resultados) + 1)


def __buildVariablesDefaul(count, variable):

    variables = []
    key = ''

    if variable:
        key = 'Var_'
    else:
        key = 'Obj_'

    for var in range(count):
        variables.append(key + str(var + 1))

    return ','.join(variables)


def procesarArchivo(listFile, proyecto):

    for path in listFile:

        resultado = Result()

        fOpen = open(path, 'r')
        resultado.name = os.path.basename(path)
        resultado.alias = __getAlias(proyecto)
        resultado.iteration_count = int(__getValue__(fOpen.readline()))
        resultado.etiqueta1 = __getValue__(fOpen.readline())
        resultado.etiqueta2 = __getValue__(fOpen.readline())
        resultado.etiqueta3 = __getValue__(fOpen.readline())
        resultado.etiqueta4 = __getValue__(fOpen.readline())
        resultado.problem_name = __getValue__(fOpen.readline())
        countO = resultado.number_objectives = int(__getValue__(fOpen.
                                                                readline()))
        countV = resultado.number_variables = int(__getValue__(fOpen.
                                                               readline()))
        resultado.number_initial_population = int(__getValue__(fOpen.
                                                               readline()))
        resultado.name_variables = __buildVariablesDefaul(countV, True)
        resultado.name_objectives = __buildVariablesDefaul(countO, False)
        resultado.add_date = date.today()

        proyecto.resultados.append(resultado)
        dproject.upDate(proyecto)

        print resultado

        tiempoInicial = float(__getValue__(fOpen.readline()))
        iteTotal = resultado.iteration_count
        iteSum = 0
        #t1 = time.time()
        while(iteSum < iteTotal):
            iteSum += 1

            iteracion = Iteration()
            iteracion.execution_start = tiempoInicial
            iteracion.number_individuals = int(
                                    __getValue__(fOpen.readline()))

            unIndi = []
            listIndividuos = []
            indiTotal = iteracion.number_individuals
            indiSum = 0
            while(indiSum < indiTotal):
                indiSum += 1
                individuo = Individual()

                lineaRead = fOpen.readline()
                unIndi = lineaRead.split("\t")

                individuo.identifier = int(unIndi[1])
                individuo.varDTLZ = float(unIndi[2 +
                        resultado.number_variables +\
                        resultado.number_objectives])
                longV = 2 + resultado.number_variables
                individuo.variables = ",".join(unIndi[2:longV])
                longO = longV + resultado.number_objectives
                individuo.objectives = ",".join(unIndi[longV:longO])
                individuo.objectives = __getObjetiosString(unIndi[longV:longO])
                individuo.identifier = unIndi[1]
                listIndividuos.append(individuo)

            iteracion.identifier = unIndi[0]
            iteracion.execution_end = float(
                                    __getValue__(fOpen.readline()))
            tiempoInicial = iteracion.execution_end
            iteracion.individuos = listIndividuos
            iteracion.resultado_id = resultado.id

            diteration.add(iteracion)

        fOpen.close()
