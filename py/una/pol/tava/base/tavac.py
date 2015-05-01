'''
Created on 30/08/2014

@author: abrahan
'''


# ------ constant settings for styles -----------------------------------------
vonlucken = 0  # estilo del archivo resultado seleccionado
# ----------------------------------------------------

# ------ errores en agregar archivos a proyectos ------------------------------
correct = 0      # not error
nid_error = 1    # error_name_in_datetable
nip_error = 2    # error_name_in_project
fos_error = 3    # file OSError
fva_Error = 4    # file ValueError
fio_error = 5    # file IOError
fuk_error = 6    # file unknown Error
# ----------------------------------------------------

# -------------------------- list style existing ------------------------------
style_list = ['Von Lucken']
# ---------------------------------------------------------------------------

# -------------------- pre-establish a file filter ----------------------------
wildcard = "Riles results |*"
# ---------------------------------------------------------------------------

import os
import tempfile


def getTavaDirectory():
    base = tempfile.gettempdir()
    test = os.path.join(base, 'tava')
    if not os.path.isdir(test):
        os.makedirs(test)
    return test


def isFileTava(filename):
    filepath = os.path.join(getTavaDirectory(), filename)
    os.path.isfile(filepath)


def fileDelete(filename):
    filepath = os.path.join(getTavaDirectory(), filename)
    if os.path.isfile(filepath):
        os.remove(filepath)


def createfileForParallel(list_graphic, list_objectives, list_variables,
                          filename_gra, filename_var, filename_obj):

    fp_gra = os.path.join(getTavaDirectory(), filename_gra)
    fp_var = os.path.join(getTavaDirectory(), filename_var)
    fp_obj = os.path.join(getTavaDirectory(), filename_obj)

    f_gra = open(fp_gra, 'w')
    f_var = open(fp_var, 'w')
    f_obj = open(fp_obj, 'w')

    f_gra.write(list_graphic[0])
    for index in range(len(list_objectives)):

        f_gra.write(list_graphic[index + 1])
        f_obj.write(list_objectives[index])
        f_var.write(list_variables[index])
    f_gra.close()
    f_var.close()
    f_obj.close()


def redFileForTab(filename):

    to_ret = []
    filepath = os.path.join(getTavaDirectory(), filename)
    f = open(filepath)
    ind = f.readline()

    while ind != '':
        to_ret.append(ind.split(','))
        ind = f.readline()
    f.close()

    return to_ret

# ---------------------------------------------------------------------------
# ------------------- Modos para Graficos   ---------------------------------
MODE_PARALLEL_COORDINATES_GF = 0
MODE_PARALLEL_COORDINATES_AL = 4
TREE_BACKGROUND_AL = '#FFFFFF'
FIGURE_BACKGROUND_AL = '#FFFFFF'
T_FIGURE_BACKGROUND_AL = '#BBA2FF'
# T_FIGURE_BACKGROUND_AL = '#F8F1D9'
ORIENTATION_LINE_AL = ['both', 'x', 'y']
STYLE_LINE_AL = [':', '--', '-.', '-']

