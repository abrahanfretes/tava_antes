'''
Created on 27/06/2014

@author: afretes
'''
import base
from entity import Proyecto, Resultado, Iteracion, Individuo
from sqlalchemy.orm import subqueryload
#==============================================================================
# SQL>>> jack = session.query(User).\
# ...                 options(subqueryload(User.addresses)).\
# ...                 filter_by(name='jack').one()
#==============================================================================

session = base.getSession()

#Querys para Proyectos


def getAllProject():
    return session.query(Proyecto).order_by(Proyecto.fecha, Proyecto.estado)


def getAllProjectWithResults():
    return session.query(Proyecto).options(subqueryload(Proyecto.resultados))


def getProjectWithResults(proyecto):

    return session.query(Proyecto).options(subqueryload(Proyecto.resultados)).\
            filter_by(id=proyecto.id).first()


def getProjectById(idProyecto):
    return session.query(Proyecto).filter_by(id=idProyecto).first()


def getProjectByResult(resultado):
    return session.query(Proyecto).filter_by(id=resultado.proyecto_id).first()


def getAllNamesProject():
    return session.query(Proyecto.nombre).order_by(Proyecto.nombre).all()

#Querys para Resultado


def getAllResult():
    return session.query(Resultado).order_by(Resultado.nombre).all()


def getResultsByProject(proyecto):
    return session.query(Resultado).filter_by(proyecto_id=proyecto.id).all()


def getResultById(idResultado):
    return session.query(Resultado).filter_by(id=idResultado).first()


def getResultWithIterations(resultado):
    return session.query(Resultado).options(
            subqueryload(Resultado.iteraciones)).\
            filter_by(id=resultado.id).first()


#Querys para Iteracion

def getIterationsByResult(resultado):
    return session.query(Iteracion).order_by(Iteracion.id).\
                        filter_by(id=resultado.id).all()


def getIterationsByIdResult(resultadoId):
    return session.query(Iteracion).order_by(Iteracion.id).\
                        filter_by(id=resultadoId).all()


def getIterationById(idIteracion):
    return session.query(Iteracion).filter_by(id=idIteracion).first()


def getIterationWithIndividuo(idIteracion):
    return session.query(Iteracion).options(
            subqueryload(Iteracion.individuos)).\
            filter_by(id=idIteracion).first()


#Querys para Individuo


def getIndividuosByIteracion(iteracion):
    return session.query(Individuo).order_by(Individuo.identificador).\
                            filter_by(iteracion_id=iteracion.id).all()


def getIndividuosByIteracionId(idIteracion):
    return session.query(Individuo).order_by(Individuo.identificador).\
                            filter_by(iteracion_id=idIteracion).all()


def getIdenVarOfIndividuo(idIteracion):
    return session.query(Individuo.identificador, Individuo.variables).\
                            order_by(Individuo.identificador).\
                            filter_by(iteracion_id=idIteracion).all()


def getIdenObjOfIndividuo(idIteracion):
    return session.query(Individuo.identificador, Individuo.objetivos).\
                            order_by(Individuo.identificador).\
                            filter_by(iteracion_id=idIteracion).all()


def getIdenObjOfIndividuoByIteracion(iteracion):
    return session.query(Individuo.identificador, Individuo.objetivos).\
                            order_by(Individuo.identificador).\
                            filter_by(iteracion_id=iteracion.id).all()


def getIdenObjVarOfIndividuo(idIteracion):
    return session.query(Individuo.identificador, Individuo.objetivos,
                    Individuo.variables).order_by(Individuo.identificador).\
                            filter_by(iteracion_id=idIteracion).all()


def getVarDTLZOfIndividuo(idIteracion):
    return session.query(Individuo.identificador, Individuo.varDTLZ).\
                            rder_by(Individuo.identificador).\
                            filter_by(iteracion_id=idIteracion).all()
