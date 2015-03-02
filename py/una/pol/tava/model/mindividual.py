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

    def createFiles(self, ite, mode, v_objectives):

        #crear el archivo y
        file_obj = os.path.join(gtd(), str(ite) + '.mode.' + mode + '.csv')
        file_var_d = os.path.join(gtd(), str(ite) + '.mode.' + mode + '.var')
        file_obj_d = os.path.join(gtd(), str(ite) + '.mode.' + mode + '.obj')
        f = open(file_obj, 'w')
        f_var = open(file_var_d, 'w')
        f_obj = open(file_obj_d, 'w')

        #obtengo lista y cabecera
        obj_name, ident, obj_list, var_list = self.getObjByIteration(ite)

        list_obj = v_objectives.split(',')
        if list_obj.count('0'):
            index_one = []
            for i in range(len(list_obj)):
                if list_obj[i] == '1':
                    index_one.append(i)
            #agrego cabecera
            f.write(self.getLineObj(obj_name, index_one) + ',Name\n')
            #agrego la lista
            for index in range(len(obj_list)):
                f.write(self.getLineObj(obj_list[index], index_one)
                        + ',' + str(ident) + '\n')
                f_obj.write(str(index) + ',' + obj_list[index] + '\n')
                f_var.write(str(index) + ',' + var_list[index] + '\n')
        else:
            #agrego cabecera
            f.write(obj_name + ',Name\n')
            #agrego la lista
            for index in range(len(obj_list)):
                f.write(obj_list[index] + ',' + str(ident) + '\n')
                f_obj.write(str(index) + ',' + obj_list[index] + '\n')
                f_var.write(str(index) + ',' + var_list[index] + '\n')

        f.close()
        f_var.close()
        f_obj.close()

    def getLineObj(self, var, list_obj):
        var_aux = var.split(',')
        to_ret = []
        for i in list_obj:
            to_ret.append(var_aux[i])
        return ','.join(to_ret)

    def deleteFile(self, ite_id, mode):

        file_obj = os.path.join(gtd(), str(ite_id) + '.mode.' + mode + '.csv')
        if os.path.isfile(file_obj):
            os.remove(file_obj)

    def  getCsv(self, ite_id, mode):
        file_obj = os.path.join(gtd(), str(ite_id) + '.mode.' + mode + '.csv')
        return read_csv(file_obj)

    def  getVar(self, ite, mode):
        return self.redFile(ite, mode, 'var')

    def  getObj(self, ite, mode):
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

    def createFilesWithFilter(self, ite, mode, filters):

        #crear el archivo y
        file_obj = os.path.join(gtd(), str(ite) + '.mode.' + mode + '.csv')
        file_var_d = os.path.join(gtd(), str(ite) + '.mode.' + mode + '.var')
        file_obj_d = os.path.join(gtd(), str(ite) + '.mode.' + mode + '.obj')
        f = open(file_obj, 'w')
        f_var = open(file_var_d, 'w')
        f_obj = open(file_obj_d, 'w')

        #obtengo lista y cabecera
        obj_name, ident, objs, vars_r = self.getObjByIteration(ite)

        #agrego cabecera
        f.write(obj_name + ',Name\n')
        #agrego la lista

        ind = 0
        for index in range(len(objs)):

            to_write = True

            i = 0
            for obj in objs[index].split(','):
                if float(obj) < filters[i][0] or float(obj) > filters[i][1]:
                    to_write = False
                    break
                i += 1

            if(to_write):
                f.write(objs[index] + ',' + str(ident) + '\n')
                f_obj.write(str(ind) + ',' + objs[index] + '\n')
                f_var.write(str(ind) + ',' + vars_r[index] + '\n')
                ind += 1

            else:
                to_write = True

        f.close()
        f_var.close()
        f_obj.close()

    def getMinMax(self, ite_id, mode):
        min_v = []
        max_v = []

        filepath = os.path.join(gtd(), str(ite_id) + '.mode.' + mode + '.obj')
        f = open(filepath)

        #======================================================================
        # f.readline()
        #======================================================================
        ind = f.readline()
        while ind != '':
            if min_v != []:
                index = 0
                for obj_aux in ind.split(',')[1:]:
                    if float(obj_aux) < min_v[index]:
                        min_v[index] = float(obj_aux)
                    if float(obj_aux) > max_v[index]:
                        max_v[index] = float(obj_aux)
                    index += 1
            else:
                for obj in ind.split(',')[1:]:
                    min_v.append(float(obj))
                    max_v.append(float(obj))
            ind = f.readline()

        f.close()
        return min_v, max_v
