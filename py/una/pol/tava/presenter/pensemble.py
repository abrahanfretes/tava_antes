'''
Created on 18/08/2015

@author: arsenioferreira
'''
from py.una.pol.tava.view import agreggation as ag
import py.una.pol.tava.dao.dmetric as dm
import random


class PanelEnsemblePresenter:
    '''
    Clase presenter del panel de configuraciones para el metodo ensemble
    '''
    def __init__(self, iview):
        self.iview = iview

    def prepare_listctrl_by_moea(self, list_results):
        '''
        Metodo que configura la grilla para la opcion "por cada moea"
        :param list_results:
        '''

        # Se selecciona la maxima longitud de la cuarta fila,
        # para la columna 4, ya que contiene el listado de ganadores
        max_len = max([len(i[4]) for i in list_results])
        self.iview.list_ctrl.InsertColumn(0, 'Problem')
        self.iview.list_ctrl.InsertColumn(1, 'Number of Objectives', width=145)
        self.iview.list_ctrl.InsertColumn(2, 'MOEA')
        self.iview.list_ctrl.InsertColumn(3, 'Number of Threads', width=130)
        for i in range(max_len):
            self.iview.list_ctrl.InsertColumn(4 + i, 'Winner ' + str(i + 1))

        index = 0
        for i in list_results:
            self.iview.list_ctrl.InsertStringItem(index, i[0])
            self.iview.list_ctrl.SetStringItem(index, 1, str(i[1]))
            self.iview.list_ctrl.SetStringItem(index, 2, i[2])
            self.iview.list_ctrl.SetStringItem(index, 3, str(i[3]))
            for idx, ii in enumerate(i[4]):
                self.iview.list_ctrl.SetStringItem(index, 4 + idx, ii)

            index += 1

    def prepare_listctrl_by_parallel_method(self, list_results):
        '''
        Metodo que configura la grilla para la opcion "por cada moea"
        :param list_results:
        '''
        # Se selecciona la maxima longitud de la cuarta fila,
        # para la columna 3, ya que contiene el listado de ganadores
        max_len = max([len(i[3]) for i in list_results])
        self.iview.list_ctrl.InsertColumn(0, 'Problem')
        self.iview.list_ctrl.InsertColumn(1, 'Number of Objectives', width=155)
        self.iview.list_ctrl.InsertColumn(2, 'Parallel Method', width=125)
        for i in range(max_len):
            self.iview.list_ctrl.InsertColumn(3 + i, 'Winner ' + str(i + 1))

        index = 0
        for i in list_results:
            self.iview.list_ctrl.InsertStringItem(index, i[0])
            self.iview.list_ctrl.SetStringItem(index, 1, str(i[1]))
            self.iview.list_ctrl.SetStringItem(index, 2, i[2])
            for idx, ii in enumerate(i[3]):
                self.iview.list_ctrl.SetStringItem(index, 3 + idx, ii)

            index += 1


class ApproximationFront():
    '''
    Clase que representa a un frente pareto aproximado a ser utilizado en el
    torneo de doble eliminacion.
    '''
    def __init__(self):
        pass

    def setNumberObjectiveId(self, number_objective_id):
        self.number_objective_id = number_objective_id

    def setMoeaName(self, moea_name):
        self.moea_name = moea_name

    def setNumberThread(self, number_thread):
        self.number_thread = number_thread

    def setParallelMethodId(self, parallel_method_id):
        self.parallel_method_id = parallel_method_id

    def setParallelMethodName(self, parallel_method_name):
        self.parallel_method_name = parallel_method_name

    def setValuePopulation(self, value_population):
        self.value_population = value_population

    def setIteration(self, iteration):
        self.iteration = iteration


