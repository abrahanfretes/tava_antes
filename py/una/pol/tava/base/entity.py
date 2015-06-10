# -*- coding: utf-8 -*-
'''
Created on 27/06/2014

@author: afretes
'''
from sqlalchemy import ForeignKey, SmallInteger, Text
from sqlalchemy import Column, Integer, String, Date, Boolean
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

    results = relationship('Result', lazy=None,
                           cascade="save-update, merge, delete",
                           order_by='Result.id', backref='project')

    test_config = relationship('TestConfig', lazy=None,
                               cascade="save-update, merge, delete",
                               order_by='TestConfig.id', backref='project')

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

    iterations = relationship('Iteration', lazy=None,
                              cascade="save-update, merge, delete",
                              order_by='Iteration.id', backref='result')

    def __init__(self):
        pass

    def __repr__(self):
        return "<Result(name='%s', alias='%s', iteration_count='%s', \
        label1='%s', label2='%s', label3='%s', label4='%s', \
        problem_name='%s', number_objectives='%s', number_variables='%s', \
        number_initial_population='%s', name_variables='%s', \
        name_objectives='%s', add_date='%s')>"\
        % (self.name, self.alias,
           self.iteration_count, self.label1, self.label2, self.label3,
           self.label4, self.problem_name, self.number_objectives,
           self.number_variables, self.number_initial_population,
           self.name_variables, self.name_objectives, self.add_date)


class Iteration(Base):
    ''''''

    __tablename__ = 'iteration'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    identifier = Column(Integer)
    execution_start = Column(Float)
    execution_end = Column(Float)
    number_individuals = Column(Integer)
    objectives_min = Column(String(500))
    objectives_max = Column(String(500))
    result_id = Column(Integer, ForeignKey('result.id'))

    individuals = relationship('Individual', lazy=None,
                               cascade="save-update, merge, delete",
                               order_by='Individual.id', backref='iteration')

    def __init__(self):
        pass

    def __repr__(self):
        return "<Iteration(identifier: '%s', execution_start :'%s', \
        execution_end:'%s', number_individuals:'%s')>"\
        % (self.identifier, self.execution_start,
           self.execution_end, self.number_individuals)


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


