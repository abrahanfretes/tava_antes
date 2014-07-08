'''
Created on 27/06/2014

Modulo base encargado de manejar las interacciones con la Base de Datos.

@author: afretes
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///tava.db', echo=True)
Base = declarative_base()


def getBase():

    return Base


def createDb():

    Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


def getSession():

    return session
