# -*- coding: utf-8 -*-
'''
Created on 27/06/2014

@author: afretes
'''
import base

session = base.getSession()


def add(objeto):
    '''
    Función que persiste un Objeto a la Base de Datos.

    :param objeto: cualquiera de las clases mapeadas a la Base de Datos
    :return: Objeto
    '''
    session.add(objeto)
    session.commit()
    return objeto


def addAll(listaObjeto):
    '''
    Función que persiste una lista de Objetos a la Base de Datos.

    :param listaObjeto: cualquiera de las clases mapeadas a la Base de Datos
    '''
    session.add_all(listaObjeto)
    session.commit()


def delete(objeto):
    '''
    Función que remueve uno o varios Objetos de la Base de Datos.

    :param objeto: cualquiera de las clases mapeadas a la Base de Datos
    '''
    session.delete(objeto)
    session.commit()
