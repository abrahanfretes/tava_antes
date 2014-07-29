# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''

import wx
from py.una.pol.tava.presenter.pproject import NewProjectDialogPresenter
#from py.una.pol.tava.model.mproject import ProjectModel as pro


class NewProjectDialog(wx.Dialog):

    def __init__(self, parent):
        super(NewProjectDialog, self).__init__(parent,
            title="Nuevo Proyecto", size=(621, 220))

        self.presenter = NewProjectDialogPresenter(self)
        #self.parent = parent

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        container_panel = wx.Panel(self)
        container_sizer = wx.GridBagSizer(5, 5)

        new_project_label = "Crear un nuevo Proyecto"
        new_project_text = wx.StaticText(container_panel,
                                          label=new_project_label)
        new_project_text_font = new_project_text.GetFont()
        new_project_text_font.SetWeight(wx.BOLD)
        new_project_text.SetFont(new_project_text_font)
        container_sizer.Add(new_project_text, pos=(0, 0), flag=wx.TOP |
                            wx.LEFT, border=15)

        execute_bmp = wx.StaticBitmap(container_panel,
                               bitmap=wx.Bitmap('icons/exec.png'))
        container_sizer.Add(execute_bmp, pos=(0, 4), flag=wx.RIGHT |
                            wx.ALIGN_RIGHT, border=5)

        add_new_project_label = "Introduzca un nombre de proyecto."
        self.description_text = wx.StaticText(container_panel,
                                             label=add_new_project_label)
        container_sizer.Add(self.description_text, pos=(1, 0), flag=wx.TOP |
                            wx.LEFT | wx.BOTTOM, border=15)

        line = wx.StaticLine(container_panel)
        container_sizer.Add(line, pos=(2, 0), span=(1, 5),
            flag=wx.EXPAND | wx.BOTTOM, border=10)

        name_project_text = wx.StaticText(container_panel,
                                          label="Nombre de Proyecto")
        container_sizer.Add(name_project_text, pos=(3, 0), flag=wx.LEFT,
                            border=10)

        self.name_project_textctrl = wx.TextCtrl(container_panel)
        self.name_project_textctrl.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.name_project_textctrl.SetFocus()
        container_sizer.Add(self.name_project_textctrl, pos=(3, 1),
                            span=(1, 3), flag=wx.TOP | wx.EXPAND)

        help_button = wx.Button(container_panel, label='Help')
        container_sizer.Add(help_button, pos=(5, 0), flag=wx.LEFT, border=10)

        self.ok_button = wx.Button(container_panel, label="Ok")
        self.ok_button.Bind(wx.EVT_BUTTON, self.OnNew)
        self.ok_button.Disable()
        container_sizer.Add(self.ok_button, pos=(5, 3))

        cancel_button = wx.Button(container_panel, label="Cancelar")
        cancel_button.Bind(wx.EVT_BUTTON, self.OnCancel)
        container_sizer.Add(cancel_button, pos=(5, 4), span=(1, 1),
            flag=wx.BOTTOM | wx.RIGHT, border=5)

        container_sizer.AddGrowableCol(2)
        container_panel.SetSizer(container_sizer)

    def OnNew(self, e):
        self.OnCreate(self.name_project_textctrl.Value)

    def OnKeyUp(self, e):

        if self.presenter.IsNameValido(self.name_project_textctrl.Value):
            self.ok_button.Enable(True)
            self.ConfigEnableLabel()

            if wx.WXK_RETURN == e.GetKeyCode():
                self.OnCreate(self.name_project_textctrl.Value)
        else:
            self.ok_button.Disable()
            self.ConfigDisableLabel()

    def ConfigEnableLabel(self):
        self.description_text.SetLabel("Introduzca un nombre de proyecto.")
        self.description_text.SetForegroundColour((0, 0, 0))
        self.name_project_textctrl.SetBackgroundColour((255, 255, 255))

    def ConfigDisableLabel(self):
        self.description_text.SetLabel("Ya existe el Proyecto")
        self.description_text.SetForegroundColour((255, 0, 0))
        self.name_project_textctrl.SetBackgroundColour("Pink")

    def OnCreate(self, nameProject):
        self.presenter.OnNew(nameProject)
        #project = self.presenter.OnNew(nameProject)
        #self.parent.main_panel.project_tree_notebook.project_tree_panel.\
        #project_tree.AddProjectNode(project)
        self.OnClose()

    def OnCancel(self, e):
        self.Close(True)

    def OnClose(self):
        self.Close(True)


#==============================================================================
# class NewProjectDialogPresenter:
#     def __init__(self):
# 
#         self.listNamesProject = self.GetNamesProject()
# 
#     def GetNamesProject(self):
#         return pro().getNamesProject()
# 
#     def OnNew(self, name):
#         return pro().add(name)
# 
#     def IsNameValido(self, name):
#         return name not in self.listNamesProject and bool(name)
#==============================================================================