class EnsembleMethod:
    '''
    Clase que maneja la logica del ensemble method, para las opciones de
    "por cada metodo evolutivo" y "por cada metodo paralelo"
    '''
    def __init__(self):
        self.by_moea = True
        self.dict_metric = None
        self.result_metric = None

    def get_by_moea(self):
        return self.by_moea

    def set_by_moea(self, value):
        self.by_moea = value

    def get_dict_metric(self):
        return self.dict_metric

    def set_dict_metric(self, value):
        self.dict_metric = value

    def get_result_metric(self):
        return self.result_metric

    def set_result_metric(self, value):
        self.result_metric = value

    def execute_ensemble_method(self):
        '''
        Metodo que inicia el proceso ensemble method, recorriendo los difentes
        espacios de busquedos entre los metodos seleccionados.
        '''

        list_results = []

        if self.by_moea:
            for moea_problem in self.result_metric.moea_problems:
                for number_objective in moea_problem.number_objectives:
                    for moea in number_objective.evolutionary_methods:
                        for number_thread in moea.number_threads:
                            result = self.generate_aproximation_front_by_moea(
                                                                number_thread)
                            list_results.append((moea_problem.name,
                                                 number_objective.value,
                                                 moea.name,
                                                 number_thread.value,
                                                 result))
        else:
            for moea_problem in self.result_metric.moea_problems:
                for number_objective in moea_problem.number_objectives:
                    pm_list = dm.getDistinctParallelMethodsByNumberObjective(
                                                        number_objective.id)
                    for parallel_method, in pm_list:
                            result = self.\
                            generate_aproximation_front_by_parallel_method(
                                                number_objective,
                                                parallel_method)
                            list_results.append((moea_problem.name,
                                                 number_objective.value,
                                                 parallel_method,
                                                 result))
        return list_results

    def generate_aproximation_front_by_moea(self, number_thread):
        '''
        Metodo que selecciona los frentes aproximados ganadores empleando
        diferentes semillas y escogiendo metricas de evaluacion aleatoria para
        cada seleccion.
        :param number_thread: entidad utilizada para acotar el espacio de
        busqueda.
        '''
        if len(number_thread.parallelization_methods) == 1:
            return [number_thread.parallelization_methods[0].name]

        max_value_population, = dm.getMaxValuePopulation(
                            number_thread.parallelization_methods[0].
                            metrics[0].id)
        values_population = range(max_value_population + 1)

        approximation_fronts = []
        selected_parallel_methods = []

        # Step 1 Generate 50 approximation front
        for value_population in values_population:
            # Obtenemos una metrica aleatoria
            metric_name, condition = self.get_random_item(
                                                    self.dict_metric.items())

            value_metric = None
            if condition == ag.MAX:
                value_metric = dm.getMaxValueMetric(number_thread.id,
                                                 value_population,
                                                 metric_name)
            else:
                value_metric = dm.getMinValueMetric(number_thread.id,
                                                 value_population,
                                                 metric_name)
    #         Metodo paralelo escogido
            parallel_method = value_metric.population.metric.\
                              parallelization_method
    #         Representacion del Frente Aproximado
            approximation_front = ApproximationFront()
            approximation_front.setParallelMethodId(parallel_method.id)
            approximation_front.setValuePopulation(value_population)
            approximation_front.setIteration(value_metric.iteration)

    #         Adjuntamos al listado de frentes aproximados ganadores
            approximation_fronts.append((parallel_method.name,
                                         approximation_front))
            if parallel_method.name not in selected_parallel_methods:
                selected_parallel_methods.append(parallel_method.name)

        return self.run_double_tournament_selection(approximation_fronts,
                                           selected_parallel_methods)

    def generate_aproximation_front_by_parallel_method(self, number_objective,
                                              parallel_method_name):
        '''
        Metodo que selecciona los frentes aproximados ganadores empleando
        diferentes semillas y escogiendo metricas de evaluacion aleatoria para
        cada seleccion.
        :param number_objective: entidad empleada para acotar el espacio de
        busqueda.
        :param parallel_method_name: nombre del metodo paralelo actualmente
        evaluado.
        '''

        max_value_population, = dm.getMaxValuePopulation(
                            number_objective.\
                            evolutionary_methods[0].\
                            number_threads[0].
                            parallelization_methods[0].\
                            metrics[0].id)
        values_population = range(max_value_population + 1)

        approximation_fronts = []
        selected_evolutionary_methods = []

        # Step 1 Generate 50 approximation front
        for value_population in values_population:
            # Obtenemos una metrica aleatoria
            metric_name, condition = self.get_random_item(
                                                    self.dict_metric.items())

            if condition == ag.MAX:
                value_metric = dm.getMaxValueMetricByParallelMethod(
                                                 number_objective.id,
                                                 parallel_method_name,
                                                 metric_name,
                                                 value_population)
            else:
                value_metric = dm.getMinValueMetricByParallelMethod(
                                                number_objective.id,
                                                parallel_method_name,
                                                metric_name,
                                                value_population)
    #         numero de hilo del moea escogido como ganador
            number_thread = value_metric.\
                                population.\
                                metric.\
                                parallelization_method.\
                                number_threads
    #         moea ganador escogido
            evolutionary_method = number_thread.evolutionary_method

    #         Representacion del Frente Aproximado
            approximation_front = ApproximationFront()
            approximation_front.setNumberObjectiveId(number_objective.id)
            approximation_front.setMoeaName(evolutionary_method.name)
            approximation_front.setNumberThread(number_thread.value)
            approximation_front.setParallelMethodName(parallel_method_name)
            approximation_front.setValuePopulation(value_population)
            approximation_front.setIteration(value_metric.iteration)

            approximation_fronts.append((evolutionary_method.name,
                                         approximation_front))
            if evolutionary_method.name not in selected_evolutionary_methods:
                selected_evolutionary_methods.append(evolutionary_method.name)

        return self.run_double_tournament_selection(approximation_fronts,
                                           selected_evolutionary_methods)

    def run_double_tournament_selection(self, approximation_fronts,
                                    selected_methods):
        '''
        Clase que evalua el torneo de doble eliminacion para cada frente
        aproximado ganador retornando el ranking de metodos ganadores.
        :param approximation_fronts: frentes ganadores seleccionados por cada
        semilla diferente.
        :param selected_methods: listado de metodos seleccionados.
        '''
        # Step 2: Use Double-Tournament Selection to get the best one front:
        fronts = list(approximation_fronts)

        ranking_methods = []

        while len(selected_methods) > 1:
            round_fronts = list(fronts)

            winners = []
            winners_w = []
            winners_l = []
            winners_l_w = []

            losers = []
            losers_w = []
            losers_l = []
            losers_l_w = []

            self.evaluate_winners_and_losers(round_fronts, winners, losers)

            # Ganador del torneo para una ronda
            ind_winner = None
            while True:
                if len(winners) == 1:
                    metric_name, condition = self.get_random_item(
                                                    self.dict_metric.items())
                    value1 = self.get_value_front_by_metric(winners[0][1],
                                                        metric_name)
                    value2 = self.get_value_front_by_metric(losers[0][1],
                                                        metric_name)
                    w_ = self.evaluate_fronts(winners[0], value1, losers[0],
                                             value2, condition)[0]
                    if w_ in winners:
                        ind_winner = w_
                    else:
                        metric_name, condition = self.get_random_item(
                                                    self.dict_metric.items())
                        value1 = self.get_value_front_by_metric(winners[0][1],
                                                            metric_name)
                        value2 = self.get_value_front_by_metric(losers[0][1],
                                                            metric_name)
                        w_ = self.evaluate_fronts(winners[0], value1,
                                            losers[0], value2, condition)[0]
                        ind_winner = w_
                    break

                self.evaluate_winners_and_losers(winners, winners_w, winners_l)

                self.evaluate_winners_and_losers(losers, losers_w, losers_l)

                self.evaluate_winners_and_losers_one_by_one(winners_l,
                                            losers_w, winners_l_w, losers_l_w)

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
            item = self.delete_individuals_from_winner_method(ind_winner,
                                                              fronts)

            # removemos de los metodos seleccionados
            selected_methods.remove(item)

            # agregamos al ranking de metodos
            name = ind_winner[0]
            ranking_methods.append(name)

        name = fronts[0][0]
        ranking_methods.append(name)

        return ranking_methods

    def evaluate_winners_and_losers(self, fronts_, winners_, losers_):
        while len(fronts_) > 0:
            winner_, loser_ = self.get_winner_and_loser_fronts(fronts_)
            winners_.append(winner_)
            losers_.append(loser_)

    def get_winner_and_loser_fronts(self, fronts_):
        if len(fronts_) == 1:
            front = fronts_[0]
            self.delete_item_from_list(front, fronts_)
            return front, front
        front_1 = self.get_random_item(fronts_)
        self.delete_item_from_list(front_1, fronts_)
        front_2 = self.get_random_item(fronts_)
        self.delete_item_from_list(front_2, fronts_)
        metric_name, condition = self.get_random_item(self.dict_metric.items())
        value1 = self.get_value_front_by_metric(front_1[1], metric_name)
        value2 = self.get_value_front_by_metric(front_2[1], metric_name)
        return self.evaluate_fronts(front_1, value1, front_2, value2,
                                    condition)

    def evaluate_winners_and_losers_one_by_one(self, winners_l, losers_w,
                                         winners_l_w, losers_l_w):
        for front_1, front_2 in zip(winners_l, losers_w):
            metric_name, condition = self.get_random_item(
                                                    self.dict_metric.items())
            value1 = self.get_value_front_by_metric(front_1[1], metric_name)
            value2 = self.get_value_front_by_metric(front_2[1], metric_name)
            winner_, loser_ = self.evaluate_fronts(front_1, value1, front_2,
                                                   value2, condition)
            winners_l_w.append(winner_)
            losers_l_w.append(loser_)

    def evaluate_fronts(self, front_1, value1, front_2, value2, condition):
        if condition == ag.MAX:
            item = max(value1, value2)
        else:
            item = min(value1, value2)
        if item == value1:
            return front_1, front_2
        else:
            return front_2, front_1

    def get_value_front_by_metric(self, front, metric_name):
        if self.by_moea:
            value_metric = dm.getValueMetricByMoea(front.parallel_method_id,
                            metric_name, front.value_population,
                            front.iteration)
        else:
            value_metric = dm.getValueMetricByParallelMethod(
                                                front.number_objective_id,
                                                front.moea_name,
                                                front.number_thread,
                                                front.parallel_method_name,
                                                metric_name,
                                                front.value_population,
                                                front.iteration)
        return value_metric.value

    def delete_losers(self, fronts_, losers_l_w_, losers_l_):
        for ind in losers_l_w_:
            if ind in fronts_:
                fronts_.remove(ind)

        for ind in losers_l_:
            if ind in fronts_:
                fronts_.remove(ind)

    def delete_individuals_from_winner_method(self, ind_winner_, fronts_):
        item = ind_winner_[0]
        to_delete = []
        for ind in fronts_:
            if ind[0] == item:
                to_delete.append(ind)
        for ind in to_delete:
            fronts_.remove(ind)
        return item

    def get_random_item(self, list_):
        random.shuffle(list_)
        return random.choice(list_)

    def delete_item_from_list(self, item, list_):
        list_.pop(list_.index(item))
