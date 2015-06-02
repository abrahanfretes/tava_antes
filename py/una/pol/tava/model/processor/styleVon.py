'''
Created on 28/06/2014

@author: abrahan
'''
from py.una.pol.tava.base.entity import Result, Iteration, Individual
from py.una.pol.tava.dao import dproject, diteration
from datetime import date
from py.una.pol.tava.base.tavac import correct, fos_error, fva_Error
from py.una.pol.tava.base import tavac as tvc
from py.una.pol.tava.dao import dmetric


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


def __converter(listFloat):
    list_string = []
    for i in listFloat:
        list_string.append(str(i))
    return ','.join(list_string)


def __getAlias(proyecto, count_result):
    return 'file-' + str(count_result)


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
        retorno = tvc.fio_error
    except:
        retorno = tvc.fuk_error
    finally:
        fOpen.close()

    return retorno


def quickCheckStyleMetric(path):
    retorno = correct

    try:
        fOpen = open(path, 'r')
        line = fOpen.readline()
        content = False

        while line != '' and not content:
            lv = line.split(',')
            if lv[0] == '*':
                while lv[0] == '*':
                    lv[1] = lv[1].split('p')[1]
                    lv[4] = lv[4].split('-')[0]
                    lv[6] = lv[6].split('H')[0]
                    line = fOpen.readline()
                    lv = line.split(',')
                    content = True
            else:
                line = fOpen.readline()
        fOpen.close()

        if not content:
            retorno = tvc.content_error
    except OSError:
        retorno = fos_error
    except ValueError:
        retorno = fva_Error
    except IOError:
        retorno = tvc.fio_error
    except:
        retorno = tvc.fuk_error
    finally:
        fOpen.close()

    return retorno


def procesarArchivo(listFile, proyecto):

    count_result = 0
    for path in listFile:
        count_result = count_result + 1

        resultado = Result()

        fOpen = open(path, 'r')
        resultado.name = tvc.getBaseName(path)
        resultado.alias = __getAlias(proyecto, count_result)
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
        # t1 = time.time()
        while(iteSum < iteTotal):
            iteSum += 1

            iteracion = Iteration()
            iteracion.execution_start = tiempoInicial
            iteracion.number_individuals = int(__getValue__(fOpen.readline()))

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
                                                 resultado.number_variables +
                                                 resultado.number_objectives])
                longV = 2 + resultado.number_variables
                individuo.variables = ",".join(unIndi[2:longV])
                longO = longV + resultado.number_objectives
                individuo.objectives = ",".join(unIndi[longV:longO])
                s_obj, f_obj = __getObjetiosString(unIndi[longV:longO])
                individuo.objectives = ",".join(s_obj)

                if list_min_indi != []:
                    for idx in range(len(f_obj)):
                        if f_obj[idx] < list_min_indi[idx]:
                            list_min_indi[idx] = f_obj[idx]
                        elif f_obj[idx] > list_max_indi[idx]:
                            list_max_indi[idx] = f_obj[idx]
                else:
                    for index in range(len(f_obj)):
                        list_min_indi.append(f_obj[index])
                        list_max_indi.append(f_obj[index])

                individuo.identifier = unIndi[1]
                listIndividuos.append(individuo)

            iteracion.objectives_min = __converter(list_min_indi)
            iteracion.objectives_max = __converter(list_max_indi)
            iteracion.identifier = unIndi[0]
            iteracion.execution_end = float(__getValue__(fOpen.readline()))
            tiempoInicial = iteracion.execution_end
            iteracion.individuals = listIndividuos
            iteracion.result_id = resultado.id

            diteration.add(iteracion)

        fOpen.close()
    return proyecto

from py.una.pol.tava.base.entity import MoeaProblem
from py.una.pol.tava.base.entity import NumberObjective
from py.una.pol.tava.base.entity import EvolutionaryMethod
from py.una.pol.tava.base.entity import NumberThreads
from py.una.pol.tava.base.entity import ParallelizationMethod
from py.una.pol.tava.base.entity import Metric
from py.una.pol.tava.base.entity import Population
from py.una.pol.tava.base.entity import ValueMetric


