'''
Created on 28/06/2014

@author: abrahan
'''
from py.una.pol.tava.model.entity import Resultado, Iteracion
from py.una.pol.tava.model.entity import Individuo
from py.una.pol.tava.model import abm
from datetime import date
import os


def __getPrimerValor__(string):
    listaValores = string.split('\n')
    return listaValores[0]


def __getObjetiosString(listObjetivos):

    stringObjetivos = []
    for valor in listObjetivos:
        stringObjetivos.append(str(float.fromhex(valor)))

    return ",".join(stringObjetivos)


def procesarArchivo(listFile, proyecto):

    for path in listFile:

        resultado = Resultado()

        fOpen = open(path, 'r')
        resultado.nombre = os.path.basename(path)
        resultado.cantidadIteracion = int(__getPrimerValor__(fOpen.readline()))
        resultado.etiqueta1 = __getPrimerValor__(fOpen.readline())
        resultado.etiqueta2 = __getPrimerValor__(fOpen.readline())
        resultado.etiqueta3 = __getPrimerValor__(fOpen.readline())
        resultado.etiqueta4 = __getPrimerValor__(fOpen.readline())
        resultado.nombreProblema = __getPrimerValor__(fOpen.readline())
        resultado.numeroObjetivo = int(__getPrimerValor__(fOpen.readline()))
        resultado.numeroVariable = int(__getPrimerValor__(fOpen.readline()))
        resultado.poblacionInicial = int(__getPrimerValor__(fOpen.readline()))
        resultado.fechaAdd = date.today()

        proyecto.resultados.append(resultado)
        abm.add(proyecto)

        print resultado

        tiempoInicial = float(__getPrimerValor__(fOpen.readline()))
        iteTotal = resultado.cantidadIteracion
        iteSum = 0
        #t1 = time.time()
        while(iteSum < iteTotal):
            iteSum += 1

            iteracion = Iteracion()
            iteracion.inicioEjecucion = tiempoInicial
            iteracion.cantidadIndividuo = int(
                                    __getPrimerValor__(fOpen.readline()))

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
                                    __getPrimerValor__(fOpen.readline()))
            tiempoInicial = iteracion.finEjecucion
            iteracion.individuos = listIndividuos
            iteracion.resultado_id = resultado.id

            abm.add(iteracion)

        fOpen.close()
