'''
Created on 28/11/2014

@author: arsenioferreira
'''
import wx
import matplotlib
matplotlib.use('WXAgg')
from minisom import MiniSom
from numpy import genfromtxt, linalg, apply_along_axis

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from pylab import get_cmap
from wx import EVT_LIST_ITEM_RIGHT_CLICK
from matplotlib.patches import Rectangle

from pandas.tools.plotting import parallel_coordinates
from pandas import DataFrame


class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111, xlim=(0, 1), ylim=(0, 1),
                                 autoscale_on=False)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        self.numObjetives = 0
        self.rect = None

    def setParameters(self, iterDir, sigma, learning_rate, columns, rows,
                      map_initialization, iterations):
        self.iterId = iterDir
        self.sigma = sigma
        self.learning_rate = learning_rate
        self.columns = columns
        self.rows = rows
        self.map_initialization = map_initialization
        self.iterations = iterations

    def trainSom(self):
        from py.una.pol.tava.dao.dindividual import getIndividualsByIteracionId
        individuals = getIndividualsByIteracionId(self.iterId)
        data = ""
        for individual in individuals:
            data += str(individual.objectives) + "\n"
        from StringIO import StringIO
        datos = genfromtxt(StringIO(data), delimiter=',')
        data = None
        data = datos
        self.numObjetives = len(data[0])

        # data normalization (Norma de Frobenius)
        data = apply_along_axis(lambda x: x / linalg.norm(x), 1, data)

        ### Initialization and training ###
        som = MiniSom(self.columns, self.rows, data.shape[1], sigma=self.sigma,
                      learning_rate=self.learning_rate)
        # som.random_weights_init(data)
        # Si el entrenamiento debe ser lineal o aleatorio
        if str(self.map_initialization) == "linear":
            print("Training batch...")
            som.train_batch(data, self.iterations)  # batch training
        else:
            print("Training random...")
            som.train_random(data, self.iterations)  # random training
        print("\n...ready!")
        return som, data

    def draw(self):
        som, data = self.trainSom()
        for xx in data:
            w = som.winner(xx)  # getting the winner
            som.individuals[w[0]][w[1]].append(xx)
        self.axes.pcolor(som.distance_map().T, cmap=get_cmap('gray'))

        self.axes.axis([0, som.weights.shape[0], som.weights.shape[1], 0])
        self.som = som

    def initialDraw(self):
        som, data = self.trainSom()

        for xx in data:
            w = som.winner(xx)  # getting the winner
            som.individuals[w[0]][w[1]].append(xx)

        self.axes.pcolor(som.distance_map().T, cmap=get_cmap('gray'))
        cax = self.axes.imshow(data, interpolation='nearest',
                               cmap=get_cmap('gray'))
        self.figure.colorbar(cax)

        self.axes.axis([0, som.weights.shape[0], som.weights.shape[1], 0])
        self.som = som

        for cnt, xx in enumerate(data):
            w = som.winner(xx)  # getting the winner
            som.individuals[w[0]][w[1]].append(xx)

        def onPick(event):
            if event.xdata and event.ydata:
                xdata = int(event.xdata)
                ydata = int(event.ydata)
                if self.rect:
                    self.rect.remove()
                self.rect = Rectangle((xdata, ydata), 1, 1, color="yellow",
                                      fill=False, lineWidth=2)

                self.axes.add_patch(self.rect)
                self.canvas.draw()

                self.GetParent().lc.DeleteAllItems()

                self.individuals = self.som.individuals[xdata][ydata]

                count = len(self.individuals)

                self.Parent.text.SetLabel("Cantidad de individuos: "
                                          + str(count))

                for cnt, ind in enumerate(self.individuals):
                    self.GetParent().lc.InsertStringItem(cnt, str(cnt + 1))
                    for c, i in enumerate(ind):
                        c = c + 1
                        self.GetParent().lc.SetStringItem(cnt, c, str(i))
                        if cnt % 2:
                            self.GetParent().lc.SetItemBackgroundColour(cnt,
                                                                    "white")
                        else:
                            self.GetParent().lc.SetItemBackgroundColour(cnt,
                                                                    "pink")
                print(self.GetParent().lc.getSelectIndices())

        self.figure.canvas.mpl_connect('button_press_event', onPick)


