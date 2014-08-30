# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''

import wx
import sys
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
from wx import GetTranslation as _
from py.una.pol.tava.presenter.pproject import NewProjectDialogPresenter
from py.una.pol.tava.presenter.pproject import RenameProjectDialogPresenter
from py.una.pol.tava.presenter.pproject import DeleteProjectDialogPresenter
from py.una.pol.tava.presenter.pproject import UnHideProjectDialogPresenter
from py.una.pol.tava.presenter.pproject import CheckListCtrlPresenter
from py.una.pol.tava.presenter.pproject import AddFileDialogPresenter
import py.una.pol.tava.view.vi18n as C
import py.una.pol.tava.view.vimages as I


class NewProjectDialog(wx.Dialog):
    '''
    Clase Dialog que define la ventana de creación de un nuevo proyecto.
    '''

    def __init__(self, parent):
        super(NewProjectDialog, self).__init__(parent, size=(600, 250))

        # Definicion del presenter de la clase
        self.presenter = NewProjectDialogPresenter(self)

        # Inicializacion de los componentes de la clase
        self.InitUI()

        self.Centre()
        self.ShowModal()

    def InitUI(self):
        '''
        Metodo de inicializacion de componentes de la clase
        '''

        # Definicion del panel contenedor principal
        panel = wx.Panel(self)

        # Definicion del sizer principal de la clase
        sizer = wx.GridBagSizer(5, 5)

        # Titulo de Proyecto Tava
        # Fuente para el titulo
        font_title = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font_title.SetWeight(wx.BOLD)
        font_title.SetPointSize(14)

        # Definicion del componente texto para el titulo
        title_text = wx.StaticText(panel, label=_(C.NPD_TP))
        title_text.SetFont(font_title)

        # Asociamos el titulo al sizer de la clase
        sizer.Add(title_text, pos=(0, 0), flag=wx.TOP | wx.LEFT, border=15)

        # Icono de ejecucion
        exec_bmp = wx.StaticBitmap(panel, bitmap=I.exec_png)

        # Asociamos el icono de ejecucion al sizer
        sizer.Add(exec_bmp, pos=(0, 4),
                     flag=wx.ALIGN_RIGHT | wx.RIGHT, border=15)

        # Texto Descriptivo que cambia
        # Sizer horizontal para el componente texto para las descripciones
        hbox_description = wx.BoxSizer(wx.HORIZONTAL)

        # Definicion de la fuente para el texto de descripcion
        font_description = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font_description.SetPointSize(9)

        # Definicion del componente texto para las descripciones
        self.description_text = wx.StaticText(panel)
        self.description_text.SetFont(font_description)

        # Definicion del icono de ejecucion
        self.execute_bmp = wx.StaticBitmap(panel)

        # Asociamos el icono con el sizer de las descripciones
        hbox_description.Add(self.execute_bmp, flag=wx.LEFT, border=2)

        # Asociamos el texto con el sizer de las descripciones
        hbox_description.Add(self.description_text, flag=wx.LEFT, border=2)

        # Agregamos el sizer de descripciones al sizer principal de la clase
        sizer.Add(hbox_description, pos=(1, 0), span=(1, 3), flag=wx.TOP |
                            wx.LEFT | wx.BOTTOM, border=15)

        # Componente Linea estatica
        line = wx.StaticLine(panel)

        # Asociamos la linea con el sizer principal de la clase
        sizer.Add(line, pos=(2, 0), span=(1, 5),
            flag=wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, border=15)

        # Definicion del componente texto estático para nombre de proyecto
        name_project_text = wx.StaticText(panel, label=_(C.NPD_NAP))

        # Asociamos el texto con el sizer principal de la clase
        sizer.Add(name_project_text, pos=(3, 0),
                     flag=wx.LEFT | wx.EXPAND | wx.RIGHT, border=15)

        # Definicion del TextCtrl para el nombre de proyecto
        self.name_project_textctrl = wx.TextCtrl(panel)

        # Enlazamos la gestion de los eventos lanzados por teclado al
        # componente textCtrl
        self.name_project_textctrl.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

        # Establecemos el foco para el textCtrl
        self.name_project_textctrl.SetFocus()

        # Asociamos el textCtrl con el sizer principal de la clase
        sizer.Add(self.name_project_textctrl, pos=(3, 1), span=(1, 4),
                     flag=wx.EXPAND | wx.RIGHT, border=15)

        # Definicion del Boton Ayuda
        self.help_button = wx.Button(panel, label=_(C.NPD_HELP))

        # Asociamos el boton ayuda con el sizer principal de la clase
        sizer.Add(self.help_button, pos=(5, 0), flag=wx.LEFT, border=15)

        # Definicion del Boton Cancelar
        cancel_button = wx.Button(panel, label=_(C.NPD_CAN))

        # Enlazamos el evento de boton al metodo OnCancel
        cancel_button.Bind(wx.EVT_BUTTON, self.OnCancel)

        # Asociamos el boton ayuda con el sizer principal de la clase
        sizer.Add(cancel_button, pos=(5, 3),
                     flag=wx.ALIGN_RIGHT | wx.RIGHT, border=15)

        # Definicion del Boton OK
        self.ok_button = wx.Button(panel, label=_(C.NPD_OK))

        # Enlazamos el evento de boton al metodo OnCreateProject
        self.ok_button.Bind(wx.EVT_BUTTON, self.OnCreateProject)

        # Desabilitamos el boton ok
        self.ok_button.Disable()

        # Asociamos el boton ok con el sizer principal de la clase
        sizer.Add(self.ok_button, pos=(5, 4),
                     flag=wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT, border=15)

        # Manejo de evento cuando se oprima la tecla Esc
        panel.Bind(wx.EVT_CHAR, self.OnKeyDown)

        # Configuracion del sizer principal
        sizer.AddGrowableCol(2)

        # Asociamos el sizer al panel principal
        panel.SetSizer(sizer)

        # Invocamos al metodo de configuracion inicial de label
        self.ConfigEnableLabel()

    def OnKeyUp(self, e):
        if(self.presenter.IsValidName(self.name_project_textctrl.Value)):
            if wx.WXK_RETURN == e.GetKeyCode():
                self.presenter.CreateProject(self.name_project_textctrl.Value)

    def ConfigEnableLabel(self):
        self.description_text.SetLabel(_(C.NPD_ENP))
        self.execute_bmp.SetBitmap(I.execute_png)
        self.name_project_textctrl.SetBackgroundColour((255, 255, 255))

    def ConfigEmptyNameProject(self):
        self.description_text.SetLabel(_(C.NPD_PNE))
        self.execute_bmp.SetBitmap(I.warningnewproject_png)
        self.name_project_textctrl.SetBackgroundColour('#F9EDED')

    def ConfigNameProjectWithSlash(self):
        self.description_text.SetLabel(_(C.NPD_PNSI))
        self.IconError()
        self.SetNameErrorBackground()

    def ConfigNameProjectStartWithPoint(self):
        self.description_text.SetLabel(_(C.NPD_PNPI))
        self.IconError()
        self.SetNameErrorBackground()

    def ConfigNameProjectInvalidLength(self):
        self.description_text.SetLabel(_(C.NPD_PNLI))
        self.IconError()
        self.SetNameErrorBackground()

    def ConfigExistingProject(self):
        self.description_text.SetLabel(_(C.NPD_PAE))
        self.IconError()
        self.SetNameErrorBackground()

    def ConfigExistingHideProject(self):
        self.description_text.SetLabel(_(C.NPD_HPAE))
        self.IconError()
        self.SetNameErrorBackground()

    def OnCreateProject(self, e):
        self.presenter.CreateProject(self.name_project_textctrl.Value)

    def IconError(self):
        self.execute_bmp.SetBitmap(I.errornewproject_png)

    def SetNameErrorBackground(self):
        self.name_project_textctrl.SetBackgroundColour((237, 93, 93))

    def OnCancel(self, e):
        self.Close(True)

    def OnKeyDown(self, e):
        key = e.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.Close()


