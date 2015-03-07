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

#Asi no funciona
#==============================================================================
# # Send = pproject
# # Subscribe = ptree
# PROJECT_RENAME_UP = 'PROJECT.RENAME.UP'
#==============================================================================

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