class TestConfig(Base):
    ''''''

    __tablename__ = 'test_config'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text(2000), nullable=True)
    creation_date = Column(Date(), nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'))

    test_details = relationship('TestDetail',
                                cascade="save-update, merge, delete",
                                order_by='TestDetail.id',
                                backref='test_config')

    def __init__(self):
        pass

    def __repr__(self):
        return "<TestConfig(name='%s', description='%s', creation_date='%s')>"\
            % (self.name, self.description, self.creation_date)


class TestDetail(Base):
    ''''''

    __tablename__ = 'test_detail'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    test_config_id = Column(Integer, ForeignKey('test_config.id'))
    result_id = Column(Integer, ForeignKey('result.id'))

    test_datas = relationship('TestData',
                              cascade="save-update, merge, delete",
                              order_by='TestData.id',
                              backref='test_detail')

    def __init__(self):
        pass

    def __repr__(self):
        return "<TestDetail(id='%i')>" % (self.id)


class ParallelAnalizer(Base):
    ''''''

    __tablename__ = 'parallel_analizer'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name_figure = Column(String(100), nullable=True)
    color_lines = Column(String(7), nullable=False)
    legent = Column(Boolean, nullable=False)
    enable_objectives = Column(String(100))
    order_objective = Column(String(100))
    order_name_obj = Column(String(100))
    name_objetive = Column(String(100))
    name_variable = Column(String(100))
    maxs_objetive = Column(String(100))
    mins_objetive = Column(String(100))
    colors_backgrounds = Column(String(100))
    test_config_id = Column(Integer, ForeignKey('test_config.id'))
    figure_grid = relationship("FigureGrid", uselist=False,
                               backref="parallel_analizer")

    def __init__(self):
        pass

    def __repr__(self):
        return "<TestDetail(id='%i', name_figure='%s, name_figure='%s)>"\
            % (self.id, self.name_figure, self.legent)


class FigureGrid(Base):
    ''''''

    __tablename__ = 'figure_config'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    grid = Column(Boolean, nullable=False)
    orientation = Column(SmallInteger)
    red_color = Column(String(7))
    red_width = Column(SmallInteger, nullable=False)
    red_style = Column(SmallInteger)
    parallel_analizer_id = Column(Integer, ForeignKey('parallel_analizer.id'))

    def __init__(self):
        pass


class AndrewsCurves(Base):
    ''''''

    __tablename__ = 'andrews_curves'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name_figure = Column(String(100), nullable=True)
    color_lines = Column(String(7), nullable=False)
    legent = Column(Boolean, nullable=False)
    enable_objectives = Column(String(100))
    order_objective = Column(String(100))
    order_name_obj = Column(String(100))
    name_objetive = Column(String(100))
    name_variable = Column(String(100))
    maxs_objetive = Column(String(100))
    mins_objetive = Column(String(100))
    colors_backgrounds = Column(String(100))
    test_config_id = Column(Integer, ForeignKey('test_config.id'))
    andrews_grid = relationship("AndrewsGrid", uselist=False,
                                backref="andrews_curves")

    def __init__(self):
        pass

    def __repr__(self):
        return "<TestDetail(id='%i', name_figure='%s, name_figure='%s)>"\
            % (self.id, self.name_figure, self.legent)


class AndrewsGrid(Base):
    ''''''

    __tablename__ = 'andrews_grid'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    grid = Column(Boolean, nullable=False)
    orientation = Column(SmallInteger)
    red_color = Column(String(7))
    red_width = Column(SmallInteger, nullable=False)
    red_style = Column(SmallInteger)
    andrews_curves_id = Column(Integer, ForeignKey('andrews_curves.id'))

    def __init__(self):
        pass


class BoxPlot(Base):
    ''''''

    __tablename__ = 'box_plot'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name_figure = Column(String(100), nullable=True)
    color_lines = Column(String(7), nullable=False)
    legent = Column(Boolean, nullable=False)
    enable_objectives = Column(String(100))
    order_objective = Column(String(100))
    order_name_obj = Column(String(100))
    name_objetive = Column(String(100))
    name_variable = Column(String(100))
    maxs_objetive = Column(String(100))
    mins_objetive = Column(String(100))
    colors_backgrounds = Column(String(100))
    test_config_id = Column(Integer, ForeignKey('test_config.id'))
    box_plot_grid = relationship("BoxPlotGrid", uselist=False,
                                 backref="box_plot")

    def __init__(self):
        pass

    def __repr__(self):
        return "<TestDetail(id='%i', name_figure='%s, name_figure='%s)>"\
            % (self.id, self.name_figure, self.legent)


class BoxPlotGrid(Base):
    ''''''

    __tablename__ = 'box_plot_grid'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    grid = Column(Boolean, nullable=False)
    orientation = Column(SmallInteger)
    red_color = Column(String(7))
    red_width = Column(SmallInteger, nullable=False)
    red_style = Column(SmallInteger)
    andrews_curves_id = Column(Integer, ForeignKey('box_plot.id'))

    def __init__(self):
        pass


class TestData(Base):
    ''''''

    __tablename__ = 'test_data'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    test_detail_id = Column(Integer, ForeignKey('test_detail.id'))
    iteration_id = Column(Integer, ForeignKey('iteration.id'))

    def __init__(self):
        pass

    def __repr__(self):
        return "<TestData(id='%s')>" % (self.id)


class SomConfig(Base):
    ''''''

    __tablename__ = 'som_config'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    learning_rate = Column(Float)
    sigma = Column(Float)
    topology = Column(String(20))
    columns = Column(Integer)
    rows = Column(Integer)
    map_initialization = Column(String(20))
    neighborhood = Column(String(50))
    iterations = Column(Integer)
    test_config_id = Column(Integer, ForeignKey('test_config.id'))

    def __init__(self):
        pass

    def __repr__(self):
        return "<SomConfig()>"


class ResultMetric(Base):
    ''''''

    __tablename__ = 'result_metric'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    filename = Column(String(100))
    project_id = Column(Integer, ForeignKey('project.id'))
    moea_problems = relationship('MoeaProblem',
                                 cascade="save-update, merge, delete",
                                 order_by='MoeaProblem.id')

    def __init__(self):
        pass

    def __repr__(self):
        return "<ResultMetric()>"


class MoeaProblem(Base):
    ''''''

    __tablename__ = 'moea_problem'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(100))
    result_metric = Column(Integer, ForeignKey('result_metric.id'))
    number_objectives = relationship('NumberObjective',
                                     cascade="save-update, merge, delete",
                                     order_by='NumberObjective.id')

    def __init__(self):
        pass

    def __repr__(self):
        return "<MoeaProblem(id='%i', name='%s, result_id='%i)>"\
            % (self.id, self.name, self.result_metric)


