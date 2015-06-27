__author__ = 'amfv'
from py.una.pol.tava.view import agreggation as ag
from py.una.pol.tava.dao.dmetric import getMaxValueMetricByMoea, getMinValueMetricByMoea, getDistinctMetrics
import py.una.pol.tava.dao.dmetric as dm
import random
import sys
import wx
from time import time

dictMetrics = {
    'GD': ag.MIN,
    'IGD': ag.MIN,
    'Convergence': ag.MIN,
    'Spacing': ag.MIN,
    'Spread': ag.MAX,
    'Tiempo': ag.MIN,
    'MaxSum': ag.MAX,
    'MinSum': ag.MIN
}

def getRandomItem(list_):
    random.shuffle(list_)
    return random.choice(list_)

def deleteItemFromList(item, list_):
    list_.pop(list_.index(item))

def evaluateIndividuals(individual_1, individual_2, condition):
    if condition == ag.MAX:
        return max(individual_1, individual_2), min(individual_1, individual_2)
    else:
        return min(individual_1, individual_2), max(individual_1, individual_2)

def getWinnerAndLoserIndividuals(individuals_):
    if len(individuals_) == 1:
        individual = individuals_[0]
        deleteItemFromList(individual, individuals_)
        return individual, individual
    individual_1 = getRandomItem(individuals_)
    deleteItemFromList(individual_1, individuals_)
    individual_2 = getRandomItem(individuals_)
    deleteItemFromList(individual_2, individuals_)
    idMetric, condition = getRandomItem(dictMetrics.items())
    return evaluateIndividuals(individual_1, individual_2, condition)

def evaluateWinnersAndLosers(individuals_, winners_, losers_):
    while len(individuals_) > 0:
        winner_, loser_ = getWinnerAndLoserIndividuals(individuals_)
        winners_.append(winner_)
        losers_.append(loser_)

def evaluateWinnersAndLosersOneByOne(winners_l, losers_w, winners_l_w, losers_l_w):
    for ind_1, ind_2 in zip(winners_l, losers_w):
        idMetric, condition = getRandomItem(dictMetrics.items())
        winner_, loser_ = evaluateIndividuals(ind_1, ind_2, condition)
        winners_l_w.append(winner_)
        losers_l_w.append(loser_)

def deleteLosers(individuals_, losers_l_w_, losers_l_):
    for ind in losers_l_w_:
        if ind in individuals_:
            individuals_.remove(ind)

    for ind in losers_l_:
        if ind in individuals_:
            individuals_.remove(ind)

def deleteIndividualsFromWinnerMoea(ind_winner_, individuals_):
    id_p = ind_winner_.population.metric.parallelization_method.id
    to_delete = []
    for ind in individuals_:
        if ind[0] == id_p:
            to_delete.append(ind)
    for ind in to_delete:
        individuals_.remove(ind)
    return id_p

# if __name__ == "__main_":
def ensemble_method(result_metric, for_each_algorithm):

    start_time = time()
    list_results = []

    if for_each_algorithm:
        # c = 1
        for moea_problem in result_metric.moea_problems:
            for number_objective in moea_problem.number_objectives:
                for evolutionary_method in number_objective.evolutionary_methods:
                    for number_thread in evolutionary_method.number_threads:
                        parallel_method_list = number_thread.parallelization_methods
                        result = generate_aproximation_front(parallel_method_list)
                        list_results.append((moea_problem.name, number_objective.value,
                                        evolutionary_method.name, number_thread.value, result))
                    break
                    if c == 2:
                        break
                    c = c + 1
                break
            break
    else:
        pass
        # parallel_method_list = dm.getDistinctParallelMethodsByResultMetric(result_metric.id)
        # dm.getDistinctParallelMethodsByResultMetric(result_metric.id)
        # for moea_problem in result_metric.moea_problems:
        #     for number_objective in moea_problem.number_objectives:
            #     for evolutionary_method in number_objective.evolutionary_methods:
            #         for number_thread in evolutionary_method.number_threads:
            #             parallel_method_list = number_thread.parallelization_methods
            #             result = generate_aproximation_front(parallel_method_list)
            #             list_results.append((moea_problem.name, number_objective.value,
            #                             evolutionary_method.name, number_thread.value, result))
    elapsed_time = time() - start_time
    print("Elapsed time: %0.10f seconds." % elapsed_time)
    return list_results