def processMetricsFile(paths, project):
    for path in paths:
        path_tmp, filename = tvc.createTmpFileForMetric(path)

        print 'inicio de insercion de informacion a base de datos'
        # Creamos archivos con valores
        parser_tem_file = open(path_tmp)
        line = parser_tem_file.readline()

        ob_problem = None
        ob_number_obj = None
        ob_method_evo = None
        ob_number_thread = None
        ob_method_parallel = None
        ob_metric = None
        ob_population = None

        list_number_obj = []
        list_method_evo = []
        list_number_thread = []
        list_method_parallel = []
        list_metric = []
        list_population = []
        list_value = []

        problem = ''
        number_obj = ''
        method_evo = ''
        number_thread = ''
        method_parallel = ''
        metric = ''
        population = ''
        count = 0

        while line != '':
            lv = line.split(',')

            if problem != lv[0]:
                #===============================================================
                # if ob_problem is not None:
                #     # ob_problem.number_objectives = list_number_obj
                #     dmetric.add(ob_number_obj)
                #===============================================================
                ob_problem = MoeaProblem()
                ob_problem.name = lv[0]
                ob_problem.name_file = filename
                ob_problem.project_id = project.id
                # ob_problem = dmetric.add(ob_problem)
                list_number_obj = ob_problem.number_objectives
                problem = lv[0]

            if number_obj != lv[1]:
                #===============================================================
                # if ob_number_obj is not None:
                #     ob_number_obj.evolutionary_methods = list_method_evo
                #     # dmetric.add(ob_number_obj)
                #===============================================================

                ob_number_obj = NumberObjective()
                ob_number_obj.value = lv[1]
                # ob_number_obj.moea_problem = ob_problem.id
                number_obj = lv[1]
                # ob_number_obj.evolutionary_methods = list_method_evo
                ob_number_obj = dmetric.add(ob_number_obj)
                list_number_obj.append(ob_number_obj)
                list_method_evo = ob_number_obj.evolutionary_methods

            if method_evo != lv[2]:
                # actualizo anterior
                #===============================================================
                # if ob_method_evo is not None:
                #     ob_method_evo.number_threadss = list_number_thread
                #     print 'add: ' + problem + ' -> ' + number_obj + ' -> ' + method_evo
                #     print str(count) + ' de 851765'
                #     # dmetric.add(ob_method_evo)
                #===============================================================

                ob_method_evo = EvolutionaryMethod()
                ob_method_evo.name = lv[2]
                method_evo = lv[2]
                # ob_method_evo.number_objective = ob_number_obj.id
                list_method_evo.append(ob_method_evo)
                list_number_thread = ob_method_evo.number_threadss

            if number_thread != lv[3]:
                #===============================================================
                # if ob_number_thread is not None:
                #     ob_number_thread.parallelization_methods = list_method_parallel
                #===============================================================

                ob_number_thread = NumberThreads()
                ob_number_thread.value = lv[3]
                number_thread = lv[3]
                list_number_thread.append(ob_number_thread)
                list_method_parallel = ob_number_thread.parallelization_methods

            if method_parallel != lv[4]:
                #===============================================================
                # if ob_method_parallel is not None:
                #     ob_method_parallel.metrics = list_metric
                #===============================================================

                ob_method_parallel = ParallelizationMethod()
                ob_method_parallel.name = lv[4]
                list_method_parallel.append(ob_method_parallel)
                method_parallel = lv[4]
                list_metric = ob_method_parallel.metrics

            if metric != lv[5]:
                #===============================================================
                # if ob_metric is not None:
                #     ob_metric.populations = list_population
                #===============================================================
                ob_metric = Metric()
                ob_metric.name = lv[5]
                list_metric.append(ob_metric)
                metric = lv[5]
                list_population = ob_metric.populations

            if population != lv[6]:
                #===============================================================
                # if ob_population is not None:
                #     ob_population.value_metrics = list_value
                #===============================================================

                ob_population = Population()
                ob_population.value = lv[6]
                list_population.append(ob_population)
                population = lv[6]
                list_value = ob_population.value_metrics

            ob_value = ValueMetric()
            ob_value.iteration = lv[7]
            ob_value.value = float((lv[8].split(' '))[0])
            list_value.append(ob_value)

            count += 1
            line = parser_tem_file.readline()

        if ob_problem is not None:
            ob_problem.number_objectives = list_number_obj
            print' init update datas'
            dmetric.add(ob_problem)
            print' terminate update datas'

        parser_tem_file.close()
        print 'finalizacion de insercion de informacion a base de datos'

    return project
