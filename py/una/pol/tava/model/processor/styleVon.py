'''
Created on 28/06/2014

@author: abrahan
'''
from py.una.pol.tava.base.entity import Result, Iteration, Individual
from py.una.pol.tava.dao import dproject, diteration
from datetime import date
from py.una.pol.tava.base.tavac import correct, fos_error, fva_Error
from py.una.pol.tava.base.tavac import fio_error, fuk_error
import os


def __getValue__(string):
    listaValores = string.split('\n')
    return listaValores[0]


def __getObjetiosString(listObjetivos):

    stringObjetivos = []
    floatObjetivos = []
    for valor in listObjetivos:
        stringObjetivos.append(str(float.fromhex(valor)))
        floatObjetivos.append(float.fromhex(valor))

    return stringObjetivos, floatObjetivos


def  __converter(listFloat):
    list_string = []
    for i in listFloat:
        list_string.append(str(i))
    return ','.join(list_string)


def __getAlias(proyecto):
    return 'file-' + str(len(proyecto.results) + 1)


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


def fastVerification(path):
    retorno = correct

    try:
        fOpen = open(path, 'r')
        int(__getValue__(fOpen.readline()))
        __getValue__(fOpen.readline())
        __getValue__(fOpen.readline())
        __getValue__(fOpen.readline())
        __getValue__(fOpen.readline())
        __getValue__(fOpen.readline())
        int(__getValue__(fOpen.readline()))
        int(__getValue__(fOpen.readline()))
        int(__getValue__(fOpen.readline()))
        float(__getValue__(fOpen.readline()))

    except OSError:
        retorno = fos_error
    except ValueError:
        retorno = fva_Error
    except IOError:
        retorno = fio_error
    except:
        retorno = fuk_error
    finally:
        fOpen.close()

    return retorno


def procesarArchivo(listFile, proyecto):

    for path in listFile:

        resultado = Result()

        fOpen = open(path, 'r')
        resultado.name = os.path.basename(path)
        resultado.alias = __getAlias(proyecto)
        resultado.iteration_count = int(__getValue__(fOpen.readline()))
        resultado.label1 = __getValue__(fOpen.readline())
        resultado.label2 = __getValue__(fOpen.readline())
        resultado.label3 = __getValue__(fOpen.readline())
        resultado.label4 = __getValue__(fOpen.readline())
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

        proyecto.results.append(resultado)
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
            list_min_indi = []
            list_max_indi = []
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
                s_obj, f_obj = __getObjetiosString(unIndi[longV:longO])
                individuo.objectives = ",".join(s_obj)

                if list_min_indi != []:
                    idx = 0
                    for obj in f_obj:
                        if obj < list_min_indi[idx]:
                            list_min_indi[idx] = obj
                        elif obj > list_max_indi[idx]:
                            list_max_indi[idx] = obj
                else:
                    list_min_indi = list_max_indi = f_obj

                individuo.identifier = unIndi[1]
                listIndividuos.append(individuo)

            iteracion.objectives_min = __converter(list_min_indi)
            iteracion.objectives_max = __converter(list_min_indi)
            iteracion.identifier = unIndi[0]
            iteracion.execution_end = float(
                                    __getValue__(fOpen.readline()))
            tiempoInicial = iteracion.execution_end
            iteracion.individuals = listIndividuos
            iteracion.result_id = resultado.id

            diteration.add(iteracion)

        fOpen.close()
    return proyecto