class IndividualsListCtrl(wx.ListCtrl):
    def __init__(self, parent, num_objetives, ID=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        self.InsertColumn(0, 'Fila')
        self.SetColumnWidth(0, 40)

        self.columns = []

        for i in range(num_objetives):
            i = i + 1
            column = 'Objetivo ' + str(i - 1)
            self.columns.append(column)
            self.InsertColumn(i, column)
            self.SetColumnWidth(i, 140)

    def getSelectIndices(self):
        selection = []
        # star at -1 to get the first selectec item
        current = -1
        while True:
            next_ = self.getNextSelected(current)
            if next_ == -1:
                return selection
            selection.append(next_)
            current = next_

    def getNextSelected(self, current):
        return self.GetNextItem(current, wx.LIST_NEXT_ALL,
                                wx.LIST_STATE_SELECTED)


class PanelSomConfig(wx.Panel):
    def __init__(self, parent, testConfig):
        super(PanelSomConfig, self).__init__(parent)

        self.initParameters(testConfig)

        # Parameters
        sbox = wx.StaticBox(self, label="Parameters")
        sboxsp = wx.StaticBoxSizer(sbox, wx.VERTICAL)

        # Attributes
        self.choice = wx.Choice(self, size=(200, 30), choices=self.items)
        self.choice.SetSelection(0)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Select one: "))
        sizer.Add(self.choice)

        sboxsp.Add(sizer, 0, wx.ALL, 8)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self, label="Initial learning \nrate:"))
        spin1 = wx.SpinCtrlDouble(self, value=self.learning_rate, min=0.00,
                                  max=1.00, inc=0.01)
        spin1.SetDigits(2)
        sizer.Add(spin1)
        self.spin1 = spin1
        sboxsp.Add(sizer, 0, wx.ALL, 8)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self, label="Sigma:                 "))
        spin2 = wx.SpinCtrlDouble(self, value=self.sigma, min=0.00, max=1.00,
                                 inc=0.01)
        spin2.SetDigits(2)
        sizer.Add(spin2)
        self.spin2 = spin2
        sboxsp.Add(sizer, 0, wx.ALL, 8)

        # Layout
        sbox = wx.StaticBox(self, label="Matrix Size")
        sboxsz = wx.StaticBoxSizer(sbox, wx.VERTICAL)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        columns = wx.SpinCtrl(self, value=self.columns, min=4, max=1000)
        sizer.Add(wx.StaticText(self, label="Columns:    "))
        sizer.Add(columns)
        self.spin_columns = columns

        sboxsz.Add(sizer, 0, wx.ALL, 8)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        rows = wx.SpinCtrl(self, value=self.rows, min=4, max=1000)
        sizer.Add(wx.StaticText(self, label="Rows:           "))
        sizer.Add(rows)
        self.spin_rows = rows
        sboxsz.Add(sizer, 0, wx.ALL, 8)

        sbox = wx.StaticBox(self, label="Map Initialization")
        sboxszm = wx.StaticBoxSizer(sbox, wx.VERTICAL)

        self.radio1 = wx.RadioButton(self, -1, " Linear ",
                                style=wx.RB_GROUP)
        self.radio1.SetValue(self.linInit)
        sboxszm.Add(self.radio1, 0, wx.ALL, 5)

        radio2 = wx.RadioButton(self, -1, " Random ")
        radio2.SetValue(not self.linInit)
        sboxszm.Add(radio2, 0, wx.ALL, 5)

        sbox = wx.StaticBox(self, label="Stopping Conditions")
        sboxszs = wx.StaticBoxSizer(sbox, wx.VERTICAL)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        iterations = wx.SpinCtrl(self, value=self.iterations, min=1,
                                 max=1000000)
        sizer.Add(wx.StaticText(self, label="Iterations:    "))
        sizer.Add(iterations)
        self.spin_iterations = iterations

        sboxszs.Add(sizer, 0, wx.ALL, 8)

        msizer = wx.BoxSizer(wx.VERTICAL)

        msizer.Add(sboxsp, 0, wx.ALL, 7)
        msizer.Add(sboxsz, 0, wx.EXPAND | wx.ALL, 7)
        msizer.Add(sboxszm, 0, wx.EXPAND | wx.ALL, 7)
        msizer.Add(sboxszs, 0, wx.EXPAND | wx.ALL, 7)
        b = wx.Button(self, 10, "Apply", (20, 20))
        b.SetDefault()
        msizer.Add(b, 0, wx.EXPAND | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.OnButtonApply, b)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(msizer, 0, wx.EXPAND)

        vsizer = wx.BoxSizer(wx.VERTICAL)

        self.som_panel = CanvasPanel(self)

        # Tomamos el id de la primera iteracion
        iterId = testConfig.test_details[0].test_datas[0].iteration_id

        self.som_panel.setParameters(iterId, self.som.sigma,
            self.som.learning_rate, self.som.columns, self.som.rows,
                            self.som.map_initialization, self.som.iterations)
        self.som_panel.initialDraw()
        vsizer.Add(self.som_panel, 3, wx.EXPAND)

        # Listctrl
        self.lc = IndividualsListCtrl(self, self.som_panel.numObjetives,
                                      style=wx.LC_REPORT)
        EVT_LIST_ITEM_RIGHT_CLICK(self.lc, -1, self.itemRightClick)

        panel = wx.Panel(self, -1)
        self.text = wx.StaticText(panel, -1, "")
        self.text.SetLabel

        vsizer.Add(panel, 0, wx.EXPAND)
        vsizer.Add(self.lc, 1, wx.EXPAND)

        sizer.Add(vsizer, 1, wx.EXPAND)

        self.testConfig = testConfig
        self.SetSizer(sizer)
        self.SetSize((900, 710))
        self.Fit()

    def initParameters(self, testConfig):
        from py.una.pol.tava.model.msom import SomModel as sm
        from py.una.pol.tava.model.mresult import ResultModel as rm
        from py.una.pol.tava.model.miteration import InterationModel as im

        # Buscaremos la instancia SOM asociada al test
        som = sm().get_som_by_test_config_id(testConfig.id)
        # som = sm().getSomById(testConfig.test_graphic[0].id_graphic)

        items = []
        # Diccionario empleado para almacenar los id de iteraciones asociadas a
        # cada opcion en el combo
        itemsDict = {}

        for tdet in testConfig.test_details:
            result = rm().getResultById(tdet.result_id)
            for tdat in tdet.test_datas:
                ite = im().getIterationById(tdat.iteration_id)
                item = str(result.name) + "\nIteration " +\
                                                        str(ite.identifier)
                items.append(item)
                itemsDict[item] = tdat.iteration_id

        self.itemsDict = itemsDict
        # Items para el combo de opciones
        self.items = items
        # Tasa de aprendizaje
        self.learning_rate = str(som.learning_rate).replace(".", ",")
        # Sigma
        self.sigma = str(som.sigma).replace(".", ",")
        # Nro de Columnas
        self.columns = str(som.columns)
        # Nro de Filas
        self.rows = str(som.rows)
        # Inicializacion del mapa
        if str(som.map_initialization) == "linear":
            self.linInit = True
        else:
            self.linInit = False
        # Cantidad de Iteraciones
        self.iterations = str(som.iterations)
        # Referencia de la instancia SOM para el panel de configuracion
        self.som = som

    def OnButtonApply(self, event):
        iterId = self.itemsDict[self.choice.GetStringSelection()]
        self.som.learning_rate = self.spin1.GetValue()
        self.som.sigma = self.spin2.GetValue()
        self.som.columns = self.spin_columns.GetValue()
        self.som.rows = self.spin_rows.GetValue()
        self.linInit = self.radio1.GetValue()
        if self.linInit:
            self.som.map_initialization = "linear"
        else:
            self.som.map_initialization = "random"
        self.som.iterations = self.spin_iterations.GetValue()
        self.som_panel.setParameters(iterId, self.som.sigma,
                    self.som.learning_rate, self.som.columns, self.som.rows,
                            self.som.map_initialization, self.som.iterations)
        if self.som_panel.rect:
            self.som_panel.rect.remove()
        self.som_panel.draw()
        self.som_panel.canvas.draw()

    def itemRightClick(self, event):
        menu = wx.Menu()
        show_in_parallel = wx.MenuItem(menu, wx.ID_ANY, 'Show In Parallel')
        menu.AppendItem(show_in_parallel)
        menu.Bind(wx.EVT_MENU, self.OnShowInParallel, show_in_parallel)
        self.lc.PopupMenu(menu)
        menu.Destroy()

    def OnShowInParallel(self, event):
        print(self.lc.getSelectIndices())
        for idx in self.lc.getSelectIndices():
            a = self.lc.GetItemText(idx)
            print a
        SomParallelCoordinateDialog(self, self.som_panel.individuals,
                                    self.lc.columns)


