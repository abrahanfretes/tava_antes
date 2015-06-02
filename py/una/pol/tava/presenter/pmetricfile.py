# -*- coding: utf-8 -*-
'''
Created on 14/5/2015

@author: abrahan
'''

from wx.lib.pubsub import Publisher as pub
from py.una.pol.tava.model.mresult import ResultModel as rm
from py.una.pol.tava.base.tavac import nid_error, nip_error, correct
import topic as T
import py.una.pol.tava.view.vimages as I
from py.una.pol.tava.model.mmetric import MetricModel as mm


class AddMetricFileDialogPresenter():
    def __init__(self, iview, project):
        self.iview = iview
        self.project = project
        self.countItem = 0

    # Validacion de nombre de archivo
    def updateGridFile(self, names, paths):
        # validacion
        index = 0
        for filename in names:
            # verificar nombre en existentes en BD
            if filename in self.getExistingNames():
                # agregar y marcar como error
                icon, label_error = self.getIconAndLabelFileError(nip_error)
                pass
            elif self.isNameTemp(filename):
                # agregar y marcar como error
                icon, label_error = self.getIconAndLabelFileError(nid_error)
                pass
            elif not self.isValidFormat(paths[index]):
                # agregar y marcar como error
                icon, label_error = self.getIconAndLabelFileError(self.eformat)
                pass
            else:
                # agregar y marcar como correcto
                icon, label_error = self.getIconAndLabelFileCorrect(correct)
                pass

            row = [icon, filename, paths[index], label_error]
            self.iview.dvlc.AppendItem(row)
            index += 1
            self.countItem += 1

        # actualizacion de los botones

        # boton ok
        if self.isEmptyGrip():
            self.iview.setInitValues()
        elif self.isValidAllFiles():
            self.iview.o_button.Enable()
            self.iview.UpDateHiderLabel(0)
        else:
            self.iview.o_button.Disable()
            self.iview.UpDateHiderLabel(1)
        # self.addListPath(paths)
        # self.setStateComponetsFile()

    # Funcion de verificacion de stylos
    def checkStyle(self):
        paths = self.getPaths()
        self.deletedAllFile()
        self.updateGridFile(paths)

    def getPaths(self):
        paths = []
        for row in range(self.countItem):
            paths.append(self.iview.dvlc.GetTextValue(row, 2))
        return paths

    def isAnyRowSelected(self):
        for row in range(self.countItem):
            if self.iview.dvlc.IsRowSelected(row):
                return True
        return False

    # Funciones de eliminacion de filas
    def deletedOneFile(self):
        row = self.iview.dvlc.GetSelectedRow()
        self.iview.dvlc.DeleteItem(row)
        self.countItem -= 1
        self.updateGridFile([], [])

    def deletedAllFile(self):
        self.iview.dvlc.DeleteAllItems()
        self.countItem = 0
        self.disableStyles()

    # Funciones de Validaciones de archivo
    def isNameTemp(self, name):
        for row in range(self.countItem):
            if self.iview.dvlc.GetTextValue(row, 1) == name:
                return True
        return False

    def isValidFormat(self, path):
        style = self.iview.rb.GetSelection()
        self.eformat = mm().quickCheckStyle(path, style)
        if self.eformat == correct:
            return True
        else:
            return False

    def isValidAllFiles(self):
        not_error = self.iview.getLabelError(correct)
        for row in range(self.countItem):
            if self.iview.dvlc.GetTextValue(row, 3) != not_error:
                return False
        return True

    def getIconAndLabelFileError(self, key_error):
        return I.errornewproject_png, self.iview.getLabelError(key_error)

    def getIconAndLabelFileCorrect(self, key_correct):
        return I.ok_png, self.iview.getLabelError(key_correct)

    def isEmptyGrip(self):
        if self.countItem == 0:
            return True
        return False

    def Close(self):
        self.iview.Close(True)

    def enableStyles(self):
        for i in range(self.iview.rb.GetCount()):
            self.iview.rb.EnableItem(i, True)

    def disableStyles(self):
        for i in range(self.iview.rb.GetCount()):
            self.iview.rb.EnableItem(i, False)

    # ------ funciones que interactuan con el modelo --------------------------

    def getExistingNames(self):
        return mm().getFilesNames(self.project)

    def CorrectStyleFormat(self, path_file):
        style = self.iview.rb.GetSelection()
        return rm().fastVerificationStyle(path_file, style)

    def AddFile(self):
        paths = []
        style = self.iview.rb.GetSelection()
        for row in range(self.countItem):
            paths.append(self.iview.dvlc.GetTextValue(row, 2))

        self.project = mm().add(paths, self.project, style)

        pub.sendMessage(T.PROJECT_UPDATE, self.project)
        self.Close()
