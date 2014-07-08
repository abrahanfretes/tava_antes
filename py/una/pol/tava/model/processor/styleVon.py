'''
Created on 28/06/2014

@author: abrahan
'''
from py.una.pol.tava.model.bd.entity import Resultado, Iteracion
from py.una.pol.tava.model.bd.entity import Individuo
from py.una.pol.tava.model.bd import abm
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

        resultado = Resultado()

        fOpen = open(path, 'r')
        resultado.nombre = os.path.basename(path)
        resultado.alias = __getAlias(proyecto)
        resultado.cantidadIteracion = int(__getValue__(fOpen.readline()))
        resultado.etiqueta1 = __getValue__(fOpen.readline())
        resultado.etiqueta2 = __getValue__(fOpen.readline())
        resultado.etiqueta3 = __getValue__(fOpen.readline())
        resultado.etiqueta4 = __getValue__(fOpen.readline())
        resultado.nombreProblema = __getValue__(fOpen.readline())
        countO = resultado.numeroObjetivo = int(__getValue__(fOpen.readline()))
        countV = resultado.numeroVariable = int(__getValue__(fOpen.readline()))
        resultado.poblacionInicial = int(__getValue__(fOpen.readline()))
        resultado.nombreVariables = __buildVariablesDefaul(countV, True)
        resultado.nombreObjetivos = __buildVariablesDefaul(countO, False)
        resultado.fechaAdd = date.today()

        proyecto.resultados.append(resultado)
        abm.add(proyecto)

        print resultado

        tiempoInicial = float(__getValue__(fOpen.readline()))
        iteTotal = resultado.cantidadIteracion
        iteSum = 0
        #t1 = time.time()
        while(iteSum < iteTotal):
            iteSum += 1

            iteracion = Iteracion()
            iteracion.inicioEjecucion = tiempoInicial
            iteracion.cantidadIndividuo = int(
                                    __getValue__(fOpen.readline()))

            unIndi = []
            listIndividuos = []
            indiTotal = iteracion.cantidadIndividuo
            indiSum = 0
            while(indiSum < indiTotal):
                indiSum += 1
                individuo = Individuo()

                lineaRead = fOpen.readline()
                unIndi = lineaRead.split("\t")

                individuo.identificador = int(unIndi[1])
                individuo.varDTLZ = float(unIndi[2 +
                        resultado.numeroVariable + resultado.numeroObjetivo])
                longV = 2 + resultado.numeroVariable
                individuo.variables = ",".join(unIndi[2:longV])
                longO = longV + resultado.numeroObjetivo
                individuo.objetivos = ",".join(unIndi[longV:longO])
                individuo.objetivos = __getObjetiosString(unIndi[longV:longO])
                individuo.identificador = unIndi[1]
                listIndividuos.append(individuo)

            iteracion.identificador = unIndi[0]
            iteracion.finEjecucion = float(
                                    __getValue__(fOpen.readline()))
            tiempoInicial = iteracion.finEjecucion
            iteracion.individuos = listIndividuos
            iteracion.resultado_id = resultado.id

            abm.add(iteracion)

        fOpen.close()
