# -*- coding: utf-8 -*-
'''
Created on 27/06/2014

@author: afretes
'''


from sqlalchemy import Column, Integer, String, Date, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
import base


Base = base.getBase()


class Proyecto(Base):
    '''
    Entidad Proyecto
    estado: SmallInteger,
            0 = abierto
            1 = cerrado
    '''

    __tablename__ = 'proyecto'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    estado = Column(SmallInteger)
    fecha = Column(Date())

    resultados = relationship('Resultado', \
                              order_by='Resultado.id', backref='proyecto')

    def __init__(self, nombre, estado, fecha):
        '''
        :param nombre:
        :param estado:
        :param fecha:
        '''

        self.nombre = nombre
        self.estado = estado
        self.fecha = fecha

    def __repr__(self):
        return "<Proyecto(nombre='%s', estado='%s', fecha de creacion='%s')>"\
              % (self.nombre, self.estado, self.fecha)


class Resultado(Base):

    __tablename__ = 'resultado'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    cantidadIteracion = Column(Integer)
    etiqueta1 = Column(String(100))
    etiqueta2 = Column(String(100))
    etiqueta3 = Column(String(100))
    etiqueta4 = Column(String(100))
    nombreProblema = Column(String(100))
    numeroObjetivo = Column(Integer)
    numeroVariable = Column(Integer)
    poblacionInicial = Column(Integer)
    fechaAdd = Column(Date())
    proyecto_id = Column(Integer, ForeignKey('proyecto.id'))

    #==========================================================================
    # proyecto = relationship('Proyecto',\
    #                         backref=backref('resultados', order_by=id))
    #==========================================================================

    def __init__(self, nombre, iteracion, etiqueta1, etiqueta2, etiqueta3,\
                 etiqueta4, nombreProblema, numeroObjetivo, numeroVariable,\
                 poblacionInicial, fechaAdd):
        '''
        Constructor
        '''
        self.nombre = nombre
        self.cantidadIteracion = iteracion
        self.etiqueta1 = etiqueta1
        self.etiqueta2 = etiqueta2
        self.etiqueta3 = etiqueta3
        self.etiqueta4 = etiqueta4
        self.nombreProblema = nombreProblema
        self.numeroObjetivo = numeroObjetivo
        self.numeroVariable = numeroVariable
        self.poblacionInicial = poblacionInicial
        self.fechaAdd = fechaAdd

    def __repr__(self):
        return "<Resultados(nombre='%s', cantidadIteracion='%s', \
        etiqueta1='%s', etiqueta2='%s', etiqueta3='%s', etiqueta4='%s', \
        nombreProblema='%s', numeroObjetivo='%s', numeroVariable='%s', \
        poblacionInicial='%s', fechaAdd='%s')>" % (self.nombre,
        self.cantidadIteracion, self.etiqueta1, self.etiqueta2, self.etiqueta3,
        self.etiqueta4, self.nombreProblema, self.numeroObjetivo,
        self.numeroVariable, self.poblacionInicial, self.fechaAdd)


def createDB():

    base.createDb()
