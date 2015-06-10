'''
Created on 7/6/2015

@author: abrahan
'''


class FigureMetricPresenter:
    def __init__(self, iview, test):
        self.iview = iview
        self.test = test
        self.figure_axes = None
        self.title_g = ''
        self.ite_list = []

    def initFigure(self, problem, objective, evolutionary, thread, parallel,
                   metric, population, iteration):

        axe = self.iview.figure.gca()
        xx = []
        yy = []

        for pop in metric.populations:
            x = []
            y = []
            for ite in pop.value_metrics:
                x.append(ite.iteration)
                y.append(ite.value)

            xx.append(x)
            yy.append(y)
            axe.plot(x, y)

        axe.plot(xx, yy)
        self.iview.canvas.draw()

        return axe