class SomParallelCoordinateDialog(wx.Dialog):

    def __init__(self, parent, individuals, columns):
        super(SomParallelCoordinateDialog, self).__init__(parent,
                                                          size=(900, 630))

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111, xlim=(0, 1), ylim=(0, 1),
                                 autoscale_on=False)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)

        mydata = DataFrame(individuals, columns=columns)
        myres = range(1, len(individuals) + 1)
        mydata['res'] = myres
        parallel_coordinates(mydata, 'res', ax=self.axes)
        self.axes.legend().set_visible(False)
        self.canvas.draw()
        self.axes.set_title('Individuals')

        #------ Definiciones iniciales -----
        self.Centre(wx.BOTH)
        self.CenterOnScreen()
        # self.sizer.Fit(self)
        # self.sizer.SetSizeHints(self)
        # self.Layout()
        # self.Fit()
        self.ShowModal()


if __name__ == "__main__":
    # from py.una.pol.tava.base.entity import createDB
    # createDB()
    from py.una.pol.tava.model.mtestconfig import TestConfigModel as tm
    testConfig = tm().getTestConfigById(1)
    app = wx.App()
    fr = wx.Frame(None, title='Configuration')
    panel = PanelSomConfig(fr, testConfig)
    fr.Centre(wx.BOTH)
    fr.Fit()
    fr.Show()
    app.MainLoop()
