# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''
import wx

from py.una.pol.tava.view.vtree import ProjectTreeCtrl
from py.una.pol.tava.presenter.pbody import ProjectTreeNotebookPresenter
from wx import GetTranslation as _
import py.una.pol.tava.view.vi18n as C
import py.una.pol.tava.view.vimages as I
import wx.lib.agw.aui as aui
# Para emplear como backend la libreria WxPython
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
import numpy as np
import matplotlib.pyplot as plt

from py.una.pol.tava.presenter.pbody import WorkingPagePresenter

#-- Config Parallel -------------------
import wx.dataview as dv


class MainPanel(wx.Panel):
    '''
    Clase Panel que representa al Cuerpo Principal que contendrá el panel de
    navegación de Proyectos, área de trabajo, etc.
    '''

    def __init__(self, parent):
        '''
        Constructor de la clase MainPanel.
        :param parent: referencia a la clase padre de MainPanel.
        '''
        super(MainPanel, self).__init__(parent)

        # Seteamos el color de fondo
        self.SetBackgroundColour('#3B444B')

        # Definicion del Splitter que divide el area de trabajo de la
        # exploración de proyectos
        self.splitter = wx.SplitterWindow(self, style=wx.SP_3D)

        # Definicion del panel izquierdo que contendra el panel de explorcion
        # de proyectos.
        left_panel = wx.Panel(self.splitter)
        left_panel.SetBackgroundColour('#FFFFFF')

        # Definicion de la clase Notebook para el explorador de proyectos
        self.project_tree_notebook = ProjectTreeNotebook(left_panel)

        # Definicion del Sizer para la clase Notebook
        project_tree_sizer = wx.BoxSizer()
        project_tree_sizer.Add(self.project_tree_notebook, 1, wx.EXPAND)

        # Asociamos el sizer al panel izquierdo
        left_panel.SetSizer(project_tree_sizer)

        # Definicion del panel derecho para el splitter
        right_panel = wx.Panel(self.splitter, -1)

        # Definicion del componente Notebook para el panel derecho
        right_notebook = AUINotebook(right_panel)

        # Creamos el sizer para el contenido del panel derecho
        right_panel_hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # Establecemos la notebook creada en el sizer
        right_panel_hsizer.Add(right_notebook, 1, wx.EXPAND)

        # Asociamos el sizer con el panel derecho
        right_panel.SetSizer(right_panel_hsizer)

        # Asociamos los paneles izquierdo y derecho al splitter
        self.splitter.SplitVertically(left_panel, right_panel, 210)
        self.splitter.SetMinimumPaneSize(200)

        # Creamos el sizer para colocar el Splitter y expandirlo
        # en el MainPanel
        body_sizer = wx.BoxSizer(wx.VERTICAL)
        body_sizer.Add(self.splitter, 1, wx.EXPAND | wx.ALL, 10)

        # Asociamos el sizer creado con la clase MainPanel
        self.SetSizer(body_sizer)


class ProjectTreeNotebook(wx.Notebook):
    '''
    Clase Notebook que contendrá la pestaña que albergará el árbol de
    proyectos.
    '''
    def __init__(self, parent):
        super(ProjectTreeNotebook, self).__init__(parent, style=wx.BK_DEFAULT)

        # Definición del Presenter
        self.presenter = ProjectTreeNotebookPresenter(self)

        # Creacion del panel contenedor del arbol de Proyectos
        self.project_tree_panel = TreePanel(self)

        # El panel es agregado como pagina del componente Notebook con su
        # correspondiente label
        self.AddPage(self.project_tree_panel, _(C.MP_PE))

        # Se añade el icono de explorador de proyectos a la unica pestaña.
        il = wx.ImageList(16, 16)
        self.SetImageList(il)
        tree_explorer_bmp = il.Add(I.tree_explorer_gif)
        self.SetPageImage(0, tree_explorer_bmp)

        # Se establece el color de fondo para el componente Notebook.
        self.SetBackgroundColour(self.GetThemeBackgroundColour())


