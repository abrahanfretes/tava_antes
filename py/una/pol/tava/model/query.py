'''
Created on 27/06/2014

@author: afretes
'''
import base
from entity import Proyecto, Resultado
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
            filter_by(id=proyecto.id).all()


def getProjectById(idProyecto):
    return session.query(Proyecto).filter_by(id=idProyecto).first()


def getProjectByResult(resultado):
    return session.query(Proyecto).filter_by(id=resultado.proyecto_id).first()


#Querys para Resultado


def getAllResult():
    return session.query(Resultado).order_by(Resultado.nombre)


def getResultsByProject(proyecto):
    return session.query(Resultado).filter_by(proyecto_id=proyecto.id).all()


def getResultById(idResultado):
    return session.query(Resultado).filter_by(id=idResultado).first()
