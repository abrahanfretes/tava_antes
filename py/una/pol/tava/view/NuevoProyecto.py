# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''

import wx


class NuevoProyecto(wx.Dialog):

    def __init__(self, parent):
        super(NuevoProyecto, self).__init__(parent, title="Nuevo Proyecto",
            size=(621, 220))

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
        textDescripcion = wx.StaticText(panel, label=labelAddNewProject)
        sizer.Add(textDescripcion, pos=(1, 0), flag=wx.TOP | wx.LEFT |
                  wx.BOTTOM, border=15)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(2, 0), span=(1, 5),
            flag=wx.EXPAND | wx.BOTTOM, border=10)

        text2 = wx.StaticText(panel, label="Nombre de Proyecto")
        sizer.Add(text2, pos=(3, 0), flag=wx.LEFT, border=10)

        self.textNameProject = wx.TextCtrl(panel)
        self.textNameProject.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.textNameProject.SetFocus()
        sizer.Add(self.textNameProject, pos=(3, 1), span=(1, 3), flag=wx.TOP |
                  wx.EXPAND)

        button3 = wx.Button(panel, label='Help')
        sizer.Add(button3, pos=(5, 0), flag=wx.LEFT, border=10)

        self.botonOK = wx.Button(panel, label="Ok")
        self.botonOK.Bind(wx.EVT_BUTTON, self.AddProject)
        sizer.Add(self.botonOK, pos=(5, 3))

        botonCancelar = wx.Button(panel, label="Cancelar")
        botonCancelar.Bind(wx.EVT_BUTTON, self.OnClose)
        sizer.Add(botonCancelar, pos=(5, 4), span=(1, 1),
            flag=wx.BOTTOM | wx.RIGHT, border=5)

        sizer.AddGrowableCol(2)

        panel.SetSizer(sizer)

    def AddProject(self, e):
        self.createProject()

    def OnKeyDown(self, e):
        key = e.GetKeyCode()
        if key == wx.WXK_RETURN:
            self.createProject()
        e.Skip()

    def createProject(self):
        self.arbolProyecto = self.Parent.cuerpoPrincipal.arbolProyecto

        #--> aqui se van a crear los directorios
        nameProject = self.textNameProject.Value

        #--> [] = del nuevo proyecto
        listProject = [nameProject]
        self.arbolProyecto.AddTreeNodes(self.arbolProyecto.root, [nameProject])
        self.Close(True)

    def OnClose(self, e):
        self.Close(True)


if __name__ == '__main__':

    app = wx.App()
    NuevoProyecto(None)
    app.MainLoop()