class RenameProjectDialog(wx.Dialog):
    '''
    Clase Dialog que define la ventana de renombre de un proyecto.
    '''

    def __init__(self, parent, project):
        super(RenameProjectDialog, self).__init__(parent,
            title=_(C.RPD_RN), size=(550, 220))

        # Creacion de referencia al proyecto pasado como parametro
        self.project = project

        # Referencia al nombre original del nombre pasado como parametro
        self.previous_name = self.project.name

        # Definicion del presenter de la clase
        self.presenter = RenameProjectDialogPresenter(self)

        # Inicializacion de los componentes de la clase
        self.InitUI()

        self.Centre()
        self.ShowModal()

    def InitUI(self):

        # Definicion del panel contenedor principal
        panel = wx.Panel(self)

        # Definicion del sizer principal de la clase
        sizer = wx.GridBagSizer(3, 4)

        # Definicion del icono de execucion
        exec_bmp = wx.StaticBitmap(panel, bitmap=I.exec_png)

        # Insertamos el icono en el sizer principal
        sizer.Add(exec_bmp, pos=(0, 4),
                   flag=wx.ALIGN_RIGHT | wx.RIGHT, border=15)

        #Texto Descriptivo que cambia
        # Sizer horizontal para el componente texto para las descripciones
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Definicion de la fuente para el texto de descripcion
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        # Definicion del componente texto para las descripciones
        self.description_text = wx.StaticText(panel)
        self.description_text.SetFont(font)

        # Definicion del icono de ejecucion
        self.fig_alet_bmp = wx.StaticBitmap(panel)

        # Asociamos el icono con el sizer de las descripciones
        hbox.Add(self.fig_alet_bmp, flag=wx.LEFT, border=2)

        # Asociamos el texto con el sizer de las descripciones
        hbox.Add(self.description_text, flag=wx.LEFT, border=2)

        # Agregamos el sizer de descripciones al sizer principal de la clase
        sizer.Add(hbox, pos=(0, 0), span=(0, 3), flag=wx.TOP |
                            wx.LEFT | wx.BOTTOM, border=15)

        # Componente Linea estatica
        line = wx.StaticLine(panel)

        # Asociamos la linea con el sizer principal de la clase
        sizer.Add(line, pos=(1, 0), span=(1, 5),
            flag=wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, border=15)

        # Definicion del componente texto para nuevo nombre de proyecto
        new_name_project_text = wx.StaticText(panel, label=_(C.RPD_NN))

        # Asociamos el texto con el sizer principal de la clase
        sizer.Add(new_name_project_text, pos=(2, 0), flag=wx.LEFT | wx.TOP,
                   border=15)

        # Definicion del TextCtrl para el nuevo nombre de proyecto
        self.new_name_textctrl = wx.TextCtrl(panel, value=self.previous_name)

        # Enlazamos la gestion de los eventos lanzados por teclado al
        # componente textCtrl
        self.new_name_textctrl.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

        # Asociamos el textCtrl con el sizer principal de la clase
        sizer.Add(self.new_name_textctrl, pos=(2, 1), span=(1, 4),
                   flag=wx.BOTTOM | wx.TOP | wx.RIGHT | wx.EXPAND, border=15)

        # Definicion del Boton OK
        self.ok_button = wx.Button(panel, label=_(C.RPD_OK))

        # Enlazamos el evento de boton al metodo OnProjectRename
        self.ok_button.Bind(wx.EVT_BUTTON, self.OnProjectRename)

        # Asociamos el boton ok con el sizer principal de la clase
        sizer.Add(self.ok_button, pos=(3, 4),
                flag=wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT | wx.TOP, border=15)

        # Definicion del Boton Cancelar
        self.cancel_button = wx.Button(panel, label=_(C.RPD_CAN))

        # Enlazamos el evento de boton al metodo OnCancel
        self.cancel_button.Bind(wx.EVT_BUTTON, self.OnCancel)

        # Asociamos el boton ayuda con el sizer principal de la clase
        sizer.Add(self.cancel_button, pos=(3, 3),
                   flag=wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, border=15)

        # Manejo de evento cuando se oprima la tecla Esc
        panel.Bind(wx.EVT_CHAR, self.OnKeyDown)

        # Configuracion del sizer principal
        sizer.AddGrowableCol(2)

        # Asociamos el sizer al panel principal
        panel.SetSizer(sizer)

        # Invocamos al metodo de configuracion inicial de label
        self.ConfigEnableLabel()

    def OnKeyUp(self, e):
        if(self.presenter.IsValidName(self.new_name_textctrl.Value,
                                         self.previous_name)):
            if wx.WXK_RETURN == e.GetKeyCode():
                self.presenter.UpdateName(self.new_name_textctrl.Value)

    def ConfigEnableLabel(self):
        self.description_text.SetLabel(_(C.RPD_NNA))
        self.fig_alet_bmp.SetBitmap(I.renamenewproject_png)
        self.new_name_textctrl.SetBackgroundColour((255, 255, 255))

    def ConfigEmptyNameProject(self):
        self.description_text.SetLabel(_(C.NPD_PNE))
        self.fig_alet_bmp.SetBitmap(I.warningnewproject_png)
        self.new_name_textctrl.SetBackgroundColour('#F9EDED')

    def ConfigNameProjectWithSlash(self):
        self.description_text.SetLabel(_(C.NPD_PNSI))
        self.IconError()
        self.SetNameErrorBackground()

    def ConfigNameProjectStartWithPoint(self):
        self.description_text.SetLabel(_(C.NPD_PNPI))
        self.IconError()
        self.SetNameErrorBackground()

    def ConfigNameProjectInvalidLength(self):
        self.description_text.SetLabel(_(C.NPD_PNLI))
        self.IconError()
        self.SetNameErrorBackground()

    def ConfigExistingProject(self):
        self.description_text.SetLabel(_(C.NPD_PAE))
        self.IconError()
        self.SetNameErrorBackground()

    def ConfigExistingHideProject(self):
        self.description_text.SetLabel(_(C.NPD_HPAE))
        self.IconError()
        self.SetNameErrorBackground()

    def SetNameErrorBackground(self):
        self.new_name_textctrl.SetBackgroundColour((237, 93, 93))

    def IconError(self):
        self.fig_alet_bmp.SetBitmap(I.errornewproject_png)

    def OnProjectRename(self, event):
        self.presenter.UpdateName(self.new_name_textctrl.Value)

    def OnCancel(self, e):
        self.Close(True)

    def OnKeyDown(self, e):
        key = e.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.Close()