class TreePanel(wx.Panel):
    '''
    Clase Panel que contendrá el árbol de exploración de proyectos.
    '''
    def __init__(self, parent):
        super(TreePanel, self).__init__(parent)

        # Creamos el arbol de Proyectos y lo asociamos al Panel
        self.project_tree = ProjectTreeCtrl(self)

        # Creamos un boxSizer para el arbol de Proyectos y lo añadimos al Panel
        project_tree_vsizer = wx.BoxSizer(wx.VERTICAL)
        project_tree_vsizer.Add(self.project_tree, 1, wx.EXPAND | wx.ALL, 3)

        # Asociamos el sizer a la clase Panel
        self.SetSizer(project_tree_vsizer)


class AUINotebook(aui.AuiNotebook):
    '''
    AUI Notebook class
    '''

    def __init__(self, parent):
        '''
        Método de inicialización de la clase AUINotebook.
        :param parent: referencia al objeto padre de la clase.
        '''

        aui.AuiNotebook.__init__(self, parent=parent)

        # Se establecen los estilos por defecto
        self.default_style = (aui.AUI_NB_DEFAULT_STYLE |
                                aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER)

        self.SetWindowStyleFlag(self.default_style)

        # Establecemos el estilo similar al navegador Chrome
        self.SetArtProvider(aui.ChromeTabArt())

#         # Se agregan algunas paginas al Notebook
        self.AddPage(WorkingPage(self), 'TabPrueba', True)
#         pages = [ParallelPanel, TabPanel]
#
#         pageCtr = 1
#         for page in pages:
#             label = "Tab #%i" % pageCtr
#             tab = page(self)
#             self.AddPage(tab, label, False)
#             pageCtr += 1


class WorkingPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.presenter = WorkingPagePresenter(self)
        self.datas = self.presenter.createDate()

        #una Pagina consiste en:
        #Una o mas figuras y,
        #Unas configuraciones
        self.figure = ParallelPanel(self)
        self.config = ParallelConfig(self, self.datas)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.config, 1, wx.EXPAND)
        sizer.Add(self.figure, 3, wx.EXPAND)
        self.SetSizer(sizer)


class ZoomPan:
    '''
    Clase encargada de gestionar de scrolling y seleccion para invocar a los
    métodos zoom y pan factory.
    '''
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None

    def zoom_factory(self, ax, fig, base_scale=2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            # get event x location
            xdata = event.xdata
            # get event y location
            ydata = event.ydata

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print event.button

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width *
                         (relx)])
            ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height *
                         (rely)])
            ax.figure.canvas.draw()

        # get the figure of interest
        fig = ax.get_figure()
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax, fig):
        def onPress(event):
            if event.inaxes != ax:
                return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None:
                return
            if event.inaxes != ax:
                return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        # get the figure of interest
        fig = ax.get_figure()

        # attach the call back
        fig.canvas.mpl_connect('button_press_event', onPress)
        fig.canvas.mpl_connect('button_release_event', onRelease)
        fig.canvas.mpl_connect('motion_notify_event', onMotion)

        #return the function
        return onMotion


