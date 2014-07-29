# -*- coding: utf-8 -*-
'''
Created on 27/06/2014

@author: afretes
'''


from sqlalchemy import ForeignKey, SmallInteger, Text
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import Float
from sqlalchemy.orm import relationship
import base


Base = base.getBase()
OPEN = 0
CLOSED = 1
HIDDEN = 2


class Project(Base):
    '''
    Entidad Project, clase mapeada a base de datos con name "project"

    :param name: String(100), regitra el name de un project
    :param blog: Text(2000), regitra la descripción de un project
    :param state: SmallInteger, regitra el state de un project, valores
            posibles:
            0 = abierto
            1 = cerrado
            2 = oculto
    :param creation_date: Date, regitra la fecha de creación de un project

    '''

    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(100), nullable=False, unique=True)
    blog = Column(Text(2000), nullable=True)
    state = Column(SmallInteger, nullable=False)
    creation_date = Column(Date(), nullable=False)

    results = relationship('Result',
                              cascade="save-update, merge, delete",
                              order_by='Result.id', backref='project')

    def __init__(self, name, blog, state, date):

        self.name = name
        self.blog = blog
        self.state = state
        self.creation_date = date

    def __repr__(self):
        return "<Project(name='%s', blog='%s', state='%s',\
        creation_date='%s')>" % (self.name,
                                    self.blog, self.state, self.creation_date)


class Result(Base):
    '''
    Entidad Result, clase mapeada a una base de datos con name "result"
    :param name: String(100), regitra el name de un archivo result.
    :param alias: String(100), name corto generado para un archivo.
    :param iteration_count: Integer, registra el número de iterations
            guardadas en un archivo.
    :param label1: String(100),
    :param label2: String(100),
    :param label3: String(100),
    :param label4: String(100),
    :param problem_name: String(100), registra el name del problema.
    :param number_objectives: registra el número de objectives.
    :param number_variables: String(100), registra el número de variables.
    :param name_variables: String(100), registra los valores de las variables.
    :param name_objectives: String(100), registra los valores de loss
    objectives.
    :param number_initial_population: Integer, registra el número de población
    inicial.
    :param add_date: Date, fecha registro del archivo.
    :param project_id: Integer, ForeignKey de un Project.
    '''
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(100))
    alias = Column(String(50))
    iteration_count = Column(Integer)
    label1 = Column(String(100))
    label2 = Column(String(100))
    label3 = Column(String(100))
    label4 = Column(String(100))
    problem_name = Column(String(100))
    number_objectives = Column(Integer)
    number_variables = Column(Integer)
    name_objectives = Column(String(100))
    name_variables = Column(String(100))
    number_initial_population = Column(Integer)
    add_date = Column(Date())
    project_id = Column(Integer, ForeignKey('project.id'))

    iterations = relationship('Iteration',
                          cascade="save-update, merge, delete",
                          order_by='Iteration.id', backref='result')

    def __init__(self):
        pass

    def __repr__(self):
        return "<Result(name='%s', alias='%s', iteration_count='%s', \
        label1='%s', label2='%s', label3='%s', label4='%s', \
        problem_name='%s', number_objectives='%s', number_variables='%s', \
        number_initial_population='%s', name_variables='%s', \
        name_objectives='%s', add_date='%s')>" % (self.name, self.alias, \
        self.iteration_count, self.label1, self.label2, self.label3,
        self.label4, self.problem_name, self.number_objectives,\
        self.number_variables, self.number_initial_population, \
        self.name_variables, self.name_objectives, self.add_date)


class Iteration(Base):
    ''''''

    __tablename__ = 'iteration'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    identifier = Column(Integer)
    execution_start = Column(Float)
    execution_end = Column(Float)
    number_individuals = Column(Integer)
    result_id = Column(Integer, ForeignKey('result.id'))

    individuals = relationship('Individual',
                          cascade="save-update, merge, delete",
                          order_by='Individual.id', backref='iteration')

    def __init__(self):
        pass

    def __repr__(self):
        return "<Iteration(identifier: '%s', execution_start :'%s', \
        execution_end:'%s', number_individuals:'%s')>" % (self.identifier,
        self.execution_start, self.execution_end, self.number_individuals)


class Individual(Base):
    ''''''

    __tablename__ = 'individual'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    identifier = Column(Integer)
    varDTLZ = Column(Float)
    objectives = Column(String(500))
    variables = Column(String(500))
    iteration_id = Column(Integer, ForeignKey('iteration.id'))

    def __init__(self):
        pass

    def __repr__(self):
        return "<Individual(identifier: '%s', objectives: '%s', variables: \
        '%s', varDTLZ: '%f')>" % (self.identifier, self.objectives,
                                  self.variables, self.varDTLZ)


def createDB():

    base.createDb()