class NumberObjective(Base):
    ''''''

    __tablename__ = 'number_objective'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    value = Column(SmallInteger)
    moea_problem = Column(Integer, ForeignKey('moea_problem.id'))
    evolutionary_methods = relationship('EvolutionaryMethod',
                                        cascade="save-update, merge, delete",
                                        order_by='EvolutionaryMethod.id')

    def __init__(self):
        pass

    def __repr__(self):
        return "<NumberObjective(id='%i', value='%i, moea_problem_id='%i)>"\
            % (self.id, self.value, self.moea_problem)


class EvolutionaryMethod(Base):
    ''''''

    __tablename__ = 'evolutionary_method'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(100))
    number_objective = Column(Integer, ForeignKey('number_objective.id'))
    number_threadss = relationship('NumberThreads',
                                   cascade="save-update, merge, delete",
                                   order_by='NumberThreads.id')

    def __init__(self):
        pass

    def __repr__(self):
        return "<EvolutionaryMethod(id='%i', name='%s, number_objective_id='%i)>"\
            % (self.id, self.name, self.number_objective)


class NumberThreads(Base):
    ''''''

    __tablename__ = 'number_threads'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    value = Column(SmallInteger)
    evolutionary_method = Column(Integer, ForeignKey('evolutionary_method.id'))
    parallelization_methods = relationship('ParallelizationMethod',
                                           cascade="save-update, merge, \
                                           delete",
                                           order_by='ParallelizationMethod.id')

    def __init__(self):
        pass

    def __repr__(self):
        return "<NumberThreads(id='%i', value='%i, evolutionary_method_id='%i)>"\
            % (self.id, self.value, self.evolutionary_method)


class ParallelizationMethod(Base):
    ''''''

    __tablename__ = 'parallelization_method'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(100))
    number_thread = Column(Integer, ForeignKey('number_threads.id'))
    metrics = relationship('Metric', cascade="save-update, merge, delete",
                           order_by='Metric.id')

    def __init__(self):
        pass

    def __repr__(self):
        return "<ParallelizationMethod(id='%i', name='%s, number_thread_id='%i)>"\
            % (self.id, self.name, self.number_thread)


class Metric(Base):
    ''''''

    __tablename__ = 'metric'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(100))
    parallelization_method = Column(Integer,
                                    ForeignKey('parallelization_method.id'))
    populations = relationship('Population',
                               cascade="save-update, merge, delete",
                               order_by='Population.id')

    def __init__(self):
        pass

    def __repr__(self):
        return "<Metric(id='%i', name='%s, parallelization_method_id='%i)>"\
            % (self.id, self.name, self.parallelization_method)


class Population(Base):
    ''''''

    __tablename__ = 'population'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    value = Column(Integer)
    metric = Column(Integer, ForeignKey('metric.id'))
    value_metrics = relationship('ValueMetric',
                                 cascade="save-update, merge, delete",
                                 order_by='ValueMetric.id')

    def __init__(self):
        pass

    def __repr__(self):
        return "<Population(id='%i', value='%i, metric_id='%i)>"\
            % (self.id, self.value, self.metric)


class ValueMetric(Base):
    ''''''

    __tablename__ = 'value_metric'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    iteration = Column(Integer)
    value = Column(Float)
    population = Column(Integer, ForeignKey('population.id'))

    def __init__(self):
        pass

    def __repr__(self):
        return "<ValueMetric(id='%i', iteration='%i, value='%f, population_id='%i)>"\
            % (self.id, self.iteration, self.value, self.population)


class TestMetric(Base):
    ''''''

    __tablename__ = 'test_metric'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(100))
    project_id = Column(Integer, ForeignKey('project.id'))
    result_metric_id = Column(Integer, ForeignKey('result_metric.id'))

    def __init__(self):
        pass

    def __repr__(self):
        return "<TestMetric(id='%i', name='%s', project_id='%i, result_id='%i)>"\
            % (self.id, self.name, self.project_id, self.result_metric_id)


def createDB():
    base.createDb()
