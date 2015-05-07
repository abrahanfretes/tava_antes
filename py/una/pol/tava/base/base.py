'''
Created on 27/06/2014

Modulo base encargado de manejar las interacciones con la Base de Datos.

@author: afretes
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from py.una.pol.tava.base import tavac as tvc


path_database = tvc.getDataBaseInHome('tava.db')
engine = create_engine('sqlite:///' + path_database)
Base = declarative_base()


def getBase():

    return Base


def createDb():

    Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


def getSession():

    return session
