'''
Created on 21/09/2014

@author: arsenioferreira
'''
from py.una.pol.tava.model.mresult import ResultModel as rm
from py.una.pol.tava.model.miteration import InterationModel as im
from py.una.pol.tava.base.entity import TestData, TestDetail, TestConfig,\
TestGraphic, SomConfig
from py.una.pol.tava.model.mtestconfig import TestConfigModel as tm
from wx.lib.pubsub import Publisher as pub
import topic as T
import time
import wx


class GraphicWizardPresenter():
    def __init__(self, iview):
        self.iview = iview

    def GetListResultIterations(self, project, filesSelecteds):
        listResults = []
        for file_name in filesSelecteds:
            result = rm().getResultByProjectIdAndFileName(project.id,
                                                          file_name)
            listIters = im().getIterationsByResult(result)

            for itr in listIters:
                listResults.append((itr, result))

        b = {}
        for i in range(0, len(listResults)):
            b[i] = listResults[i]

        return b

    def GetListItems(self):
        return rm().getNamesResultForProject(self.iview.project)

    def CreateTest(self, name_test, data, selection, project):

        # Agregar TestConfig a la Base de Datos
        test = TestConfig()
        test.name = name_test
        test.project_id = project.id
        test.creation_date = time.strftime("%d/%m/%y")

        #test = tm().add(test)

        #obtener las iteraciones de cada archivo
        for rf in data:
            test_detail = TestDetail()
            test_detail.result_id = rf.result.id

            iterations = self.GetIterationsSelected(rf)
            for i in iterations:
                test_data = TestData()
                test_data.iteration_id = i.id

                test_detail.test_datas.append(test_data)

            test.test_details.append(test_detail)

        # verificamos la seleccion escogida de grafico
        test_graphic = TestGraphic()
        if selection == 0:
            test_graphic.name_graphic = "parallel"
        if selection == 1:
            from py.una.pol.tava.model.msom import SomModel as sm
            somConfigPanel = self.iview.graphicList.somConfigPanel
            test_graphic.name_graphic = "som"
            som = SomConfig()
            som.learning_rate = somConfigPanel.learning_rate.GetValue()
            som.sigma = somConfigPanel.sigma.GetValue()
            if somConfigPanel.hex_topology.GetValue():
                som.topology = "hexagonal"
            else:
                som.topology = "square"
            som.columns = somConfigPanel.columns.GetValue()
            som.rows = somConfigPanel.rows.GetValue()
            if somConfigPanel.lin_map_initialization.GetValue():
                som.map_initialization = "linear"
            else:
                som.map_initialization = "random"
            if somConfigPanel.gauss_neighborhood.GetValue():
                som.neighborhood = "gaussian"
            else:
                som.neighborhood = "bubble"
            som.iterations = somConfigPanel.iterations.GetValue()
            sm().add(som)
            test_graphic.id_graphic = som.id

        test.test_graphic.append(test_graphic)

        test = tm().add(test)
        
       #test = tm().upDate(test)

        pub.sendMessage(T.PROJECT_UPDATE, project)
        pub.sendMessage(T.TESTCONFIG_ADD_PAGE, (test, selection))

    def GetIterationsSelected(self, rf):
        iterations = []
        for itr in rf.iterations:
            if itr.check:
                iterations.append(itr.iteration)
        return iterations

    def keyboardEvents(self, key_code):
        valid = 0
        #verifica si el nombre es correcto
        key_name = self.keyValidName()
        if key_name != valid:
            self.DisableNextButton()
            return

        self.EnableNextButton()

    def keyValidName(self):
        name = self.iview.page1.panel1.name_value_text.Value

        if len(name.strip(' ')) == 0:
            return 1
        if '/' in name:
            return 2
        if name[0] == '.':
            return 3
        if len(name.strip(' ')) > 100:
            return 4
        return 0

    def DisableNextButton(self):
        forward_btn = self.iview.FindWindowById(wx.ID_FORWARD)
        forward_btn.Disable()

    def EnableNextButton(self):
        forward_btn = self.iview.FindWindowById(wx.ID_FORWARD)
        forward_btn.Enable(True)
