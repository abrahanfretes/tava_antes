'''
Created on 17/3/2015

@author: abrahan
'''
import wx
import py.una.pol.tava.view.vimages as I

from wx import GetTranslation as _
import py.una.pol.tava.view.vi18n as C

# -------------------         Panel Principal          ------------------------
# -------------------                                  ------------------------
from py.una.pol.tava.presenter.pparallelcoordinatesgf\
    import WorkingPageParallelGFPresenter


class WorkingPageParallelGF(wx.Panel):
    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        #  ------ self customize -----------------------------------------
        #  ------ self components ----------------------------------------
        self.presenter = WorkingPageParallelGFPresenter(self)
        tree = ParallelTreeGF(self, test)
        figure = ParallelFigureGF(self, test)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(tree, 1, wx.EXPAND)
        sizer.Add(figure, 3, wx.EXPAND)
        self.SetSizer(sizer)
        #  ------ self controls ------------------------------------------

# -------------------         Panel Tree               ------------------------
# -------------------                                  ------------------------
import wx.lib.agw.customtreectrl as CT
from py.una.pol.tava.presenter.pparallelcoordinatesgf\
    import ParallelTreeGFPresenter


class ParallelTreeGF(CT.CustomTreeCtrl):
    def __init__(self, parent, test):
        CT.CustomTreeCtrl.__init__(self, parent, agwStyle=CT.TR_HIDE_ROOT)

        #  ------ self customize -----------------------------------------
        il = wx.ImageList(16, 16)
        self.file_bmp = il.Add(I.filegraph_png)
        self.AssignImageList(il)
        self.SetBackgroundColour('#D9F0F8')
        #  ------ self components ----------------------------------------
        self.presenter = ParallelTreeGFPresenter(self, test)

        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnChecked)
        #  ------ self controls ------------------------------------------

    def OnChecked(self, event):
        self.presenter.setCheckedGF()


# -------------------         Panel Figure             ------------------------
# -------------------                                  ------------------------
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar

from py.una.pol.tava.presenter.pparallelcoordinatesgf\
    import ParallelFigureGFPresenter


class ParallelFigureGF(wx.Panel):
    '''
    '''
    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        #  ------ self customize -----------------------------------------
        #  ------ self components ----------------------------------------
        self.parent = parent

        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()

        self.button_tolbar = ButtonsTollFigureGF(self)

        self.sizer_toll = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_toll.Add(self.button_tolbar, 4, wx.EXPAND)
        self.sizer_toll.Add(self.toolbar, 1)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer_toll, 0, wx.LEFT | wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

        self.presenter = ParallelFigureGFPresenter(self, test)
        #  ------ self controls ------------------------------------------

# -------------------         Panel Toll Figure        ------------------------
# -------------------                                  ------------------------
from py.una.pol.tava.presenter.pparallelcoordinatesgf\
    import ButtonsTollFigureGFPresenter


class ButtonsTollFigureGF(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
        self.SetBackgroundColour('#f8f1d9')

        # ------ self components --------------------------------------

        self.test = wx.Button(self, -1, _(C.BTFGF_FT))
        self.test.SetToolTipString(_(C.BTFGF_FT_T))

        self.result = wx.Button(self, -1, _(C.BTFGF_FR))
        self.result.SetToolTipString(_(C.BTFGF_FR_T))

        self.iteration = wx.Button(self, -1, _(C.BTFGF_FI))
        self.iteration.SetToolTipString(_(C.BTFGF_FI_T))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.test, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=5)
        sizer.Add(self.result, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.iteration, 0, wx.ALIGN_CENTER_VERTICAL)
        self.SetSizer(sizer)

        self.presenter = ButtonsTollFigureGFPresenter(self)

        # ------ self inicailes executions ----------------------------
        self.Bind(wx.EVT_BUTTON, self.OnTestGrafic, self.test)
        self.Bind(wx.EVT_BUTTON, self.OnResultGrafic, self.result)
        self.Bind(wx.EVT_BUTTON, self.OnIterationGrafic, self.iteration)

    # ------ self controls --------------------------------------------

    def OnTestGrafic(self, event):
        self.presenter.testGrafic()

    def OnResultGrafic(self, event):
        self.presenter.resultGrafic()

    def OnIterationGrafic(self, event):
        self.presenter.iterationGrafic()
