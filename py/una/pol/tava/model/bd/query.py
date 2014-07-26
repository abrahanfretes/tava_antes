'''
Created on 27/06/2014

@author: afretes
'''
import base
from entity import Project, Result, Iteration, Individual
from sqlalchemy.orm import subqueryload

session = base.getSession()

#Querys para Proyectos


def getAllProject():
    return session.query(Project).order_by(Project.creation_date,
                                           Project.state)


def getAllProjectWithResults():
    return session.query(Project).options(subqueryload(Project.results))


def getProjectWithResults(project):

    return session.query(Project).options(subqueryload(Project.results)).\
            filter_by(id=project.id).first()


def getProjectById(id_project):
    return session.query(Project).filter_by(id=id_project).first()


def getProjectByResult(result):
    return session.query(Project).filter_by(id=result.proyecto_id).first()


def getAllNamesProject():
    return session.query(Project.name).order_by(Project.name).all()

#Querys para Result


def getAllResult():
    return session.query(Result).order_by(Result.name).all()


def getResultsByProject(project):
    return session.query(Result).filter_by(proyecto_id=project.id).all()


def getResultById(id_result):
    return session.query(Result).filter_by(id=id_result).first()


def getResultWithIterations(result):
    return session.query(Result).options(
            subqueryload(Result.iterations)).\
            filter_by(id=result.id).first()


#Querys para Iteration

def getIterationsByResult(result):
    return session.query(Iteration).order_by(Iteration.id).\
                        filter_by(id=result.id).all()


def getIterationsByIdResult(id_result):
    return session.query(Iteration).order_by(Iteration.id).\
                        filter_by(id=id_result).all()


def getIterationById(id_iteration):
    return session.query(Iteration).filter_by(id=id_iteration).first()


def getIterationWithIndividual(id_iteration):
    return session.query(Iteration).options(
            subqueryload(Iteration.individuals)).\
            filter_by(id=id_iteration).first()


#Querys para Individual


def getIndividuosByIteracion(iteration):
    return session.query(Individual).order_by(Individual.identifier).\
                            filter_by(iteracion_id=iteration.id).all()


def getIndividualsByIteracionId(id_iteration):
    return session.query(Individual).order_by(Individual.identifier).\
                            filter_by(iteracion_id=id_iteration).all()


def getIdentifierAndVariableOfIndividual(id_iteration):
    return session.query(Individual.identifier, Individual.variables).\
                            order_by(Individual.identifier).\
                            filter_by(iteracion_id=id_iteration).all()


def getIdentifierAndObjectiveOfIndividual(id_iteration):
    return session.query(Individual.identifier, Individual.objectives).\
                            order_by(Individual.identifier).\
                            filter_by(iteracion_id=id_iteration).all()


def getIdenObjOfIndividuoByIteracion(iteration):
    return session.query(Individual.identifier, Individual.objectives).\
                            order_by(Individual.identifier).\
                            filter_by(iteracion_id=iteration.id).all()


def getIdentifierObjectiveVariableOfIndividual(id_iteration):
    return session.query(Individual.identifier, Individual.objectives,
                    Individual.variables).order_by(Individual.identifier).\
                            filter_by(iteracion_id=id_iteration).all()


def getVarDTLZOfIndividual(id_iteration):
    return session.query(Individual.identifier, Individual.varDTLZ).\
                            rder_by(Individual.identifier).\
                            filter_by(iteracion_id=id_iteration).all()
