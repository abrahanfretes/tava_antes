'''
Created on 28/11/2014

@author: arsenioferreira
'''
from minisom import MiniSom
from numpy import genfromtxt, linalg, apply_along_axis

"""
    This script shows how to use MiniSom on the Iris dataset.
In particular it shows how to train MiniSom and how to visualize the result.
    ATTENTION: pylab is required for the visualization.
"""

import wx
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from pylab import get_cmap


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

    def initParameters(self, testConfig):
        panelSom = self.GetParent()
        self.iterId = testConfig.test_details[0].test_datas[0].iteration_id
        self.sigma = float(panelSom.sigma.replace(",", "."))
        self.learning_rate = float(panelSom.learning_rate.replace(",", "."))
        self.columns = int(panelSom.columns)
        self.rows = int(panelSom.rows)

    def updateParameters(self, som, iterId):
        self.iterId = iterId
        self.sigma = som.sigma
        self.learning_rate = som.learning_rate
        self.columns = som.columns
        self.rows = som.rows

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
        print("Training...")
        som.train_batch(data, 100)  # random training
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

        ### Plotting the response for each pattern in the iris dataset ###
        # plotting the distance map as background
        self.axes.pcolor(som.distance_map().T, cmap=get_cmap('gray'))
        cax = self.axes.imshow(data, interpolation='nearest',
                               cmap=get_cmap('gray'))
        self.figure.colorbar(cax)

        self.axes.axis([0, som.weights.shape[0], som.weights.shape[1], 0])
        self.som = som

        def onpick4(event):
#             print "on_press"
            if event.xdata and event.ydata:
                xdata = int(event.xdata)
                ydata = int(event.ydata)
                print 'onpick points:', xdata, ydata
                print 'cantidad de individuals del som:',
                len(self.som.individuals[xdata][ydata])

                self.GetParent().lc.DeleteAllItems()

                for cnt, ind in enumerate(self.som.individuals[xdata][ydata]):
                    for c, i in enumerate(ind):
                        if c == 0:
                            self.GetParent().lc.InsertStringItem(cnt, str(i))
                        else:
                            self.GetParent().lc.SetStringItem(cnt, c, str(i))

        self.figure.canvas.mpl_connect('button_press_event', onpick4)


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

        radio1 = wx.RadioButton(self, -1, " Linear ",
                                style=wx.RB_GROUP)
        radio1.SetValue(self.linInit)
        sboxszm.Add(radio1, 0, wx.ALL, 5)

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
        self.som_panel.initParameters(testConfig)
        self.som_panel.initialDraw()
        vsizer.Add(self.som_panel, 3, wx.EXPAND)

        # Listctrl
        self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        # Se insertan dos columnas
        for i in range(self.som_panel.numObjetives):
            self.lc.InsertColumn(i, 'Objetivo ' + str(i))
            self.lc.SetColumnWidth(i, 140)
#             self.lc.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)

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
        som = sm().getSomById(testConfig.test_graphic[0].id_graphic)

        items = []
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

        self.items = items

        self.learning_rate = str(som.learning_rate).replace(".", ",")
        self.sigma = str(som.sigma).replace(".", ",")
        self.columns = str(som.columns)
        self.rows = str(som.rows)
        if str(som.map_initialization) == "linear":
            self.linInit = True
        else:
            self.linInit = False
        self.iterations = str(som.iterations)
        self.som = som

    def OnButtonApply(self, event):
        iterId = self.itemsDict[self.choice.GetStringSelection()]
        self.som.learning_rate = self.spin1.GetValue()
        self.som.sigma = self.spin2.GetValue()
        self.som.columns = self.spin_columns.GetValue()
        self.som.rows = self.spin_rows.GetValue()
        self.som_panel.updateParameters(self.som, iterId)
        self.som_panel.draw()
        self.som_panel.canvas.draw()


if __name__ == "__main__":
    from py.una.pol.tava.base.entity import createDB
    createDB()
    from py.una.pol.tava.model.mtestconfig import TestConfigModel as tm
    testConfig = tm().getTestConfigById(1)
    a = str(testConfig.test_graphic[0].name_graphic)
    app = wx.App()
    fr = wx.Frame(None, title='Configuration')
    panel = PanelSomConfig(fr, testConfig)
    fr.Centre(wx.BOTH)
    fr.Fit()
    fr.Show()
    app.MainLoop()
