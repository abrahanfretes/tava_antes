#  -*- coding: utf-8 -*-
'''
Created on 2/5/2015

@author: abrahan
'''
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from wx import GetTranslation as _

from py.una.pol.tava.view import vi18n as C
from py.una.pol.tava.view import vimages as I


# ------------------- Panel Para Grafico De Coordenadas Paralelas -------------
# -------------------                                  ------------------------
class CurvesFigure(wx.Panel):
    '''
    Clase Panel que contiene la configuracion para la visualizacion del
    componente de coordenadas paralelas.
    '''
    def __init__(self, parent, page_curves, test):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
        # ------ self components --------------------------------------
        self.parent = parent
        self.page_curves = page_curves

        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()

        self.button_execution = wx.BitmapButton(self, -1, I.graficar_parallel,
                                                style=wx.NO_BORDER)
        self.button_execution.SetToolTipString(_(C.BTF_UF))
        s_line_update = wx.StaticLine(self, style=wx.LI_VERTICAL)
        self.update_filters = wx.BitmapButton(self, -1, I.update_figure,
                                              style=wx.NO_BORDER)
        self.update_filters.SetToolTipString(_(C.BTF_ESF))
        self.clean_filter = wx.BitmapButton(self, -1, I.clear_filters,
                                            style=wx.NO_BORDER)
        self.clean_filter.SetToolTipString(_(C.BTF_CF))

        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_button.Add(self.button_execution)
        sizer_button.Add(s_line_update,
                         flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)
        sizer_button.Add(self.update_filters)
        sizer_button.Add(self.clean_filter)

        self.sizer_toll = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_toll.Add(sizer_button, 4)
        self.sizer_toll.Add(self.toolbar, 1)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer_toll, 0, wx.LEFT | wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

        # ------ self inicailes executions ----------------------------
        self.button_execution.Bind(wx.EVT_BUTTON, self.OnClickExecution)
        self.update_filters.Bind(wx.EVT_BUTTON, self.OnClickFilter)
        self.clean_filter.Bind(wx.EVT_BUTTON, self.OnClickCleanFilter)

        self.button_execution.Disable()
        self.update_filters.Disable()
        self.clean_filter.Disable()
        self.presenter = CurvesFigurePresenter(self, test)

    # ------ self controls --------------------------------------------

    def OnClickExecution(self, event):
        self.page_curves.updateDatas()
        self.update_filters.Enable()

    def OnClickFilter(self, event):
        if self.page_curves.verificFilter():
            self.clean_filter.Enable()
            self.update_filters.Disable()

    def OnClickCleanFilter(self, event):
        self.page_curves.cleanFilter()
        self.clean_filter.Disable()
        self.update_filters.Enable()

    def enableButtons(self):
        self.button_execution.Enable()
        if self.presenter.containsFilter():
            self.clean_filter.Enable()

    def disableButtons(self):
        self.button_execution.Disable()


from py.una.pol.tava.model.mcurves import AndrewsCurvesModel as acm


# ------------------- Clase Presentador de Figura Coordenadas Paralelas  ------
# -------------------                                  ------------------------
class CurvesFigurePresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        self.figure_axes = None
        self.title_g = ''
        self.ite_list = []

        self.Init()

    def Init(self):

        ac = self.__getAC()
        self.__setBackGroundFigure(ac.colors_backgrounds)

    # ---- Metodos usados con Topic -----------
    # ---                           -----------
    def newFigure(self, ite_list):
        self.ite_list = ite_list
        self.newFigureTest(self.ite_list)

    def setBackGroundFigurePub(self, message):
        self.__setBackGroundFigure(message.data)

    def setGridFigurePub(self, message):
        if self.figure_axes is not None:
            self.newFigureTest(self.ite_list)

    # ---- Metodos usados No Localmente -----------
    # ---                               -----------

    def newFigureTestShowPub(self, message):
        ite_list = message.data
        self.newFigureTest(ite_list)

    def newFigureTest(self, ite_list, suptitle=''):
        pa = self.__getAC()
        self.color_g = (pa.color_lines,)
        self.legend_g = pa.legent
        self.__cleanParallelFigure()
        suptitle = self.title_g
        self.figure_axes = self._initFigurePaint(ite_list, suptitle)

    def getAdrewsCurves(self):
        return self.__getAC()

    # ---- Metodos usados Localmente -----------
    # ---                            -----------

    def __getAC(self):
        return acm().getCurvesByTestId(self.test.id)

    def __setBackGroundFigure(self, backColor):
        list_bac = backColor.split(',')
        self.iview.figure.set_facecolor(list_bac[1])
        self.iview.SetBackgroundColour(list_bac[2])
        self.iview.toolbar.SetBackgroundColour(list_bac[2])
        self.iview.canvas.draw()

    def __cleanParallelFigure(self):
        if not(self.figure_axes is None):
            self.iview.figure.delaxes(self.figure_axes)

    def _initFigurePaint(self, ite_list, suptitle='', sp_axe=None):
        axe = None
        if sp_axe is None:
            axe = self.iview.figure.gca()
        else:
            axe = self.iview.figure.add_subplot(sp_axe)
        self.iview.figure.suptitle(suptitle)
        axe = self._figurePaint(axe, ite_list)
        return axe

    def _figurePaint(self, axe, ite_list, count_last=0):
        _pos = 0 + count_last
        _len = len(ite_list) + count_last
        for iteration in ite_list:
            axe = acm().getCurvesAxe(iteration, _len, _pos, axe,
                                     self.legend_g, self.color_g)
            # ac = self.__getAC()
            # axe = self._setAddConfigGrip(axe, ac.figure_grid)

            self.iview.canvas.draw()
            _pos += 1
        self.iview.canvas.draw()
        return axe
    # --------------------------------------------------------------------------

    #===========================================================================
    # def _setAddConfigGrip(self, axe, figure_grid):
    #     fg = figure_grid
    #     if fg.grid:
    #         o_axis = tvc.ORIENTATION_LINE_AL[fg.orientation]
    #         s_linestyle = tvc.STYLE_LINE_AL[fg.red_style]
    #         axe.grid(b=True,  which='major', axis=o_axis,
    #                  color=fg.red_color, linestyle=s_linestyle,
    #                  linewidth=fg.red_width)
    #     else:
    #         axe.grid(fg.grid)
    #     return axe
    #===========================================================================

    def containsFilter(self):
        ac = acm().getCurvesByTestId(self.test.id)
        return not (ac.maxs_objetive is None or ac.mins_objetive is None)
