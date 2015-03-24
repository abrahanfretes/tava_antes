'''
Created on 03/07/2014

@author: abrahan
'''
import os
from pandas import read_csv

from py.una.pol.tava.dao import dindividual
from py.una.pol.tava.model.miteration import InterationModel as im
from py.una.pol.tava.model.mresult import ResultModel as rm
from py.una.pol.tava.base.tavac import getTavaDirectory as gtd
from numpy.distutils.npy_pkg_config import VariableSet


class IndividualModel(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    def getIndividualById(self, id_individual):
        return dindividual.getIndividualById(id_individual)

    def getObjectivesIndividualById(self, id_individual):
        return dindividual.getObjectivesIndividualById(id_individual)[0]

    def getIndividualsByIteracionId(self, id_iteration):
        return dindividual.getIndividualsByIteracionId(id_iteration)

    def getIndividualsByListIterationId(self, list_id_iteration):

        individual = []
        for id_ite in list_id_iteration:
            individual.append(dindividual.getIndividualsByIteracionId(id_ite))
        return individual

    def getIdentifierAndVariableOfIndividual(self, list_id_iteration):

        individual = []
        for id_ite in list_id_iteration:
            individual.\
            append(dindividual.getIdentifierAndVariableOfIndividual(id_ite))
        return individual

    def getIdentifierAndObjectiveOfIndividual(self, list_id_iteration):

        individual = []
        for id_ite in list_id_iteration:
            individual.\
            append(dindividual.getIdentifierAndObjectiveOfIndividual(id_ite))
        return individual

    def getIdentifierObjectiveVariableOfIndividual(self, list_id_iteration):

        individual = []
        for id_ite in list_id_iteration:
            individual.append(dindividual.\
                            getIdentifierObjectiveVariableOfIndividual(id_ite))
        return individual

    def getVarDTLZOfIndividual(self, list_id_iteration):

        individual = []
        for idIte in list_id_iteration:
            individual.append(dindividual.getVarDTLZOfIndividual(idIte))
        return individual

    def getVarByIterations(self, list_id):
        toRet = []
        key = 1
        for individuals in self.getIndividualsByListIterationId(list_id):
            for indi in individuals:
                indi = indi
                var = str(key) + ',' + indi.variables
                toRet.append(var.split(','))
                key += 1

        return toRet

    def getObjByIteration(self, ite_id):
        to_ret_obj = []
        to_ret_var = []
        ite = im().getIterationById(ite_id)
        res = rm().getResultById(ite.result_id)

        for ind in self.getIndividualsByIteracionId(ite_id):
            to_ret_obj.append(ind.objectives)
            to_ret_var.append(ind.variables)

        return res.name_objectives, ite.identifier, to_ret_obj, to_ret_var

    def createFiles(self, ite, mode, v_objectives, v_order,
                    order_name_obj, max_objetive, min_objetive):

        obj_orders_var = []

        # obtengo lista y cabecera de la base de datos
        obj_name, ident, obj_list, var_list = self.getObjByIteration(ite)

        # obtiene los datos filtratdos por objetivos
        list_obj = v_objectives.split(',')
        obj_filters = []
        if list_obj.count('0'):
            index_one = []
            for i in range(len(list_obj)):
                if list_obj[i] == '1':
                    index_one.append(i)
                    obj_orders_var.append(i)

            obj_name = self.getLineFilters(obj_name, index_one)

            for index in range(len(obj_list)):
                obj_filters.append(self.getLineFilters(obj_list[index],
                                                       index_one))
        else:
            obj_filters = obj_list

        # obtiene los datos ordenados
        orders = [int(i) for i in v_order.split(',')]
        obj_orders = []
        if(not orders == sorted(orders)):
            obj_name = self.getLineOrders(obj_name, obj_orders_var, orders)
            for obj in obj_filters:
                obj_orders.append(self.getLineOrders(obj,
                                                     obj_orders_var, orders))
        else:
            obj_orders = obj_filters

        # agrego filtros si es distinto a None(debe modifiar todos los archivo)
        # debe modificar tanto los valores objetivos como los de Variables
        obj_order_filter = []
        var_order_filter = []
        if(not (max_objetive is None) and not (min_objetive is None)):
            for index in range(len(obj_orders)):
                to_write = True
                value = [float(i) for i in obj_orders[index].split(',')]
                for i in range(len(value)):
                    if min_objetive[i] > value[i] or\
                            value[i] > max_objetive[i]:
                        to_write = False
                        break

                if(to_write):
                    obj_order_filter.append(obj_orders[index])
                    var_order_filter.append(var_list[index])
        else:
            obj_order_filter = obj_orders
            var_order_filter = var_list

        # escribe los datos en archivo
        file_obj = os.path.join(gtd(), str(ite) + '.mode.' + mode + '.csv')
        file_var_d = os.path.join(gtd(), str(ite) + '.mode.' + mode + '.var')
        file_obj_d = os.path.join(gtd(), str(ite) + '.mode.' + mode + '.obj')
        f = open(file_obj, 'w')
        f_var = open(file_var_d, 'w')
        f_obj = open(file_obj_d, 'w')

        # agrego cabecera
        f.write(order_name_obj + ',Name\n')
        # agrego la lista
        for index in range(len(obj_order_filter)):
            f.write(obj_order_filter[index] + ',' + str(ident) + '\n')
            f_obj.write(str(index) + ',' + obj_order_filter[index] + '\n')
            f_var.write(str(index) + ',' + var_order_filter[index] + '\n')

        f.close()
        f_var.close()
        f_obj.close()

    def getLineFilters(self, var, list_obj):
        var_aux = var.split(',')
        to_ret = []
        for i in list_obj:
            to_ret.append(var_aux[i])
        return ','.join(to_ret)

    def getLineOrders(self, var, ordered, for_order):
        var_aux = var.split(',')
        to_ret = []
        for i in for_order:
            to_ret.append(var_aux[ordered.index(i)])

        return ','.join(to_ret)

    def getCsv(self, ite_id, mode):
        file_obj = os.path.join(gtd(), str(ite_id) + '.mode.' + mode + '.csv')
        return read_csv(file_obj)

    def getVar(self, ite, mode):
        return self.redFile(ite, mode, 'var')

    def getObj(self, ite, mode):
        return self.redFile(ite, mode, 'obj')

    def redFile(self, ite, mode, ext):

        to_ret = []
        filepath = os.path.join(gtd(), str(ite) + '.mode.' + mode + '.' + ext)
        f = open(filepath)

        ind = f.readline()
        while ind != '':
            to_ret.append(ind.split(','))
            ind = f.readline()

        f.close()
        return to_ret

    def fileExists(self, ite_id, mode):
        file_obj = os.path.join(gtd(), str(ite_id) + '.mode.' + mode + '.csv')
        return os.path.isfile(file_obj)

    def fileDelete(self, ite_id, mode):
        file_obj = os.path.join(gtd(), str(ite_id) + '.mode.' + mode + '.csv')
        if os.path.isfile(file_obj):
            os.remove(file_obj)

    def getMinMax(self, ite_id, mode):
        min_v = []
        max_v = []

        filepath = os.path.join(gtd(), str(ite_id) + '.mode.' + mode + '.obj')
        f = open(filepath)

        ind = f.readline()
        if ind != '':
            for obj in ind.split(',')[1:]:
                min_v.append(float(obj))
                max_v.append(float(obj))

        ind = f.readline()
        while ind != '':
            index = 0
            for obj_aux in ind.split(',')[1:]:
                if float(obj_aux) < min_v[index]:
                    min_v[index] = float(obj_aux)
                if float(obj_aux) > max_v[index]:
                    max_v[index] = float(obj_aux)
                index += 1
            ind = f.readline()

        f.close()
        return min_v, max_v

# -------------------------------------------------------------------
# Clases usadas para Parallel Grafic GF
# -------------------------------------------------------------------
    def createFileTestGF(self, ite_list):
        mode = str(1)
        type_gf = str(1)
        filepath = os.path.join(gtd(),
                                'type.' + type_gf + '.mode.' + mode + '.csv')
        f_test = open(filepath, 'w')

        print ite_list
        # agrego cabecera
        ite_h = im().getIterationById(ite_list[0])
        # obtener result
        res_h = rm().getResultById(ite_h.result_id)
        f_test.write(res_h.name_objectives + ',Name\n')

        # por cada iteracion
        for i in ite_list:
            # obtener la iteracion
            ite = im().getIterationById(i)
            # obtener result
            res = rm().getResultById(ite.result_id)
            # obtener individuos
            inds = self.getIndividualsByIteracionId(ite.id)
            # escribir archivo
            for ind in inds:
                f_test.write(ind.objectives
                             + ',' + res.alias
                             + '_' + str(ite.identifier) + '\n')
        f_test.close()

    def createFileResultGF(self, ite_list):
        mode = str(1)
        type_gf = str(2)

        # por cada lista de iteraciones
        for i_list in ite_list:

            # ----- por cada resultado ---------
            # obtener la iteracion
            ite = im().getIterationById(i_list[0])
            res = rm().getResultById(ite.result_id)
            filepath = os.path.join(gtd(), str(ite.result_id) + '.'
                                    + 'type.' + type_gf
                                    + '.mode.' + mode
                                    + '.csv')
            f_test = open(filepath, 'w')
            f_test.write(res.name_objectives + ',Name\n')

            # ----- por cada iteracion ---------
            for i in i_list:
                ite = im().getIterationById(i)
                inds = self.getIndividualsByIteracionId(ite.id)
                for ind in inds:
                    f_test.write(ind.objectives
                                 + ',' + res.alias
                                 + '_' + str(ite.identifier) + '\n')
            f_test.close()

    def createFileIterationtGF(self, ite_list):
        mode = str(1)
        type_gf = str(3)

        # por cada lista de iteraciones
        for i in ite_list:

            # ----- por cada resultado ---------
            # obtener la iteracion
            ite = im().getIterationById(i)
            res = rm().getResultById(ite.result_id)
            inds = self.getIndividualsByIteracionId(ite.id)
            filepath = os.path.join(gtd(), str(i) + '.'
                                    + 'type.' + type_gf
                                    + '.mode.' + mode
                                    + '.csv')
            f_test = open(filepath, 'w')
            f_test.write(res.name_objectives + ',Name\n')

            # ----- por cada iteracion ---------
            for ind in inds:
                f_test.write(ind.objectives
                             + ',' + res.alias
                             + '_' + str(ite.identifier) + '\n')
            f_test.close()

    def createFileTestGF1(self, ite_list):
        mode = str(1)
        type_gf = str(1)

        # por cada iteracion
        for i in ite_list:

            # obtener la iteracion
            ite = im().getIterationById(i)
            # obtener result
            res = rm().getResultById(ite.result_id)
            # obtener individuos
            inds = self.getIndividualsByIteracionId(ite.id)

            # abro un archivo
            filepath = os.path.join(gtd(), str(i) + '.'
                                    + 'type.' + type_gf
                                    + '.mode.' + mode
                                    + '.csv')
            f_test = open(filepath, 'w')
            f_test.write(res.name_objectives + ',Name\n')

            # escribir archivo
            for ind in inds:
                f_test.write(ind.objectives
                             + ',' + res.alias
                             + '_' + str(ite.identifier) + '\n')
            f_test.close()

    def getCsvForTest(self):
        mode = str(1)
        type_gf = str(1)
        filepath = os.path.join(gtd(),
                                'type.' + type_gf + '.mode.' + mode + '.csv')
        return read_csv(filepath)

    def getCsvForResult(self, i_list):
        mode = str(1)
        type_gf = str(2)
        ite = im().getIterationById(i_list[0])
        filepath = os.path.join(gtd(), str(ite.result_id) + '.'
                                + 'type.' + type_gf
                                + '.mode.' + mode
                                + '.csv')
        return read_csv(filepath)

    def getCsvForIteration(self, iteration):
        mode = str(1)
        type_gf = str(3)
        filepath = os.path.join(gtd(), str(iteration) + '.'
                                + 'type.' + type_gf
                                + '.mode.' + mode
                                + '.csv')
        return read_csv(filepath)
