# -*- coding: utf-8 -*-
'''
Created on 27/06/2014

@author: afretes
'''


from sqlalchemy import Column, Integer, String, Date, ForeignKey, SmallInteger
from sqlalchemy import Float
from sqlalchemy.orm import relationship
import base


Base = base.getBase()
OPEN = 0
CLOSED = 1
HIDDEN = 2


class Proyecto(Base):
    '''
    Entidad Proyecto, clase mapeada a una base de datos con nombre "proyecto"
    :param nombre: String(100), regitra el nombre de un proyecto
    :param estado: SmallInteger, regitra el estado de un proyecto, valores
            posibles:
            0 = abierto
            1 = cerrado
    :param fecha: Date, regitra la fecha de creación de un proyecto
    '''

    __tablename__ = 'proyecto'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    nombre = Column(String(100))
    estado = Column(SmallInteger)
    fecha = Column(Date())

    resultados = relationship('Resultado',
                              cascade="save-update, merge, delete",
                              order_by='Resultado.id', backref='proyecto')

    def __init__(self, nombre, estado, fecha):

        self.nombre = nombre
        self.estado = estado
        self.fecha = fecha

    def __repr__(self):
        return "<Proyecto(nombre='%s', estado='%s', fecha de creacion='%s')>"\
              % (self.nombre, self.estado, self.fecha)


class Resultado(Base):
    '''
    Entidad Resultado, clase mapeada a una base de datos con nombre "resultado"
    :param nombre: String(100), regitra el nombre de un archivo resultado.
    :param alias: String(100), nombre corto generado para un archivo.
    :param cantidadIteracion: Integer, registra el número de iteraciones
            guardadas en un archivo.
    :param etiqueta1: String(100),
    :param etiqueta2: String(100),
    :param etiqueta3: String(100),
    :param etiqueta4: String(100),
    :param nombreProblema: String(100), registra el nombre del problema.
    :param numeroObjetivo: registra el número de objetivos.
    :param numeroVariable: String(100), registra el número de variables.
    :param nombreVariables: String(100), registra los valores de las variables.
    :param nombreObjetivos: String(100), registra los valores de los objetivos.
    :param poblacionInicial: Integer, registra el número de población inicial.
    :param fechaAdd: Date, fecha registro del archivo.
    :param proyecto_id: Integer, ForeignKey de un Proyecto.
    '''
    __tablename__ = 'resultado'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    nombre = Column(String(100))
    alias = Column(String(50))
    cantidadIteracion = Column(Integer)
    etiqueta1 = Column(String(100))
    etiqueta2 = Column(String(100))
    etiqueta3 = Column(String(100))
    etiqueta4 = Column(String(100))
    nombreProblema = Column(String(100))
    numeroObjetivo = Column(Integer)
    numeroVariable = Column(Integer)
    nombreVariables = Column(String(100))
    nombreObjetivos = Column(String(100))
    poblacionInicial = Column(Integer)
    fechaAdd = Column(Date())
    proyecto_id = Column(Integer, ForeignKey('proyecto.id'))

    iteraciones = relationship('Iteracion',
                          cascade="save-update, merge, delete",
                          order_by='Iteracion.id', backref='resultado')

    def __init__(self):
        pass

    def __repr__(self):
        return "<Resultados(nombre='%s', alias='%s', cantidadIteracion='%s', \
        etiqueta1='%s', etiqueta2='%s', etiqueta3='%s', etiqueta4='%s', \
        nombreProblema='%s', numeroObjetivo='%s', numeroVariable='%s', \
        poblacionInicial='%s', nombreVariables='%s', nombreObjetivos='%s',\
        fechaAdd='%s')>" % (self.nombre, self.alias, self.cantidadIteracion,
        self.etiqueta1, self.etiqueta2, self.etiqueta3, self.etiqueta4,
        self.nombreProblema, self.numeroObjetivo, self.numeroVariable,
        self.poblacionInicial, self.nombreVariables, self.nombreObjetivos,
        self.fechaAdd)


class Iteracion(Base):
    ''''''

    __tablename__ = 'iteracion'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    identificador = Column(Integer)
    inicioEjecucion = Column(Float)
    finEjecucion = Column(Float)
    cantidadIndividuo = Column(Integer)
    resultado_id = Column(Integer, ForeignKey('resultado.id'))

    individuos = relationship('Individuo',
                          cascade="save-update, merge, delete",
                          order_by='Individuo.id', backref='iteracion')

    def __init__(self):
        pass

    def __repr__(self):
        return "<Iteracion(identificador: '%s', inicioEjecucion :'%s', \
        finEjecucion:'%s', cantidadindividuo:'%s')>" % (self.identificador,
        self.inicioEjecucion, self.finEjecucion, self.cantidadIndividuo)


class Individuo(Base):
    ''''''

    __tablename__ = 'individuo'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    identificador = Column(Integer)
    varDTLZ = Column(Float)
    objetivos = Column(String(500))
    variables = Column(String(500))
    iteracion_id = Column(Integer, ForeignKey('iteracion.id'))

    def __init__(self):
        pass

    def __repr__(self):
        return "<Individuo(identificador: '%s', objetivos: '%s', variables: \
        '%s', varDTLZ: '%f')>" % (self.identificador, self.objetivos,
                                  self.variables, self.varDTLZ)


def createDB():

    base.createDb()
