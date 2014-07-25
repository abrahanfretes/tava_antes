'''
Created on 23/07/2014

@author: afretes
'''


import wx
from py.una.pol.tava.presenter.proPresenter import ProyectoPresenter as pro


class NewProjectDialog(wx.Dialog):

    def __init__(self, parent):
        super(NewProjectDialog, self).__init__(parent,
            title="Nuevo Proyecto", size=(621, 220))

        self.pro = Project()
        self.parent = parent

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(5, 5)

        labelNewProject = "Crear un nuevo Proyecto"
        textNuevoProyecto = wx.StaticText(panel, label=labelNewProject)
        sum_font = textNuevoProyecto.GetFont()
        sum_font.SetWeight(wx.BOLD)
        textNuevoProyecto.SetFont(sum_font)
        sizer.Add(textNuevoProyecto, pos=(0, 0), flag=wx.TOP | wx.LEFT,
            border=15)

        icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('icons/exec.png'))
        sizer.Add(icon, pos=(0, 4), flag=wx.RIGHT | wx.ALIGN_RIGHT,
            border=5)

        labelAddNewProject = "Introduzca un nombre de proyecto."
        self.textDescripcion = wx.StaticText(panel, label=labelAddNewProject)
        sizer.Add(self.textDescripcion, pos=(1, 0), flag=wx.TOP | wx.LEFT |
                  wx.BOTTOM, border=15)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(2, 0), span=(1, 5),
            flag=wx.EXPAND | wx.BOTTOM, border=10)

        text2 = wx.StaticText(panel, label="Nombre de Proyecto")
        sizer.Add(text2, pos=(3, 0), flag=wx.LEFT, border=10)

        self.namePro = wx.TextCtrl(panel)
        self.namePro.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.namePro.SetFocus()
        sizer.Add(self.namePro, pos=(3, 1), span=(1, 3), flag=wx.TOP |
                  wx.EXPAND)

        button3 = wx.Button(panel, label='Help')
        sizer.Add(button3, pos=(5, 0), flag=wx.LEFT, border=10)

        self.botonOK = wx.Button(panel, label="Ok")
        self.botonOK.Bind(wx.EVT_BUTTON, self.OnNew)
        self.botonOK.Disable()
        sizer.Add(self.botonOK, pos=(5, 3))

        botonCancelar = wx.Button(panel, label="Cancelar")
        botonCancelar.Bind(wx.EVT_BUTTON, self.OnCancel)
        sizer.Add(botonCancelar, pos=(5, 4), span=(1, 1),
            flag=wx.BOTTOM | wx.RIGHT, border=5)

        sizer.AddGrowableCol(2)
        panel.SetSizer(sizer)

    def OnNew(self, e):
        self.OnCreate(self.namePro.Value)

    def OnKeyUp(self, e):

        if self.pro.IsNameValido(self.namePro.Value):
            self.botonOK.Enable(True)
            self.ConfigEnableLabel()

            if wx.WXK_RETURN == e.GetKeyCode():
                self.OnCreate(self.namePro.Value)
        else:
            self.botonOK.Disable()
            self.ConfigDisableLabel()

    def ConfigEnableLabel(self):
        self.textDescripcion.SetLabel("Introduzca un nombre de proyecto.")
        self.textDescripcion.SetForegroundColour((0, 0, 0))
        self.namePro.SetBackgroundColour("Blank")

    def ConfigDisableLabel(self):
        self.textDescripcion.SetLabel("Ya existe el Proyecto")
        self.textDescripcion.SetForegroundColour((255, 0, 0))
        self.namePro.SetBackgroundColour("Pink")

    def OnCreate(self, nameProject):
        pro = self.pro.OnNew(nameProject)
        self.parent.cuerpoPrincipal.notebook1.panelTreeProjects.\
        arbolProyecto.AddProjectNode(pro)
        self.OnClose()

    def OnCancel(self, e):
        self.Close(True)

    def OnClose(self):
        self.Close(True)


class Project:
    def __init__(self):

        self.listNamesProject = self.GetNamesProject()
        print self.listNamesProject

    def GetNamesProject(self):
        return pro().getNamesProject()

    def OnNew(self, name):
        return pro().add(name)

    def IsNameValido(self, name):
        return name not in self.listNamesProject and bool(name)
