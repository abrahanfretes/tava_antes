__author__ = 'amfv'
from py.una.pol.tava.view import agreggation as ag
from py.una.pol.tava.presenter.pensemble import EnsembleMethod,\
PanelEnsemblePresenter
import wx
import wx.lib.agw.ultimatelistctrl as ULC
import py.una.pol.tava.dao.dmetric as dm

# dictMetrics = {
#     'GD': ag.MIN,
#     'IGD': ag.MIN,
#     'Convergence': ag.MIN,
#     'Spacing': ag.MIN,
#     'Spread': ag.MAX,
#     'Tiempo': ag.MIN,
#     'AvgSumObjs': ag.MAX,
#     'MaxSum': ag.MAX,
#     'MinSum': ag.MIN,
#     'SumMax': ag.MAX,
#     'SumMin': ag.MIN,
#     'Range': ag.MIN
# }


class MetricConfigDialog(wx.Dialog):

    def __init__(self, parent, id_result_metric):
        super(MetricConfigDialog, self).__init__(parent,
                                                 title="Metric Config",
                                                 size=(250, 500))

        list_m = ULC.UltimateListCtrl(self, wx.ID_ANY,
            agwStyle=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES |
            wx.LC_SINGLE_SEL | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)

        list_m.InsertColumn(0, "Metric", width=150)
        list_m.InsertColumn(1, "Values")

        list_metrics = dm.getDistinctMetrics(id_result_metric)

        index = 0
        for i, in list_metrics:
            list_m.InsertStringItem(index, i)
            choice = wx.Choice(list_m, -1, choices=[ag.MAX, ag.MIN])
            choice.SetSelection(1)
            list_m.SetItemWindow(index, 1, choice, expand=True)
            index += 1

        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # Definicion del boton cancel
        cancel_btn = wx.Button(self, -1, "Cancel")
        cancel_btn.Bind(wx.EVT_BUTTON, self.OnCancel, id=cancel_btn.GetId())

        # Definicion del boton apply
        self.apply_btn = wx.Button(self, -1, "Apply")
        # self.apply_btn.Enable(False)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.OnApply,
                  id=self.apply_btn.GetId())

        # Agregamos los botones al sizer hbox3
        hsizer.Add(cancel_btn, 1, wx.RIGHT)
        hsizer.Add(self.apply_btn)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(list_m, 1, wx.EXPAND)
        self.list_m = list_m
        sizer.Add(hsizer, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT
                  | wx.BOTTOM, 10)
        self.SetSizer(sizer)
        self.Centre(wx.BOTH)
        self.CenterOnScreen()
        self.ShowModal()

    def OnCancel(self, event):
        self.Close()

    def OnApply(self, event):
        count = self.list_m.GetItemCount()
        for row in range(count):
            item = self.list_m.GetItem(row)
            wnd = self.list_m.GetItemWindow(row, col=1)
            self.Parent.dict_metric[item.GetText()] = wnd.GetStringSelection()
        self.Close()


class PanelEnsembleConfig(wx.Panel):
    def __init__(self, parent, test):
        super(PanelEnsembleConfig, self).__init__(parent)

        self.ensemble_method = EnsembleMethod()

        self.presenter = PanelEnsemblePresenter(self)

        self.result_metric = dm.getResultMetricById(test.result_metric_id)

        self.dict_metric = {}

        self.config_metric_dialog = None

        msizer = wx.BoxSizer(wx.VERTICAL)

        text = wx.StaticText(self, label="Ensemble Method: ")
        font = text.GetFont()
        font.SetWeight(wx.BOLD)
        text.SetFont(font)

        msizer.Add(text)

        # Radios
        self.radio1 = wx.RadioButton(self, -1, " for each Algorithm ",
                                     style=wx.RB_GROUP)
        msizer.Add(self.radio1, 0, wx.ALL, 5)

        self.radio2 = wx.RadioButton(self, -1,
                                     " for each Parallelization Method ")
        msizer.Add(self.radio2, 0, wx.ALL, 5)

        #  Boton de Configuracion de metricas
        metrics_button = wx.Button(self, 10, "Configure Metrics", (20, 20))
        metrics_button.Bind(wx.EVT_BUTTON, self.on_button_config_metrics,
                            metrics_button)
        msizer.Add(metrics_button, 0, wx.EXPAND | wx.ALL, 5)

        #  Boton de ejecucion
        execute_button = wx.Button(self, 10, "Execute", (20, 20))
        execute_button.Bind(wx.EVT_BUTTON, self.on_button_execute,
                            execute_button)
        msizer.Add(execute_button, 0, wx.EXPAND | wx.ALL, 5)

        vsizer = wx.BoxSizer(wx.VERTICAL)

        self.list_ctrl = wx.ListCtrl(self, size=(-1, 100),
                                     style=wx.LC_REPORT | wx.BORDER_SUNKEN)

        vsizer.Add(self.list_ctrl, 3, wx.EXPAND)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(msizer, 0, wx.EXPAND)
        sizer.Add(vsizer, 1, wx.EXPAND)

        self.SetSizer(sizer)
        self.SetSize((900, 710))
        self.Fit()

    def on_button_config_metrics(self, event):
        if not self.config_metric_dialog:
            self.config_metric_dialog = MetricConfigDialog(self,
                                                        self.result_metric.id)
        else:
            self.config_metric_dialog.ShowModal()

    def on_button_execute(self, event):
        if not self.dict_metric:
            dlg = wx.MessageDialog(self,
            "Las metricas no han sido configuradas, desea continuar?", "Info",
                    wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_NO:
                return
            dlg.Destroy()
            # Por default inicializa las metricas con la condicion de Minimo
            list_metrics = dm.getDistinctMetrics(self.result_metric.id)
            for i, in list_metrics:
                self.dict_metric[i] = ag.MIN

        # Ventana de espera durante el procesamiento
        import wx.lib.agw.pybusyinfo as PBI
        message = "Please wait 5 seconds, working..."
        busy = PBI.PyBusyInfo(message, parent=self.GetParent(),
                              title="Really Busy")
        wx.Yield()

        self.ensemble_method.set_by_moea(self.radio1.GetValue())
        self.ensemble_method.set_dict_metric(self.dict_metric)
        self.ensemble_method.set_result_metric(self.result_metric)

#         invocamos al ensemble method para evaluar los datos con las metricas
#         configuradas.
        list_results = self.ensemble_method.execute_ensemble_method()

        # Limpiamos el listado principal
        self.list_ctrl.ClearAll()

        # Dibujamos el listado para la opcion por cada metodo evolutivo
        if self.radio1.GetValue():
            self.presenter.prepare_listctrl_by_moea(list_results)
        else:
            # Dibujamos el listado para la opcion por cada metodo paralelo
            self.presenter.prepare_listctrl_by_parallel_method(list_results)

        # Se elimina la ventana de espera de procesamiento
        del busy

if __name__ == "__main__":
    from py.una.pol.tava.dao.dmetric import getResultMetricById
    result_metric = getResultMetricById(1)
    app = wx.App()
    fr = wx.Frame(None, title='Configuration')
    panel = PanelEnsembleConfig(fr, result_metric)
    fr.SetSize((1000, 500))
    fr.Centre(wx.BOTH)
    fr.Show()
    app.MainLoop()
