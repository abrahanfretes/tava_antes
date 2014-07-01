'''
Created on 28/06/2014

@author: abrahan
'''
from py.una.pol.tava.model.entity import Resultado, Iteracion
from py.una.pol.tava.model.entity import Individuo, Objetivo, Variable
from py.una.pol.tava.model import abm
from datetime import date


def __getPrimerValor__(string):
    listaValores = string.split('\n')
    return listaValores[0]


def procesarArchivo(listFile, proyecto):

    for path in listFile:
        resultado = Resultado()

        fOpen = open(path, 'r')
        resultado.nombre = fOpen.name()
        resultado.cantidadIteracion = int(__getPrimerValor__(fOpen.readline()))
        resultado.etiqueta1 = __getPrimerValor__(fOpen.readline())
        resultado.etiqueta2 = __getPrimerValor__(fOpen.readline())
        resultado.etiqueta3 = __getPrimerValor__(fOpen.readline())
        resultado.etiqueta4 = __getPrimerValor__(fOpen.readline())
        resultado.nombreProblema = __getPrimerValor__(fOpen.readline())
        resultado.numeroObjetivo = int(__getPrimerValor__(fOpen.readline()))
        resultado.numeroVariable = int(__getPrimerValor__(fOpen.readline()))
        resultado.poblacionInicial = int(__getPrimerValor__(fOpen.readline()))
        resultado.fechaAdd = date.today(__getPrimerValor__(fOpen.readline()))

        proyecto.resultados.append(resultado)
        abm.add(proyecto)

        tiempoInicial = float(__getPrimerValor__(fOpen.readline()))
        for ite in range(resultado.cantidadIteracion):

            iteracion = Iteracion()
            iteracion.inicioEjecucion = tiempoInicial
            iteracion.cantidadIndividuo = int(
                                    __getPrimerValor__(fOpen.readline()))

            listaElement = []
            listIndividuos = []
            for indi in range(iteracion.cantidadIndividuo):

                individuo = Individuo()

                lineaRead = fOpen.readline()
                listaElement = lineaRead.split("\t")

                individuo.identificador = int(listaElement[1])
                individuo.varDTLZ = int(listaElement[2 +
                        resultado.numeroVariable + resultado.numeroObjetivo])

                orden = 0
                corteVariable = 2 + resultado.numeroVariable
                listVariables = []
                for valor in listaElement[2:corteVariable]:
                    variable = Variable(orden, float(valor))
                    listVariables.append(variable)
                    orden += 1

                individuo.variables = listVariables

                orden = 0
                corteObjetivo = corteVariable + resultado.numeroObjetivo
                listObjetivos = []
                for valor in listaElement[corteVariable:corteObjetivo]:
                    objetivo = Objetivo(orden, float.fromhex(valor))
                    listObjetivos.append(objetivo)
                    orden += 1

                individuo.objetivos = listObjetivos

                listIndividuos.append(individuo)

            iteracion.identificador = listaElement[0]
            iteracion.finEjecucion = float(
                                    __getPrimerValor__(fOpen.readline()))
            tiempoInicial = iteracion.finEjecucion
            iteracion.individuos = listIndividuos

        fOpen.close()
