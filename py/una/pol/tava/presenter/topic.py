'''
Created on 04/08/2014

@author: afretes
'''

# Send = ptoolbar
# Subscribe = pframe
BAR_PROJECT_NEW = 'BAR.PROJECT.NEW'

# Send = ptoolbar, pprojectmenu
# Subscribe = ptoolbar, ptree
PROJECT_STATE_UPDATE = 'PROJECT.STATEUPDATE'

# Send = ptoolbar, pprojectmenu
# Subscribe = pframe
PROJECT_DELETE_SELECT = 'PROJECT.SELECTDELETE'

# Send = pproject
# Subscribe = ptree, ptoolbar
PROJECT_DELETE = 'PROJECT.DELETE'

# Send = ptree
# Subscribe = ptoolbar
PROJECT_SELECTED_OPEN = 'PROJECT.SELECTEDOPEN'

# Send = ptree
# Subscribe = ptoolbar
PROJECT_SELECTED_CLOSE = 'PROJECT.SELECTEDCLOSE'

# Send = ptree
# Subscribe = pframe, ptest
PROJECT_SELECTED = 'PROJECT.SELECTED'

# Send = pproject
# Subscribe = ptree
PROJECT_NEW = 'PROJECT.NEW'

# Send = pprojectmenu
# Subscribe =pframe
PROJECT_RENAME = 'PROJECT.RENAME'

# Send = pprojectmenu, pmenu
# Subscribe =pframe
PROJECT_PROPERTIES = 'PROJECT.PROPERTIES'

# Asi no funciona
# =============================================================================
# # Send = pproject
# # Subscribe = ptree
# PROJECT_RENAME_UP = 'PROJECT.RENAME.UP'
# =============================================================================

# Send = pproject, presult
# Subscribe = ptree
PROJECT_UPDATE = 'PROJECT.UPDATE'

# Send = pmenu
# Subscribe = pframe
ENGLISH_SELECTED = 'ENGLISH.SELECTED'

# Send = pmenu
# Subscribe = pframe
SPANISH_SELECTED = 'SPANISH.SELECTED'

# Send = pframe
# Subscribe = pmenu
LANGUAGE_CHANGED = 'LANGUAGE.CHANGED'

# Send = ptoolbar
# Subscribe = pframe
PROJECT_UNHIDE = 'PROJECT.UNHIDE'

# Send = pproject
# Subscribe = pproject
PROJECT_CLICKCHECKBOXLIST = 'PROJECT.CLICKCHECKBOXLIST'

# Send = pprojectmenu
# Subscribe = pframe
PROJECT_ADDFILE = 'PROJECT.ADDFILE'

# Send = pmenu
# Subscribe = pframe
GRAPHIC_WIZARD = 'GRAPHIC.WIZARD'

# Send = pmenu, ptest
# Subscribe = pbody
TESTCONFIG_ADD_PAGE = 'TESTCONFIG.ADDPAGE'

# -------------------------------
# Verificar para eliminar luego
# ------------------------------
# Send = pparallelcoordinatesdata_spl
# Subscribe = pparallelcoordinatesdata_spl
PARALLELANALIZER_UPDATE_FIGURE = 'PARALLELANALIZER.UPDATE_FIGURE'

# Send = pparallelcoordinatesdata_fnl
# Subscribe = pparallelcoordinatesdata_fnl
PARALLEL_TREE_CHECK_FIGURE = 'PARALLEL.TREE_CHECK_FIGURE'

# Send = pparallelcoordinatesdata_fnl
# Subscribe = pparallelcoordinatesdata_fnl
PARALLEL_UPDATE_FIGURE_FOR_TREE = 'PARALLEL.UPDATE_FIGURE_FOR_TREE'

# Send = pparallelcoordinatesdata_fnl
# Subscribe = pparallelcoordinatesdata_fnl
PARALLEL_UPDATE_FIGURE_LIST_OBJ = 'PARALLEL.UPDATE_FIGURE_LIST_OBJ'

# Send = pparallelcoordinatesdata_fnl
# Subscribe = pparallelcoordinatesdata_fnl
PARALLEL_VERIFY_TREE_CHECKEO = 'PARALLEL.VERIFY_TREE_CHECKEO'