class DeleteProjectDialog():
    '''
    Clase que despliega un MessageBox ofreciendo la opcion de eliminacion
    de un proyecto.
    '''
    def __init__(self):

        # Definicion del presenter de la clase
        self.presenter = DeleteProjectDialogPresenter(self)

        # Se despliega el MessageBox de confirmacion de eliminacion de un
        # proyecto
        result = wx.MessageBox(_(C.PM_DEL_MESS), _(C.PM_DEL_PRO),
                      style=wx.CENTER | wx.ICON_WARNING | wx.YES_NO)
        if result == wx.YES:
            # Si la opcion fue SI se procede a eliminar el proyecto
            self.presenter.DeleteProject()


class PropertiesProjectDialog(wx.Dialog):
    '''
    Clase dialog que despliega las propiedades de un proyecto seleccionado.
    '''

    def __init__(self, parent, project):
        super(PropertiesProjectDialog, self).__init__(parent,
                            title=_(C.PPD_PF), size=(450, 200))

        # Creacion de referencia al proyecto pasado como parametro
        self.project = project

        # Inicializacion de los componentes de la clase
        self.InitUI()

        self.Centre()
        self.ShowModal()

    def InitUI(self):

        # Definicion del panel contenedor principal
        panel = wx.Panel(self)

        # Definicion del sizer principal de la clase
        sizer = wx.GridBagSizer(5, 5)

        # Definicion de la fuente para el texto del titulo
        font_title = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font_title.SetWeight(wx.BOLD)
        font_title.SetPointSize(14)

        # Definicion del componente texto para el titulo
        title_text = wx.StaticText(panel, label=_(C.NPD_TP))
        title_text.SetFont(font_title)

        # Agregamos el texto al sizer principal
        sizer.Add(title_text, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                  border=15)

        # Definimos el componente StaticLine superior
        top_line = wx.StaticLine(panel)

        # Agregamos la linea superior al sizer principal
        sizer.Add(top_line, pos=(1, 0), span=(1, 5),
            flag=wx.EXPAND | wx.BOTTOM, border=10)

        # Definicion del text para el label de nombre de proyecto
        name_text = wx.StaticText(panel, label=_(C.PPD_NA))

        # Agregamos el text al sizer principal
        sizer.Add(name_text, pos=(2, 0), flag=wx.LEFT, border=10)

        # Definicion del text para el valor del nombre de proyecto
        name_value_text = wx.StaticText(panel, label=self.project.name)

        # Desabilitamos el componente text
        name_value_text.Disable()

        # Agregamos el componente text al sizer principal
        sizer.Add(name_value_text, pos=(2, 1), span=(1, 4), flag=wx.RIGHT |
                  wx.EXPAND)

        # Definicion del text para el label de la fecha de creacion del project
        creation_date_text = wx.StaticText(panel, label=_(C.PPD_CD))

        # Agregamos el componente label fecha al sizer principal
        sizer.Add(creation_date_text, pos=(3, 0), flag=wx.LEFT, border=10)

        # Definicion del text para el valor de la fecha de creacion del project
        creation_date_value_text = wx.StaticText(panel,
                                        label=str(self.project.creation_date))

        # Desabilitamos el componente text
        creation_date_value_text.Disable()

        # Agregamos el componente text al sizer principal
        sizer.Add(creation_date_value_text, pos=(3, 1), span=(1, 4),
                  flag=wx.RIGHT | wx.EXPAND)

        # Definimos el componente StaticLine inferior
        bottom_line = wx.StaticLine(panel)

        # Agregamos la linea al sizer principal
        sizer.Add(bottom_line, pos=(5, 0), span=(1, 5),
            flag=wx.EXPAND | wx.BOTTOM, border=10)

        # Definicion del boton Cancel
        cancel_button = wx.Button(panel, label=_(C.PPD_CAN))

        # Agregamos el boton cancel al sizer principal
        sizer.Add(cancel_button, pos=(6, 3),
            flag=wx.BOTTOM | wx.RIGHT, border=5)

        # Definicion del boton ok
        ok_button = wx.Button(panel, label=_(C.PPD_OK))

        # Establecemos el foco para el boton ok
        ok_button.SetFocus()

        # Enlazamos el boton ok al metodo OnClose
        ok_button.Bind(wx.EVT_BUTTON, self.OnClose)

        # Agregamos el boton ok al sizer principal
        sizer.Add(ok_button, pos=(6, 4), flag=wx.ALIGN_RIGHT
                  | wx.LEFT, border=5)

        # Manejo de evento cuando se oprima la tecla Esc
        panel.Bind(wx.EVT_CHAR, self.OnKeyDown)

        # Configuracion del sizer principal
        sizer.AddGrowableCol(2)

        # Asociamos el sizer al panel principal
        panel.SetSizer(sizer)

    def OnClose(self, e):
        self.Close(True)

    def OnKeyDown(self, e):
        key = e.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.Close()


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1,
                             style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)

        # Definicion del presenter para la clase
        self.presenter = CheckListCtrlPresenter(self)

    def OnCheckItem(self, index, flag):
        self.presenter.OnClickCheckbox()


