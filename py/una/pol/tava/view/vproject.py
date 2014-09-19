# -*- coding: utf-8 -*-
'''
Created on 28/05/2014

@author: aferreira
'''

import os
import wx
import sys
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
import wx.lib.scrolledpanel as scrolled
from py.una.pol.tava.base.tavac import wildcard
import wx.dataview as dv
from wx import GetTranslation as _
from py.una.pol.tava.presenter.pproject import NewProjectDialogPresenter
from py.una.pol.tava.presenter.pproject import RenameProjectDialogPresenter
from py.una.pol.tava.presenter.pproject import DeleteProjectDialogPresenter
from py.una.pol.tava.presenter.pproject import UnHideProjectDialogPresenter
from py.una.pol.tava.presenter.pproject import CheckListCtrlPresenter
import py.una.pol.tava.view.vi18n as C
import py.una.pol.tava.view.vimages as I
from py.una.pol.tava.base.tavac import style_list as styleNameList
from py.una.pol.tava.base.tavac import correct, nid_error, fos_error, fva_Error
from py.una.pol.tava.base.tavac import fio_error, fuk_error


class NewProjectDialog(wx.Dialog):
    '''
    Clase Dialog que define la ventana de creación de un nuevo proyecto.
    '''

    def __init__(self, parent):
        super(NewProjectDialog, self).__init__(parent, size=(600, 630))

        #------ Definiciones iniciales ----------------------------------------
        self.presenter = NewProjectDialogPresenter(self)
        self.InitUI()

        self.Centre()
        self.ShowModal()
        #----------------------------------------------------

    def InitUI(self):
        '''
        Metodo de inicializacion de componentes de la clase
        '''

        #------ variables principales -----------------------------------------
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(6, 5)
        #----------------------------------------------------

        #------ Titulo de Proyecto Tava ---------------------------------------
        font_title = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font_title.SetWeight(wx.BOLD)
        font_title.SetPointSize(14)
        title_text = wx.StaticText(panel, label=_(C.NPD_TP))
        title_text.SetFont(font_title)

        exec_bmp = wx.StaticBitmap(panel, bitmap=I.exec_png)

        sizer.Add(title_text, pos=(0, 0), flag=wx.TOP | wx.LEFT, border=15)
        sizer.Add(exec_bmp, pos=(0, 4),
                     flag=wx.ALIGN_RIGHT | wx.RIGHT, border=15)
        #----------------------------------------------------

        #------ Texto Descriptivo que cambia ----------------------------------
        hbox_description = wx.BoxSizer(wx.HORIZONTAL)

        font_description = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font_description.SetPointSize(9)
        self.description_text = wx.StaticText(panel)
        self.description_text.SetFont(font_description)

        self.execute_bmp = wx.StaticBitmap(panel)

        hbox_description.Add(self.execute_bmp, flag=wx.LEFT, border=2)
        hbox_description.Add(self.description_text, flag=wx.LEFT, border=2)

        sizer.Add(hbox_description, pos=(1, 0), span=(1, 3), flag=wx.TOP |
                            wx.LEFT | wx.BOTTOM, border=15)
        #----------------------------------------------------

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(2, 0), span=(1, 5),
            flag=wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, border=15)

        #------ Texto para nombre de proyecto ---------------------------------
        name_project_text = wx.StaticText(panel, label=_(C.NPD_NAP))

        sizer.Add(name_project_text, pos=(3, 0),
                     flag=wx.LEFT | wx.EXPAND | wx.RIGHT, border=15)

        self.name_project_textctrl = wx.TextCtrl(panel)
        self.name_project_textctrl.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.name_project_textctrl.SetFocus()

        sizer.Add(self.name_project_textctrl, pos=(3, 1), span=(1, 4),
                     flag=wx.EXPAND | wx.RIGHT, border=15)
        #----------------------------------------------------

        #------ Agregacion de archivo  (x, y)----------------------------------
        sb = wx.StaticBox(panel, label=_(C.AFD_STLH))
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        # boton para busqueda
        self.browse = wx.Button(panel, -1, _(C.AFD_BB))
        self.Bind(wx.EVT_BUTTON, self.OnButtonBrowse, self.browse)

        #grilla de archivos
        self.scrolled_panel = scrolled.ScrolledPanel(panel, -1,
                    size=(400, 200), style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        l_sizer = wx.BoxSizer()
        self.dvlc = dv.DataViewListCtrl(self.scrolled_panel)
        self.dvlc.AppendBitmapColumn(_(C.AFD_TCC), 0, width=60)
        self.dvlc.AppendTextColumn(_(C.AFD_TCN), width=250)
        self.dvlc.AppendTextColumn(_(C.AFD_TCD), width=150)
        self.dvlc.AppendTextColumn(_(C.AFD_TCE), width=400)
        self.dvlc.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.OnRightClick)
        l_sizer.Add(self.dvlc, 1, wx.EXPAND)
        self.scrolled_panel.SetSizer(l_sizer)
        self.scrolled_panel.SetAutoLayout(1)
        self.scrolled_panel.SetupScrolling()

        #obciones de estilos
        s_sizer = wx.BoxSizer()
        dimension = len(styleNameList)
        self.rb = wx.RadioBox(
                panel, -1, _(C.AFD_RBT), wx.DefaultPosition, (580, 50),
                styleNameList, dimension, wx.RA_SPECIFY_COLS)
        self.rb.Bind(wx.EVT_RADIOBOX, self.OnSelectStyle)
        s_sizer.Add(self.rb, 1, wx.EXPAND)

        #Se agregan al boxsizer
        boxsizer.Add(self.browse, flag=wx.ALIGN_LEFT | wx.TOP | wx.BOTTOM,
                     border=10)
        boxsizer.Add(self.scrolled_panel, flag=wx.EXPAND | wx.LEFT | wx.RIGHT,
                     border=10)
        boxsizer.Add(s_sizer, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)

        #Se agregan al bugsizer
        sizer.Add(boxsizer, pos=(5, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        #----------------------------------------------------

        #------ Buttons -------------------------------------------------------
        self.help_button = wx.Button(panel, label=_(C.NPD_HELP))

        bsizer = wx.BoxSizer()
        cancel_button = wx.Button(panel, label=_(C.NPD_CAN))
        self.ok_button = wx.Button(panel, label=_(C.NPD_OK))
        bsizer.Add(cancel_button, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=15)
        bsizer.Add(self.ok_button, flag=wx.ALIGN_RIGHT)

        cancel_button.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.ok_button.Bind(wx.EVT_BUTTON, self.OnCreateProject)

        sizer.Add(self.help_button, pos=(7, 0), flag=wx.LEFT, border=15)
        sizer.Add(bsizer, pos=(7, 3), span=(3, 4),
                  flag=wx.ALIGN_RIGHT | wx.RIGHT, border=95)

        #----------------------------------------------------

        #------ configuraciones Globales --------------------------------------
        sizer.AddGrowableCol(2)
        panel.SetSizer(sizer)
        #----------------------------------------------------

        #------ valores iniciales ---------------------------------------------
        self.UpDateHiderLabel(0)
        self.presenter.disablesButtonsProject()
        #----------------------------------------------------

    def UpDateHiderLabel(self, key):

        if key == 0:
            self.description_text.SetLabel(_(C.NPD_ENP))
            self.IconAndBackgroundDefault()
            return None

        if key == 1:
            self.description_text.SetLabel(_(C.NPD_PNE))
            self.IconAndBackgroundWarning()
            return None

        self.IconAndBackgroundError()

        if key == 2:
            self.description_text.SetLabel(_(C.NPD_PNSI))
            return None

        if key == 3:
            self.description_text.SetLabel(_(C.NPD_PNPI))
            return None

        if key == 4:
            self.description_text.SetLabel(_(C.NPD_PNLI))
            return None

        if key == 5:
            self.description_text.SetLabel(_(C.NPD_PAE))
            return None

        if key == 6:
            self.description_text.SetLabel(_(C.NPD_HPAE))
            return None

        if key == 7:
            self.description_text.SetLabel(_(C.NPD_FEIP))
            self.IconAndBackgroundErrorFile()
            return None

    def IconAndBackgroundError(self):
        self.execute_bmp.SetBitmap(I.errornewproject_png)
        self.name_project_textctrl.SetBackgroundColour((237, 93, 93))

    def IconAndBackgroundWarning(self):
        self.execute_bmp.SetBitmap(I.warningnewproject_png)
        self.name_project_textctrl.SetBackgroundColour('#F9EDED')

    def IconAndBackgroundDefault(self):
        self.execute_bmp.SetBitmap(I.execute_png)
        self.name_project_textctrl.SetBackgroundColour((255, 255, 255))

    def IconAndBackgroundErrorFile(self):
        self.execute_bmp.SetBitmap(I.errornewproject_png)
        self.name_project_textctrl.SetBackgroundColour((255, 255, 255))

    def OnKeyUp(self, e):
        self.presenter.keyboardEvents(e.GetKeyCode())

    def OnCreateProject(self, e):
        self.presenter.tryToCreate()

    def OnCancel(self, e):
        self.presenter.ExitDialog()

    #--Funciones para agregar archivos ----------------------------------------
    def OnButtonBrowse(self, evt):

        self.dlg = wx.FileDialog(self, message=_(C.AFD_FDM),
            defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)

        if self.dlg.ShowModal() == wx.ID_OK:
            self.presenter.udDateGridFile(self.dlg.GetPaths())

        self.dlg.Destroy()

    def getLabelError(self, error):
        if error == correct:
            return _(C.AFD_EN)
        elif error == nid_error:
            return _(C.AFD_EDNG)
        elif error == fos_error:
            return _(C.AFD_ERS)
        elif error == fva_Error:
            return _(C.AFD_EFF)
        elif error == fio_error:
            return _(C.AFD_EOF)
        elif error == fuk_error:
            return _(C.AFD_EUE)

    def OnRightClick(self, event):
        if self.presenter.isAnyRowSelected():
            if not hasattr(self, "popupID1"):
                self.popupID1 = wx.NewId()
                self.popupID2 = wx.NewId()

                self.Bind(wx.EVT_MENU, self.OnDeletedOneFile, id=self.popupID1)
                self.Bind(wx.EVT_MENU, self.OnDeletedAllFile, id=self.popupID2)

            menu = wx.Menu()
            menu.Append(self.popupID1, _(C.AFD_FDMD))
            menu.Append(self.popupID2, _(C.AFD_FDMDA))

            self.PopupMenu(menu)
            menu.Destroy()

    def OnDeletedOneFile(self, event):
        self.presenter.deletedOneFile()

    def OnDeletedAllFile(self, event):
        self.presenter.deletedAllFile()

    def OnSelectStyle(self, event):
        self.presenter.checkStyle()

    #----------------------------------------------------


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

        # variables principales
        panel = wx.Panel(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)

        #----- BoxSizer cabecera ----------------------------------------------
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        # Definicion de un staticBitmap
        self.hide_left_bmp = wx.StaticBitmap(panel, bitmap=I.hide_left_png)

        # descripcion de la cabecera
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetWeight(wx.BOLD)
        font.SetPointSize(9)
        self.description_text = wx.StaticText(panel, label=_(C.UHPD_STD))
        self.description_text.SetFont(font)

        # Definicion del icono de ejecucion
        exec_bmp = wx.StaticBitmap(panel, bitmap=I.exec_png)

        # Agregamos al BoxSizer cabecera
        hbox1.Add(self.hide_left_bmp, 1, wx.RIGHT, 10)
        hbox1.Add(self.description_text, wx.RIGHT, 10)
        hbox1.Add(exec_bmp, 1, wx.LEFT, 220)
        #-------------------------------------------------------

        #----- Componete CheckListCtrl  ---------------------------------------

        self.list = CheckListCtrl(panel)

        # Establecemos las columnas con sus respectivos labels
        self.list.InsertColumn(0, _(C.UHPD_CLN), width=300)
        self.list.InsertColumn(1, _(C.UHPD_CLD), width=175)
        self.list.InsertColumn(2, _(C.UHPD_CLS), width=105)

        # Cargamos los proyectos ocultos en la lista
        self.LoadHidesProjects()
        #-------------------------------------------------------

        #----- StaticBox agrupador --------------------------------------------
        sb = wx.StaticBox(panel, label=_(C.UHPD_SBL))

        # Definicion del sizer para el staticBox
        boxsizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)

        #----- BoxSizer para select_all, deselect_all -------------------------
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        select_all_btn = wx.Button(panel, -1, _(C.UHPD_BSAL))
        self.Bind(wx.EVT_BUTTON, self.OnSelectAll, id=select_all_btn.GetId())

        deselect_all_btn = wx.Button(panel, -1, _(C.UHPD_BDSAL))
        self.Bind(wx.EVT_BUTTON, self.OnDeselectAll,
                  id=deselect_all_btn.GetId())

        # Agregamos los botones al hbox2
        hbox2.Add(select_all_btn, 1, wx.ALL, 10)
        hbox2.Add(deselect_all_btn, 1, wx.ALL, 10)
        #-------------------------------------------------------

        # Agregamos hbox al sizer del agrupador
        boxsizer.Add(hbox2, 1,  wx.EXPAND | wx.RIGHT, 250)
        #-------------------------------------------------------

        #----- BoxSizer para cancel, apply ------------------------------------
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        # Definicion del boton cancel
        cancel_btn = wx.Button(panel, -1, _(C.UHPD_BCL))
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=cancel_btn.GetId())

        # Definicion del boton apply_changes
        self.apply_change_btn = wx.Button(panel, -1, _(C.UHPD_BRL))
        self.apply_change_btn.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.OnApply,
                  id=self.apply_change_btn.GetId())

        # Agregamos los botones al sizer hbox3
        hbox3.Add(cancel_btn, 1, wx.RIGHT, 10)
        hbox3.Add(self.apply_change_btn)
        #-------------------------------------------------------

        #----- Agregamos los box sizer al BoxSizer principal ------------------
        sizer.Add(hbox1, 1, wx.ALIGN_LEFT | wx.ALL, 10)
        sizer.Add(self.list, 8, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        sizer.Add(boxsizer, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT
                  | wx.BOTTOM, 10)
        sizer.Add(hbox3, 1, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT
                  | wx.BOTTOM, 10)
        #-------------------------------------------------------

        # Establecemos el sizer al panel principal
        panel.SetSizer(sizer)

        # Manejo de evento cuando se oprima la tecla Esc
        panel.Bind(wx.EVT_CHAR, self.OnKeyDown)

        self.Centre()
        self.Show(True)

    def LoadHidesProjects(self):
        self.presenter.GetHideProjects()

    def AddItemToList(self, name, date):
        index = self.list.InsertStringItem(sys.maxint, name)
        self.list.SetStringItem(index, 1, date)
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
        self.hide_left_bmp.SetBitmap(I.warningnewproject_png)

    def OnKeyDown(self, e):
        key = e.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.Close()