# Send = pparallelcoordinatesdata_fnl
# Subscribe = pparallelcoordinatesdata_fnl
PARALLEL_UPDATE_ALL = 'PARALLEL.UPDATE_ALL'

# Send = pparallelcoordinatesdata_fnl
# Subscribe = pparallelcoordinatesdata_fnl
PARALLEL_UPDATE_FIGURE_CONFIG = 'PARALLEL.UPDATE_FIGURE_CONFIG'

# Send = pparallelcoordinatesdata_fnl
# Subscribe = pparallelcoordinatesdata_fnl
PARALLEL_UPDATE_FIGURE_CONFIG_SHOW = 'PARALLEL.UPDATE_FIGURE_CONFIG_SHOW'

# Send = pparallelcoordinatesdata_fnl
# Subscribe = pparallelcoordinatesdata_fnl
PARALLEL_UPDATE_FIGURE_SORT_OBJ = 'PARALLEL.UPDATE_FIGURE_SORT_OBJ'

# Send = pparallelcoordinatesdata_fnl
# Subscribe = pparallelcoordinatesdata_fnl
PARALLEL_ON_SET_FILTERS_OBJ = 'PARALLEL.ON_SET_FILTERS_OBJ'

# Send = pparallelcoordinatesdata_fnl
# Subscribe = pparallelcoordinatesdata_fnl
PARALLEL_SET_FILTERS_OBJ = 'PARALLEL.SET_FILTERS_OBJ'

# Send = pparallelcoordinatesdata_fnl
# Subscribe = pparallelcoordinatesdata_fnl
PARALLEL_ON_CLEAN_FILTERS_OBJ = 'PARALLEL.ON_CLEAN_FILTERS_OBJ'

# Send = pparallelcoordinatesdata_fnl
# Subscribe = pparallelcoordinatesdata_fnl
PARALLEL_UPDATE_FIGURE_RENAME_OBJ = 'PARALLEL.UPDATE_FIGURE_RENAME_OBJ'

# -------- pparallelcoordinates ----

# Send = pparallelcoordinates
# Subscribe = pparallelcoordinates
PARALLEL_FIGURE_TREE_CHECK_GF = 'PARALLEL.TREE_CHECK_FIGURE_GF'

# Send = pparallelcoordinates
# Subscribe = pparallelcoordinates
PARALLEL_FIGURE_BUTTON_TEST_GRAFIC_GF = 'PARALLEL.FIGURE_BUTTON_TEST_GRAFIC_GF'

# Send = pparallelcoordinates
# Subscribe = pparallelcoordinates
PARALLEL_FIGURE_BUTTON_RESU_GRAFIC_GF = 'PARALLEL.FIGURE_BUTTON_RESU_GRAFIC_GF'

# Send = pparallelcoordinates
# Subscribe = pparallelcoordinates
PARALLEL_FIGURE_BUTTON_ITER_GRAFIC_GF = 'PARALLEL.FIGURE_BUTTON_ITER_GRAFIC_GF'

# Send = pparallelcoordinates
# Subscribe = pparallelcoordinates
PARALLEL_FIGURE_FILE_TEST_GRAFIC_GF = 'PARALLEL.FIGURE_FILE_TEST_GRAFIC_GF'

# Send = pparallelcoordinates
# Subscribe = pparallelcoordinates
PARALLEL_FIGURE_FILE_RESU_GRAFIC_GF = 'PARALLEL.FIGURE_FILE_RESU_GRAFIC_GF'

# Send = pparallelcoordinates
# Subscribe = pparallelcoordinates
PARALLEL_FIGURE_FILE_ITER_GRAFIC_GF = 'PARALLEL.FIGURE_FILE_ITER_GRAFIC_GF'

# Send = pparallelcoordinates
# Subscribe = pparallelcoordinates
PARALLEL_FIGURE_VIEW_TEST_GRAFIC_GF = 'PARALLEL.FIGURE_VIEW_TEST_GRAFIC_GF'

# Send = pparallelcoordinates
# Subscribe = pparallelcoordinates
PARALLEL_FIGURE_VIEW_RESULT_GRAFIC_GF = 'PARALLEL.FIGURE_VIEW_RESULT_GRAFIC_GF'

