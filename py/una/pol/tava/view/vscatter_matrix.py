'''
Created on 03/05/2015

@author: arsenioferreira
'''
import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
from pandas.tools.plotting import scatter_matrix
from pandas import DataFrame
import numpy as np
import pylab
from py.una.pol.tava.model.mresult import ResultModel as rm
from py.una.pol.tava.model.miteration import InterationModel as im


class PanelScatterMatrix(wx.Panel):
    '''
    Clase que contiene la Figura que representa a la matriz dispersa
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111, xlim=(0, 1), ylim=(0, 1),
                                 autoscale_on=False)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.add_toolbar()
        self.SetSizer(self.sizer)
        self.Fit()

    def add_toolbar(self):
        """copied verbatim from embedding_wx2.py"""
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()
        tw, th = self.toolbar.GetSizeTuple()
        fw, fh = self.canvas.GetSizeTuple()
        self.toolbar.SetSize(wx.Size(fw, th))
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.toolbar.update()

    def setParameters(self, iterDir):
        self.iterId = iterDir

    def draw(self):
        from py.una.pol.tava.dao.dindividual import getIndividualsByIteracionId
        individuals = getIndividualsByIteracionId(self.iterId)
        data = ""
#         c = 0
        for individual in individuals:
            data += str(individual.objectives) + "\n"
#             if c == 3:
#                 break  #sacarrrrr
#             c = c + 1
        from StringIO import StringIO
        datos = np.genfromtxt(StringIO(data), delimiter=',')
        data = None
        data = datos
        pylab.clf()

        df = DataFrame(data)

        axs = scatter_matrix(df, alpha=0.2, ax=self.axes)
        n = len(df.columns)
        for x in range(n):
            for y in range(n):
                # to get the axis of subplots
                ax = axs[x, y]
                # to make x axis name vertical
                ax.xaxis.label.set_rotation(90)
                # to make y axis name horizontal
                ax.yaxis.label.set_rotation(0)
                # to make sure y axis names are outside the plot area
                ax.yaxis.labelpad = 50


class PanelScatterMatrixCongif(wx.Panel):
    def __init__(self, parent, testConfig):
        super(PanelScatterMatrixCongif, self).__init__(parent)

        self.initParameters(testConfig)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Parameters
        sbox = wx.StaticBox(self, label="Parameters")
        sboxsp = wx.StaticBoxSizer(sbox, wx.VERTICAL)

        # Attributes
        self.choice = wx.Choice(self, size=(200, 30), choices=self.itemsCombo)
        self.choice.SetSelection(0)
        csizer = wx.BoxSizer(wx.VERTICAL)
        csizer.Add(wx.StaticText(self, label="Select one: "))
        csizer.Add(self.choice)
        sboxsp.Add(csizer, 0, wx.ALL, 8)

        apply_button = wx.Button(self, 10, "Apply", (20, 20))
        apply_button.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.OnButtonApply, apply_button)

        msizer = wx.BoxSizer(wx.VERTICAL)

        msizer.Add(sboxsp, 0, wx.ALL, 7)
        msizer.Add(apply_button, 0, wx.EXPAND | wx.ALL, 5)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.scatter_matrix_panel = PanelScatterMatrix(self)

        # Tomamos el id de la primera iteracion
        iterId = testConfig.test_details[0].test_datas[0].iteration_id

        self.scatter_matrix_panel.setParameters(iterId)
        self.scatter_matrix_panel.draw()
        vsizer.Add(self.scatter_matrix_panel, 3, wx.EXPAND)

        sizer.Add(msizer, 0, wx.EXPAND)
        sizer.Add(vsizer, 1, wx.EXPAND)

        self.testConfig = testConfig
        self.SetSizer(sizer)
        self.SetSize((900, 710))
        self.Fit()

    def initParameters(self, testConfig):
        # Items para el combo de opciones
        self.itemsCombo = []
        # Diccionario empleado para almacenar los id de iteraciones asociadas a
        # cada opcion en el combo
        self.itemsDict = {}

        for tdet in testConfig.test_details:
            result = rm().getResultById(tdet.result_id)
            for tdat in tdet.test_datas:
                ite = im().getIterationById(tdat.iteration_id)
                item = str(result.name) + "\nIteration " +\
                                                        str(ite.identifier)
                self.itemsCombo.append(item)
                self.itemsDict[item] = tdat.iteration_id

    def OnButtonApply(self, event):
        iterId = self.itemsDict[self.choice.GetStringSelection()]
        self.scatter_matrix_panel.setParameters(iterId)
        self.scatter_matrix_panel.draw()
        self.scatter_matrix_panel.canvas.draw()

if __name__ == "__main__":
    from py.una.pol.tava.model.mtestconfig import TestConfigModel as tm
    testConfig = tm().getTestConfigById(1)
    app = wx.App()
    fr = wx.Frame(None, title='Configuration')
    panel = PanelScatterMatrixCongif(fr, testConfig)
    fr.Centre(wx.BOTH)
    fr.Fit()
    fr.Show()
    app.MainLoop()