# double_tournament_elimination
def generate_aproximation_front(parallel_method_list):
    if len(parallel_method_list) == 1:
        return [parallel_method_list[0].name]
    # EpsDOM
    # parallel_method_list = [1, 2, 3, 4, 5, 6, 7, 8]

    valuesPopulation = range(30)

    # metrics = getDistinctMetrics()

    # for metric, in metrics:
    #     cond = getRandomItem([ag.MAX, ag.MIN])
    #     dictMetrics[metric] = cond

    approximation_fronts = []
    selected_parallel_methods = []
    ranking_moeas = []
    # Step 1 Generate 50 approximation front
    for value_population in valuesPopulation:
        metric_name, condition = getRandomItem(dictMetrics.items())
        parallel_method = getRandomItem(parallel_method_list)
        metric = None
        if condition == ag.MAX:
            metric = getMaxValueMetricByMoea(
                parallel_method.id,
                metric_name,
                value_population)
        else:
            metric = getMinValueMetricByMoea(
                parallel_method.id,
                metric_name,
                value_population)
        # print("Id del valor: " + str(metric.id))
        # print("valor: " + str(metric.value))
        approximation_fronts.append((parallel_method.id, metric))
        if parallel_method.id not in selected_parallel_methods:
            selected_parallel_methods.append(parallel_method.id)
        # sys.exit()

    # Step 2: Use Double-Tournament Selection to get the best one individual:
    individuals = list(approximation_fronts)
    # print(individuals)
    while len(selected_parallel_methods) > 1:
        round_individuals = [i[1] for i in individuals]

        winners = []
        winners_w = []
        winners_l = []
        winners_l_w = []

        losers = []
        losers_w = []
        losers_l = []
        losers_l_w = []

        evaluateWinnersAndLosers(round_individuals, winners, losers)

        ind_winner = None
        while True:
            if len(winners) == 1:
                idMetric, condition = getRandomItem(dictMetrics.items())
                w_, l_ = evaluateIndividuals(winners[0], losers[0], condition)
                if w_ in winners:
                    ind_winner = w_
                else:
                    idMetric, condition = getRandomItem(dictMetrics.items())
                    w_, l_ = evaluateIndividuals(winners[0], losers[0], condition)
                    ind_winner = w_
                break

            evaluateWinnersAndLosers(winners, winners_w, winners_l)

            evaluateWinnersAndLosers(losers, losers_w, losers_l)

            evaluateWinnersAndLosersOneByOne(winners_l, losers_w, winners_l_w, losers_l_w)
            # deleteLosers(individuals, losers_l_w, losers_l)

            # Siguientes rondas
            winners = winners_w
            winners_w = []
            winners_l = []

            losers = winners_l_w
            losers_l = []
            losers_w = []

            winners_l_w = []
            losers_l_w = []
            pass
        id_p = deleteIndividualsFromWinnerMoea(ind_winner, individuals)

        # removemos de los moeas seleccionados
        try:
            selected_parallel_methods.remove(id_p)
        except ValueError:
            print("Error")
        # agregamos al ranking de moeas
        name = ind_winner.population.metric.parallelization_method.name
        ranking_moeas.append(name)

    name = individuals[0][1].population.metric.parallelization_method.name
    ranking_moeas.append(name)
    # print("Ranking de MOEAS:")
    # print(ranking_moeas)
    # print("Algoritmo ganador: " + ind_winner.population.metric.parallelization_method.number_threads.evolutionary_method.name)
    # elapsed_time = time() - start_time
    # print("Elapsed time: %0.10f seconds." % elapsed_time)
    pass
    return ranking_moeas

class PanelEnsembleConfig(wx.Panel):
    def __init__(self, parent, result_metric):
        super(PanelEnsembleConfig, self).__init__(parent)

        self.result_metric = result_metric

        msizer = wx.BoxSizer(wx.VERTICAL)

        text = wx.StaticText(self, label="Double Tournament Elimination: ")
        font = text.GetFont()
        font.SetWeight(wx.BOLD)
        text.SetFont(font)
        msizer.Add(text)

        self.radio1 = wx.RadioButton(self, -1, " for each Algorithm ", style=wx.RB_GROUP)
        # radio1.SetValue(True)
        msizer.Add(self.radio1, 0, wx.ALL, 5)

        self.radio2 = wx.RadioButton(self, -1, " for each Parallelization Method ")
        # radio2.SetValue(False)
        msizer.Add(self.radio2, 0, wx.ALL, 5)

        b = wx.Button(self, 10, "Execute", (20, 20))
        self.Bind(wx.EVT_BUTTON, self.OnButtonApply, b)
        msizer.Add(b, 0, wx.EXPAND | wx.ALL, 5)

        vsizer = wx.BoxSizer(wx.VERTICAL)

        self.list_ctrl = wx.ListCtrl(self, size=(-1,100), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, 'Problem')
        self.list_ctrl.InsertColumn(1, 'Number of Objectives', width=145)
        self.list_ctrl.InsertColumn(2, 'MOEA')
        self.list_ctrl.InsertColumn(3, 'Number of Threads', width=130)

        vsizer.Add(self.list_ctrl, 3, wx.EXPAND)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(msizer, 0, wx.EXPAND)
        sizer.Add(vsizer, 1, wx.EXPAND)

        self.SetSizer(sizer)
        self.SetSize((900, 710))
        self.Fit()

    def OnButtonApply(self, event):
        # Ventana de procesamiento
        wait = wx.BusyInfo("Please wait, working...")
        list_results = []
        # For each Algorithm
        if self.radio1.GetValue():
            list_results = ensemble_method(self.result_metric, True)
        else:
            list_results = ensemble_method(self.result_metric, False)

        # Se selecciona la maxima longitud de la cuarta fila, para la columna 4, ya que contiene un listado
        max_len = max([len(i[4]) for i in list_results])

        for i in range(max_len):
            self.list_ctrl.InsertColumn(4 + i, 'Winner ' + str(i + 1))

        index = 0
        for i in list_results:
            self.list_ctrl.InsertStringItem(index, i[0])
            self.list_ctrl.SetStringItem(index, 1, str(i[1]))
            self.list_ctrl.SetStringItem(index, 2, i[2])
            self.list_ctrl.SetStringItem(index, 3, str(i[3]))
            for idx, ii in enumerate(i[4]):
                self.list_ctrl.SetStringItem(index, 4 + idx, ii)
            index += 1

        # Se elimina la ventana
        del wait


if __name__ == "__main__":
    from py.una.pol.tava.dao.dmetric import getResultMetricById
    result_metric = getResultMetricById(1)
    app = wx.App()
    fr = wx.Frame(None, title='Configuration')
    panel = PanelEnsembleConfig(fr, result_metric)
    fr.SetSize((1000,500))
    fr.Centre(wx.BOTH)
    # fr.Fit()
    fr.Show()
    app.MainLoop()
