'''
Created on 30/08/2014

@author: abrahan
'''


#------ constant settings for styles ------------------------------------------
vonlucken = 0  # estilo del archivo resultado seleccionado
#----------------------------------------------------

#------ errores en agregar archivos a proyectos -------------------------------
correct = 0      # not error
nid_error = 1    # error_name_in_datetable
nip_error = 2    # error_name_in_project
fos_error = 3    # file OSError
fva_Error = 4    # file ValueError
fio_error = 5    # file IOError
fuk_error = 6    # file unknown Error
#----------------------------------------------------

#-------------------------- list style existing -------------------------------
style_list = ['Von Lucken']
#---------------------------------------------------------------------------

#-------------------- pre-establish a file filter -----------------------------
wildcard = "Riles results |*"
#---------------------------------------------------------------------------

import os
import tempfile


def  getTavaDirectory():
    base = tempfile.gettempdir()
    test = os.path.join(base, 'tava')
    if not os.path.isdir(test):
        os.makedirs(test)
    return test
