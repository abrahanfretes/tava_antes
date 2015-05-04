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


def createfileForCurves(list_graphic, list_objectives, list_variables,
                        filename_gra, filename_var, filename_obj):

    fp_gra = os.path.join(getTavaDirectory(), filename_gra)
    fp_var = os.path.join(getTavaDirectory(), filename_var)
    fp_obj = os.path.join(getTavaDirectory(), filename_obj)

    f_gra = open(fp_gra, 'w')
    f_var = open(fp_var, 'w')
    f_obj = open(fp_obj, 'w')

    f_gra.write(list_graphic[0])
    for index in range(len(list_graphic) - 1):
        f_gra.write(list_graphic[index + 1])

    for index in range(len(list_objectives)):
        f_obj.write(list_objectives[index])
        f_var.write(list_variables[index])

    f_gra.close()
    f_var.close()
    f_obj.close()


def createfileBoxPlot(list_graphic, list_objectives, list_variables,
                      filename_gra, filename_var, filename_obj):

    fp_gra = os.path.join(getTavaDirectory(), filename_gra)
    fp_var = os.path.join(getTavaDirectory(), filename_var)
    fp_obj = os.path.join(getTavaDirectory(), filename_obj)

    f_gra = open(fp_gra, 'w')
    f_var = open(fp_var, 'w')
    f_obj = open(fp_obj, 'w')

    f_gra.write(list_graphic[0])
    for index in range(len(list_graphic) - 1):
        f_gra.write(list_graphic[index + 1])

    for index in range(len(list_objectives)):
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


def getFilePath(filename):
    return os.path.join(getTavaDirectory(), filename)


def getMinMax(filename):
    min_v = []
    max_v = []

    filepath = getFilePath(filename)
    f = open(filepath)

    ind = f.readline()
    if ind != '':
        for obj in ind.split(',')[1:]:
            min_v.append(float(obj))
            max_v.append(float(obj))
    ind = f.readline()
    while ind != '':
        index = 0
        for obj_aux in ind.split(',')[1:]:
            if float(obj_aux) < min_v[index]:
                min_v[index] = float(obj_aux)
            if float(obj_aux) > max_v[index]:
                max_v[index] = float(obj_aux)
            index += 1
        ind = f.readline()
    f.close()

    return min_v, max_v


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

# ---------------------------------------------------------------------------
# ------------------- Modos para Graficos  Andrews-Curves -------------------
MODE_ANDREWS_CURVES = 10
TREE_BACKGROUND_AC = '#FFFFFF'
FIGURE_BACKGROUND_AC = '#FFFFFF'
T_FIGURE_BACKGROUND_AC = '#BBA2FF'

# ---------------------------------------------------------------------------
# ------------------- Modos para Graficos  Andrews-Curves -------------------
MODE_BOX_PLOT = 20
TREE_BACKGROUND_BP = '#FFFFFF'
FIGURE_BACKGROUND_BP = '#FFFFFF'
T_FIGURE_BACKGROUND_BP = '#BBA2FF'