class TabPanel(wx.Panel):
    '''
    Clase Panel empleada como ejemplo de pestaña para la Notebook
    '''
    """ A simple wx.Panel class. """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111, xlim=(0, 1), ylim=(0, 1),
                                 autoscale_on=False)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()
        self.axes.set_title('Click to zoom')
        x, y, s, c = np.random.rand(4, 200)
        s *= 200

        self.axes.scatter(x, y, s, c)
        scale = 1.1
        zp = ZoomPan()
        zp.zoom_factory(self.axes, self.figure, base_scale=scale)
        zp.pan_factory(self.axes, self.figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()


class ParallelPanel(wx.Panel):
    '''
    Clase Panel que contiene la configuracion para la visualizacion del
    componente de coordenadas paralelas.
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        values = np.hstack((np.random.randn(4, 10) + 4 * np.random.rand(4, 1),
                        np.random.randn(4, 8) + 4 * np.random.rand(4, 1)
                       ))
        print values
        labels = np.concatenate((['Label A'] * 10, ['Label B'] * 8))
        print labels
        coordinates = map(lambda x: "coord %i" % x, range(4))
        print coordinates

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()

        # find names and number of different classes
        ulabels = np.unique(labels)
        print ulabels
        n_labels = len(ulabels)
        print n_labels

        # for each select distinct colors from Accent pallette
        cmap = plt.get_cmap('Accent')
        colors = cmap(np.arange(n_labels) * cmap.N / (n_labels + 1))
        print colors

        # change the label strings to indices into class names array
        class_id = np.searchsorted(ulabels, labels)
        lines = self.axes.plot(values[:, :], 'k')
        [l.set_color(colors[c]) for c, l in zip(class_id, lines)]

        # add grid, configure labels and axes
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['bottom'].set_position(('outward', 5))
        self.axes.spines['bottom'].set_visible(False)
        self.axes.yaxis.set_ticks_position('both')
        self.axes.xaxis.set_ticks_position('none')

        self.axes.set_xticks(np.arange(len(coordinates)), coordinates)
        self.axes.grid(axis='x', ls='-')

        leg_handlers = [lines[np.where(class_id == id_)[0][0]]
                        for id_ in range(n_labels)]
        self.axes.legend(leg_handlers, ulabels, frameon=False,
                         loc='upper left', ncol=len(labels),
                bbox_to_anchor=(0, -0.03, 1, 0))
        scale = 1.1
        zp = ZoomPan()
        zp.zoom_factory(self.axes, self.figure, base_scale=scale)
        zp.pan_factory(self.axes, self.figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()


#------------------- Config Data ------------------------------------------

class Iteration(object):
    def __init__(self, id_, label, result_file):
        self.id = id_
        self.label = label
        self.result_file = result_file
        self.check = True

    def __repr__(self):
        return 'Iteration %s-%s' % (self.label, self.result_file)


class ResultFile(object):
    def __init__(self, name):
        self.name = name
        self.iterations = []

    def __repr__(self):
        return 'ResultFile: ' + self.name


class MyTreeListModel(dv.PyDataViewModel):
    def __init__(self, data):
        dv.PyDataViewModel.__init__(self)
        self.data = data
        self.objmapper.UseWeakRefs(True)

    # Report how many columns this model provides data for.
    def GetColumnCount(self):
        return 3

    # Map the data column numbers to the data type
    def GetColumnType(self, col):
        mapper = {0: 'string', 1: 'string', 2: 'bool'}
        return mapper[col]

    def GetChildren(self, parent, children):

        if not parent:
            for result in self.data:
                children.append(self.ObjectToItem(result))
            return len(self.data)

        # Otherwise we'll fetch the python object associated with the parent
        # item and make DV items for each of it's child objects.
        node = self.ItemToObject(parent)
        if isinstance(node, ResultFile):
            for itr in node.iterations:
                children.append(self.ObjectToItem(itr))
            return len(node.iterations)
        return 0

    def IsContainer(self, item):
        # Return True if the item has children, False otherwise.
        ##self.log.write("IsContainer\n")

        # The hidden root is a container
        if not item:
            return True
        # and in this model the genre objects are containers
        node = self.ItemToObject(item)
        if isinstance(node, ResultFile):
            return True
        # but everything else (the song objects) are not
        return False

    #def HasContainerColumns(self, item):
    #    self.log.write('HasContainerColumns\n')
    #    return True

    def GetParent(self, item):
        # Return the item which is this item's parent.
        ##self.log.write("GetParent\n")

        if not item:
            return dv.NullDataViewItem

        node = self.ItemToObject(item)
        if isinstance(node, ResultFile):
            return dv.NullDataViewItem
        elif isinstance(node, Iteration):
            for rf in self.data:
                if rf.name == node.result_file:
                    return self.ObjectToItem(rf)

    def GetValue(self, item, col):
        # Return the value to be displayed for this item and column. For this
        # example we'll just pull the values from the data objects we
        # associated with the items in GetChildren.

        # Fetch the data object for this item.
        node = self.ItemToObject(item)

        if isinstance(node, ResultFile):
            # We'll only use the first column for the Genre objects,
            # for the other columns lets just return empty values
            mapper = {0: node.name, 1: "", 2: False}
            return mapper[col]

        elif isinstance(node, Iteration):
            mapper = {0: "", 1: node.label, 2: node.check}
            return mapper[col]

        else:
            raise RuntimeError("unknown node type")

    def GetAttr(self, item, col, attr):
        ##self.log.write('GetAttr')
        node = self.ItemToObject(item)
        if isinstance(node, ResultFile):
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False

    def SetValue(self, value, item, col):
        #print("SetValue: %s\n" % value)
        node = self.ItemToObject(item)
        if isinstance(node, Iteration):
            if col == 2:
                node.check = value

    def getParentItem(self):
        itemParent = []
        for node in self.data:
            if isinstance(node, ResultFile):
                itemParent.append(self.ObjectToItem(node))
        return itemParent


    #----------------------------------------------------------------------


class ParallelConfig(wx.Panel):
    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent, -1)

        #------ Definiciones iniciales ----------------------------------------
        self.data = self.GetDatas(data)

        self.InitUI()
        self.Centre()
        self.Show()
        #----------------------------------------------------

    def InitUI(self):
        #-- Se define el DataviewControl
        self.dvc = self.GetDataViewCtrl()
        self.model = MyTreeListModel(self.data)
        self.dvc.AssociateModel(self.model)
        self.ExpandFileResultItem()
        #------------------------------------------------------------------
        self.dvc.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.OnActivate)

        #-- parte de prueba
        remainingSpace = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)
        wx.StaticText(remainingSpace, -1, "Lo que sea", (15, 30))
        #-------------------------------------------------------------

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.dvc, 1, wx.EXPAND)
        sizer.Add(remainingSpace, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def ExpandFileResultItem(self):
        for node in self.model.getParentItem():
            self.dvc.Expand(node)

    def OnActivate(self, event):
        print 'OnActivate'
        for result in self.data:
            print result
            for itr in result.iterations:
                if itr.check:
                    print result.name, ':', itr.label, ': true'

    def GetDatas(self, data):

        filedatas = data.items()
        filedatas.sort()

        #nuestra estructura de datos sera una coleccion de RsultFile, cada una
        # de las cuales es una coleccion de Ieration

        data_aux = dict()
        for key, val in filedatas:
            itr = Iteration(str(key), val[0], val[1])
            result_file = data_aux.get(itr.result_file)
            if result_file is None:
                result_file = ResultFile(itr.result_file)
                data_aux[itr.result_file] = result_file
            result_file.iterations.append(itr)
        return data_aux.values()

    def GetDataViewCtrl(self):
        dvc = dv.DataViewCtrl(self, style=wx.BORDER_THEME
                    | dv.DV_ROW_LINES | dv.DV_VERT_RULES | dv.DV_MULTIPLE)

        #Defino las columnas
        tr = dv.DataViewTextRenderer()
        c0 = dv.DataViewColumn("File", tr, 0, width=80)
        dvc.AppendColumn(c0)
        c0.Alignment = wx.ALIGN_LEFT
        c1 = dvc.AppendTextColumn("Iteration", 1, width=68)
        c1.Alignment = wx.ALIGN_CENTER
        dvc.AppendToggleColumn("Select", 2, width=30,
                               mode=dv.DATAVIEW_CELL_ACTIVATABLE)
        return dvc

    #-------------------------------------------------------------------------