# Send = pparallelcoordinates
# Subscribe = pparallelcoordinates
PARALLEL_FIGURE_VIEW_ITERA_GRAFIC_GF = 'PARALLEL.FIGURE_VIEW_ITERA_GRAFIC_GF'

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# TOPICOS USADOS EN LA CLASE MANEJADA PARA
#     GRAFICO DE COORDENADAS PARALELAS
#                 ANALIZER
# ---------------------------------------------------------------
# ---------------------------------------------------------------

# Send = pconfigparallel -> ParallelTreeALPresenter
# Subscribe = pconfigparallel -> BaseButtonsTollBar
PARALLEL_TREE_CHECK_FIGURE_AL = 'PARALLEL.TREE_CHECK_FIGURE_AL'


# Send = pconfigparallel -> ParallelTreeALPresenter
# Subscribe = pconfigparallel -> ButtonsEjecutionPresenter
PARALLEL_ONCLICK_BUTTON_EXECUTE_AL = 'PARALLEL.\
PARALLEL_ONCLICK_BUTTON_EXECUTE_AL'

# Send = pconfigparallel -> ParallelTreeALPresenter
# Subscribe = pconfigparallel -> ButtonsFilterPresenter
PARALLEL_TREE_CHECK_SET_FILTER_AL = 'PARALLEL.\
PARALLEL_TREE_CHECK_SET_FILTER_AL'

# Send = pconfigparallel -> ParallelTreeALPresenter
# Subscribe = pconfigparallel -> BaseButtonsTollBar
PARALLEL_TREE_CHECK_FILTER_AL = 'PARALLEL.PARALLEL_TREE_CHECK_FILTER_AL'

# Send = pconfigparallel -> ParallelTreeALPresenter
# Subscribe = pconfigparallel -> TopPanelPresenter
PARALLEL_UPDATE_FIGURE_FOR_TREE_AL = 'PARALLEL.UPDATE_FIGURE_FOR_TREE_AL'

# Send = pconfigparallel -> ButtonsEjecutionPresenter
# Subscribe = pconfigparallel -> ParallelTreeALPresenter
PARALLEL_VERIFY_TREE_CHECKED_AL = 'PARALLEL.VERIFY_TREE_CHECKED_AL'

# Send = pconfigparallel -> TopPanelPresenter -> updateFigureForChangeTreePub
# Send = pconfigparallel -> TopPanelPresenter -> updateFiltersObjectPub
# Send = pconfigparallel -> TopPanelPresenter -> updateListObjectPub
# Subscribe = pconfigparallel -> ParallelFigureALPresenter
# Subscribe = pconfigparallel -> TabVariablesPresenter
# Subscribe = pconfigparallel -> TabObjectivesPresenter
# Subscribe = pconfigparallel -> TabFiltrosPresenter
PARALLEL_UPDATE_ALL_AL = 'PARALLEL.UPDATE_ALL_AL'

# Send = pconfigparallel -> ButtonsFilterPresenter
# Subscribe = pconfigparallel -> TabFiltrosPresenter
PARALLEL_ON_SET_FILTERS_OBJ_AL = 'PARALLEL.ON_SET_FILTERS_OBJ_AL'

# Send = pconfigparallel -> ButtonsFilterPresenter -> cleanFilter
# Subscribe = pconfigparallel -> TabFiltrosPresenter -> setFiltersCleanPub
PARALLEL_ON_CLEAN_FILTERS_OBJ_AL = 'PARALLEL.ON_CLEAN_FILTERS_OBJ_AL'

# Send = pparallelconal -> ConfigurationParallelFigurePresenter
# Subscribe = pparallelconal -> ParallelTreeALPresenter
# Subscribe = pparallelconal -> ParallelFigureALPresenter
PARALLEL_BACKGROUND_UPDATE_AL = 'PARALLEL.BACKGROUND_UPDATE_AL'

# Send = pparallelconal -> ConfigurationParallelFigurePresenter
# Subscribe = pparallelconal -> ParallelTreeALPresenter
# Subscribe = pparallelconal -> ParallelFigureALPresenter
PARALLEL_GRID_UPDATE_AL = 'PARALLEL.GRID_UPDATE_AL'