class UnHideProjectDialog(wx.Dialog):
    def __init__(self, parent):
        super(UnHideProjectDialog, self).__init__(parent,
                                title=_(C.UHPD_T), size=(600, 500))

        # Definicion del presenter para la clase
        self.presenter = UnHideProjectDialogPresenter(self)

        # Inicializacion de los componentes de la clase
        self.InitUI()

        self.Centre()
        self.ShowModal()

    def InitUI(self):

        # Definicion del panel contenedor principal
        panel = wx.Panel(self, -1)

        # Definicion del sizer principal de la clase
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Definicion del sizer para la cabecera del listado
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Definicion de la fuente para la descripcion
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetWeight(wx.BOLD)
        font.SetPointSize(9)

        # Definicion de un staticBitmap
        self.hide_left_bmp = wx.StaticBitmap(panel)
        self.hide_left_bmp.SetBitmap(I.hide_left_png)

        # Agregamos el icono en el sizer de la cabecera
        hbox.Add(self.hide_left_bmp, 1, wx.RIGHT, 10)

        # Definicion del componente text para desplegar descripciones
        self.description_text = wx.StaticText(panel, label=_(C.UHPD_STD))
        self.description_text.SetFont(font)

        # Insertamos el text de descripcion en el sizer de la cabecera
        hbox.Add(self.description_text, wx.RIGHT, 10)

        # Definicion del icono de ejecucion
        exec_bmp = wx.StaticBitmap(panel, bitmap=I.exec_png)

        # Agregamos el icono de ejecucion en el sizer de la cabecera
        hbox.Add(exec_bmp, 1, wx.LEFT, 220)

        # Agregamos el sizer de la cabecera al sizer principal
        sizer.Add(hbox, 1, wx.ALIGN_LEFT | wx.ALL, 10)

        # Definicion del CheckListCtrl
        self.list = CheckListCtrl(panel)

        # Establecemos las columnas con sus respectivos labels
        self.list.InsertColumn(0, _(C.UHPD_CLN), width=300)
        self.list.InsertColumn(1, _(C.UHPD_CLD), width=175)
        self.list.InsertColumn(2, _(C.UHPD_CLS), width=105)

        # Cargamos los proyectos ocultos en la lista
        self.LoadHidesProjects()

        # Agregamos la lista en el sizer principal
        sizer.Add(self.list, 8, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        # Definicion del agrupador
        sb = wx.StaticBox(panel, label=_(C.UHPD_SBL))

        # Definicion del sizer para el staticBox
        boxsizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)

        # Definicion del boxSizer para los siguientes botones
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Definicion del boton select_all
        select_all_btn = wx.Button(panel, -1, _(C.UHPD_BSAL))

        # Asociamos el evento de boton al metodo OnSelectAll
        self.Bind(wx.EVT_BUTTON, self.OnSelectAll, id=select_all_btn.GetId())

        # Agregamos el boton al hbox
        hbox.Add(select_all_btn, 1, wx.ALL, 10)

        # Definicion del boton deselect_all
        deselect_all_btn = wx.Button(panel, -1, _(C.UHPD_BDSAL))

        # Asociamos el evento de boton al metodo OnDeselectAll
        self.Bind(wx.EVT_BUTTON, self.OnDeselectAll,
                  id=deselect_all_btn.GetId())

        # Agregamos el boton al hbox
        hbox.Add(deselect_all_btn, 1, wx.ALL, 10)

        # Agregamos hbox al sizer del agrupador
        boxsizer.Add(hbox, 1,  wx.EXPAND | wx.RIGHT, 350)

        # Agregamos boxsizer al sizer principal
        sizer.Add(boxsizer, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT
                  | wx.BOTTOM, 10)

        # Definicion del sizer para los siguientes botones
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Definicion del boton apply_changes
        self.apply_change_btn = wx.Button(panel, -1, _(C.UHPD_BRL))

        # Deshabilitamos el boton
        self.apply_change_btn.Enable(False)

        # Enlazamos el evento de boton al metodo OnApply
        self.Bind(wx.EVT_BUTTON, self.OnApply,
                  id=self.apply_change_btn.GetId())

        # Agregamos el boton al sizer hbox
        hbox.Add(self.apply_change_btn)

        # Definicion del boton cancel
        cancel_btn = wx.Button(panel, -1, _(C.UHPD_BCL))

        # Enlazamos el evento de boton al metodo OnCancel
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=cancel_btn.GetId())

        # Agregamos el boton al sizer hbox
        hbox.Add(cancel_btn, 1, wx.RIGHT, 10)

        # Agregamos hbox al sizer principal
        sizer.Add(hbox, 1, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        # Establecemos el sizer al panel principal
        panel.SetSizer(sizer)

        # Manejo de evento cuando se oprima la tecla Esc
        panel.Bind(wx.EVT_CHAR, self.OnKeyDown)

        self.Centre()
        self.Show(True)

    def LoadHidesProjects(self):
        hides_projects = self.presenter.GetHideProjects()

        if not hides_projects:
            self.IsEmptyList()

        for pro in hides_projects:
            index = self.list.InsertStringItem(sys.maxint, pro.name)
            self.list.SetStringItem(index, 1, str(pro.creation_date))
            self.list.SetStringItem(index, 2, _(C.UHPD_CLCS))

    def OnSelectAll(self, event):
        self.presenter.SelectAll()

    def OnDeselectAll(self, event):
        self.presenter.DeselectAll()

    def OnApply(self, event):
        self.presenter.Restore()

    def OnCancel(self, event):
        self.presenter.ExitDialog()

    def IsEmptyList(self):
        self.description_text.SetLabel(_(C.UHPD_STDE))
        self.bmp.SetBitmap(I.warningnewproject_png)

    def OnKeyDown(self, e):
        key = e.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.Close()

import os
import wx.dataview as dv
#-------------------------- list style existing -------------------------------
styleNameList = ['Von Lucken', 'otro']
#---------------------------------------------------------------------------

#-------------------- pre-establish a file filter -----------------------------
wildcard = "Python source (*.py)|*.py|"     \
           "Compiled Python (*.pyc)|*.pyc|" \
           "SPAM files (*.spam)|*.spam|"    \
           "Egg file (*.egg)|*.egg|"        \
           "All files (*.*)|*.*"
#---------------------------------------------------------------------------


class AddFileDialog(wx.Dialog):
    def __init__(self, parent):
        super(AddFileDialog, self).__init__(parent,
                                title=_(C.AFD_T), size=(600, 500))

        self.presenter = AddFileDialogPresenter(self)
        panel = wx.Panel(self, -1, size=(595, 495))
        self.g_sizer = wx.BoxSizer(wx.VERTICAL)

        #------ header title description --------------------------------------
        ht_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #f_bmp = wx.StaticBitmap(panel,bitmap=wx.Bitmap('/icons/add_file.png'))
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        header = wx.StaticText(panel, label=_(C.AFD_STLH))
        header.SetFont(font)

        #bmp = wx.StaticBitmap(panel, bitmap=wx.Bitmap('/icons/exec.png'))

        #ht_sizer.Add(f_bmp, flag=wx.ALIGN_LEFT | wx.RIGHT, border=5)
        ht_sizer.Add(header, flag=wx.ALIGN_LEFT)
        #ht_sizer.Add(bmp, flag=wx.LEFT, border=386)
        #----------------------------------------------------

        #------ list DataViewListCtrl file ------------------------------------
        l_sizer = wx.BoxSizer()
        self.dvlc = dv.DataViewListCtrl(panel)
        self.dvlc.AppendTextColumn(_(C.AFD_TCN), width=220)
        self.dvlc.AppendTextColumn(_(C.AFD_TCD), width=100)
        l_sizer.Add(self.dvlc, 1, wx.EXPAND)
        #------------------------------------------------------------------

        #------ button open file ----------------------------------------------
        b_sizer = wx.BoxSizer()
        browse = wx.Button(panel, -1, _(C.AFD_BB))
        b_sizer.Add(browse, flag=wx.ALIGN_BOTTOM | wx.ALIGN_LEFT)
        self.Bind(wx.EVT_BUTTON, self.OnButtonBrowse, browse)
        #----------------------------------------------------

        #------------ list radio button styles ----------------------------
        s_sizer = wx.BoxSizer()
        dimension = len(styleNameList)
        self.rb = wx.RadioBox(
                panel, -1, _(C.AFD_RBT), wx.DefaultPosition,
                (600, 50), styleNameList, dimension, wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, self.rb)
        s_sizer.Add(self.rb, 1, wx.EXPAND)

        #------------------------------------------------------------------

        #------ button add and cancel add file --------------------------------
        boc_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.o_button = wx.Button(panel, label=_(C.AFD_BO))
        self.c_button = wx.Button(panel, label=_(C.AFD_BC))
        boc_sizer.Add(self.c_button)
        boc_sizer.Add(self.o_button)

        #----------------------------------------------------

        #------ add sizer global ----------------------------------------------
        self.g_sizer.Add(ht_sizer, 0.7, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM |
                         wx.LEFT | wx.TOP, border=10)
        self.g_sizer.Add(b_sizer, 0.5,
                         wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, 10)
        self.g_sizer.Add(l_sizer, 5,
                         wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.g_sizer.Add(s_sizer, 1, wx.ALL, 10)
        self.g_sizer.Add(boc_sizer, 1, wx.ALL | wx.ALIGN_RIGHT, 10)
        panel.SetSizer(self.g_sizer)

        #----------------------------------------------------

        #------ add event -----------------------------------------------------
        self.o_button.Bind(wx.EVT_BUTTON, self.OnAddFile)
        self.c_button.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.dvlc.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.OnRightClick)
        #----------------------------------------------------

        #------ start config --------------------------------------------------
        self.o_button.Enable(False)
        self.rb.EnableItem(0, False)
        self.rb.EnableItem(1, False)
        #----------------------------------------------------
        self.Show()

    def OnCancel(self, event):
        self.presenter.Close()

    def OnAddFile(self, event):
        self.presenter.AddFile()

    def EvtRadioBox(self, event):
        print 'EvtRadioBox: %d\n' % event.GetInt()

    def OnButtonBrowse(self, evt):

        self.dlg = wx.FileDialog(
            self, message=_(C.AFD_FDM),
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )

        if self.dlg.ShowModal() == wx.ID_OK:
            self.presenter.addListPath()

        self.dlg.Destroy()

    def OnRightClick(self, event):

        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnDeletedOneFile, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnDeletedAllFile, id=self.popupID2)

        # make a menu
        menu = wx.Menu()
        menu.Append(self.popupID1, _(C.AFD_FDMD))
        menu.Append(self.popupID2, _(C.AFD_FDMDA))

        self.PopupMenu(menu)
        menu.Destroy()

    def OnDeletedOneFile(self, event):
        self.presenter.deletedOneFile()

    def OnDeletedAllFile(self, event):
        self.presenter.deletedAllFile()
