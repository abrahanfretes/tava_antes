'''
Created on 27/06/2014

@author: afretes
'''
import base

session = base.getSession()


def add(objeto):
    session.add(objeto)
    session.commit()
    return objeto


def addAll(listaObjeto):
    session.add_all(listaObjeto)
    session.commit()
