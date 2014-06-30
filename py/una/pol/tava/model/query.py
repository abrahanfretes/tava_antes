'''
Created on 27/06/2014

@author: afretes
'''
import base
from entity import Proyecto, Resultado

session = base.getSession()

#Querys para Resultado


def getProyectos():
    return session.query(Proyecto).order_by(Proyecto.fecha, Proyecto.estado)


def getProyectoById(idProyecto):
    return session.query(Proyecto).filter_by(id=idProyecto).first()


def getProyectoByResultado(resultado):
    return session.query(Proyecto).filter_by(id=resultado.proyecto_id).first()

#Querys para Resultado


def getResultadosByProyecto(proyecto):
    return session.query(Resultado).filter_by(proyecto_id=proyecto.id).all()


def getResultadoById(idResultado):
    return session.query(Resultado).filter_by(id=idResultado).first()
