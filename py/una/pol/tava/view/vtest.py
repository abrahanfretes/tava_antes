'''
Created on 06/09/2014

@author: arsenioferreira
'''
import wx
import wx.wizard as wizmod
import wx.dataview as dv
from wx.lib.itemspicker import ItemsPicker, IP_SORT_CHOICES, IP_SORT_SELECTED,\
                               IP_REMOVE_FROM_CHOICES, EVT_IP_SELECTION_CHANGED
from py.una.pol.tava.presenter.ptest import GraphicWizardPresenter

padding = 5

graphList = ["Parallel Coordinates",
              "Som"]


class GraphicWizard(wizmod.Wizard):
    '''Add pages to this wizard object to make it useful.'''
    def __init__(self, project):

        self.presenter = GraphicWizardPresenter(self)

        self.project = project
        wizmod.Wizard.__init__(self, None, -1, title="New Test")
        self.SetPageSize((500, 380))
        self.pages = []

        # Create a first page
        self.page1 = WizardPage(self)
        panel1 = PanelFirstPage(self.page1)
        self.page1.add_stuff(panel1)
        self.page1.panel1 = panel1
        self.add_page(self.page1)

        # Add second page
        self.page2 = WizardPage(self)
        ldvPanel = TestPanel(self.page2)
        self.page2.add_stuff(ldvPanel)
        self.page2.ldvPanel = ldvPanel
        self.add_page(self.page2)

        self.Bind(wizmod.EVT_WIZARD_PAGE_CHANGED, self.on_page_changed)
        self.Bind(wizmod.EVT_WIZARD_FINISHED, self.on_finished)

        self.FitToPage(self.page1)

#         Show the main window
        self.run()

        # Cleanup
        self.Destroy()

    def add_page(self, page):
        '''Add a wizard page to the list.'''
        if self.pages:
            previous_page = self.pages[-1]
            page.SetPrev(previous_page)
            previous_page.SetNext(page)
        self.pages.append(page)

    def on_page_changed(self, evt):
        forward_btn = self.FindWindowById(wx.ID_FORWARD)
        page = evt.GetPage()
        if evt.GetDirection():
            forward_btn.Disable()
            if page is self.pages[1]:
                if (len(self.page1.ip.GetSelections()) !=
                    len(self.page2.ldvPanel.data)):

                    files = self.presenter.GetListResultIterations(
                                                                self.project,
                                                self.page1.ip.GetSelections())

                    self.page2.ldvPanel.dvc.ClearColumns()

                    self.page2.ldvPanel.configDVC(files)
                if self.page2.ldvPanel.isSomeSelection():
                    forward_btn.Enable(True)

#             if page is self.pages[2]:
#                 forward_btn.Enable(True)
        else:
            forward_btn.Enable(True)

    def run(self):
        self.RunWizard(self.pages[0])

    def on_finished(self, evt):
        '''Finish button has been pressed.  Clean up and exit.'''

        # Nombre del test
        name_test = self.page1.panel1.name_value_text.GetValue()
        # Archivos Resultados e iteraciones seleccionadas
        data = self.page2.ldvPanel.data

        self.presenter.CreateTest(name_test, data, self.project)


class WizardPage(wizmod.PyWizardPage):
    ''' An extended panel obj with a few methods to keep track of its siblings.
        This should be modified and added to the wizard.  Season to taste.'''
    def __init__(self, parent):
        wizmod.PyWizardPage.__init__(self, parent)
        self.next = self.prev = None
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, -1, "Tava Test")
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.AddWindow(title, 0, wx.ALIGN_LEFT | wx.ALL, padding)
        self.sizer.AddWindow(wx.StaticLine(self, -1), 0, wx.EXPAND |
                             wx.ALL, padding)
        self.SetSizer(self.sizer)

    def add_stuff(self, stuff):
        '''Add aditional widgets to the bottom of the page'''
        self.sizer.Add(stuff, 1, wx.EXPAND | wx.ALL, padding)

    def SetNext(self, next_):
        '''Set the next page'''
        self.next = next_

    def SetPrev(self, prev):
        '''Set the previous page'''
        self.prev = prev

    def GetNext(self):
        '''Return the next page'''
        return self.next

    def GetPrev(self):
        '''Return the previous page'''
        return self.prev


class PanelFirstPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        sizer = wx.GridBagSizer(5, 5)

        text2 = wx.StaticText(self, label="Test Name")
        sizer.Add(text2, pos=(1, 0), flag=wx.LEFT, border=10)

        self.name_value_text = wx.TextCtrl(self)
        self.name_value_text.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.name_value_text.SetFocus()
        sizer.Add(self.name_value_text, pos=(1, 1), span=(1, 4), flag=wx.TOP |
                  wx.EXPAND)

        # Definicion del text para el label de nombre de proyecto
        project_text = wx.StaticText(self, label="Project")
        sizer.Add(project_text, pos=(2, 0), flag=wx.LEFT, border=10)

        # Definicion del text para el valor del nombre de proyecto
        project_value_text = wx.StaticText(self,
                                        label=parent.GetParent().project.name)

        # Desabilitamos el componente text
        project_value_text.Disable()

        # Agregamos el componente text al sizer principal
        sizer.Add(project_value_text, pos=(2, 1), span=(1, 4), flag=wx.RIGHT |
                  wx.EXPAND)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        ip = ItemsPicker(self, -1, self.GetListItems(), 'Files:',
                              'Selected Files:', ipStyle=IP_SORT_CHOICES |
                              IP_SORT_SELECTED | IP_REMOVE_FROM_CHOICES)
        ip._source.SetMinSize((-1, 150))
        ip.Bind(EVT_IP_SELECTION_CHANGED, self.OnSelectionChange)
        vbox2.Add(ip, 1, wx.EXPAND | wx.ALL, 3)
        parent.ip = ip

        sizer.Add(vbox2, pos=(6, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.ALL)

        sizer.AddGrowableCol(2)

        self.SetSizer(sizer)

    def GetListItems(self):
        return self.GetParent().GetParent().presenter.GetListItems()

    def OnSelectionChange(self, e):
        grand_father = self.GetParent().GetParent()
        forward_btn = grand_father.FindWindowById(wx.ID_FORWARD)
        if e.GetItems():
            forward_btn.Enable(True)
        else:
            forward_btn.Disable()

    def OnKeyUp(self, e):
        self.GetParent().GetParent().presenter.keyboardEvents(e.GetKeyCode())


class Iteration(object):
    def __init__(self, id_, val):
        self.id = id_
        self.label = str(val[0].identifier)
        self.result_file = val[1].name
        self.check = False
        self.iteration = val[0]

    def __repr__(self):
        return 'Iteration %s-%s' % (self.label, self.result_file)


class ResultFile(object):
    def __init__(self, result):
        self.name = result.name
        self.result = result
        self.iterations = []

    def __repr__(self):
        return 'ResultFile: ' + self.name


class MyTreeListModel(dv.PyDataViewModel):
    def __init__(self, data):
        dv.PyDataViewModel.__init__(self)
        self.data = data

        self.objmapper.UseWeakRefs(True)

    def GetColumnCount(self):
        return 3

    def GetColumnType(self, col):
        mapper = {0: 'string',
                   1: 'string',
                   2: 'bool'
                   }
        return mapper[col]

    def GetChildren(self, parent, children):
        if not parent:
            for genre in self.data:
                children.append(self.ObjectToItem(genre))
            return len(self.data)

        node = self.ItemToObject(parent)
        if isinstance(node, ResultFile):
            for itr in node.iterations:
                children.append(self.ObjectToItem(itr))
            return len(node.iterations)
        return 0

    def IsContainer(self, item):
        if not item:
            return True

        node = self.ItemToObject(item)
        if isinstance(node, ResultFile):
            return True

        return False

    def GetParent(self, item):

        if not item:
            return dv.NullDataViewItem

        node = self.ItemToObject(item)
        if isinstance(node, ResultFile):
            return dv.NullDataViewItem
        elif isinstance(node, Iteration):
            for rf in self.data:
                if rf.name == node.result_file:
                    return self.ObjectToItem(rf)

    def GetValue(self, item, col):
        node = self.ItemToObject(item)

        if isinstance(node, ResultFile):
            mapper = {0: node.name,
                       1: "",
                       2: False      # some way to indicate a null value...
                       }
            return mapper[col]

        elif isinstance(node, Iteration):
            mapper = {0: "",
                       1: node.label,
                       2: node.check}
            return mapper[col]

        else:
            raise RuntimeError("unknown node type")

    def GetAttr(self, item, col, attr):
        node = self.ItemToObject(item)
        if isinstance(node, ResultFile):
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False

    def SetValue(self, value, item, col):
#         print("SetValue: %s\n" % value)
        node = self.ItemToObject(item)
        if isinstance(node, Iteration):
            if col == 2:
                node.check = value

    def getParentItem(self):
        itemParent = []
        for node in self.data:
            if isinstance(node, ResultFile):
                itemParent.append(self.ObjectToItem(node))
        return itemParent


class TestPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        # Create a dataview control
        self.dvc = dv.DataViewCtrl(self, style=wx.BORDER_THEME
                    | dv.DV_ROW_LINES | dv.DV_VERT_RULES | dv.DV_MULTIPLE)
        data = dict()
        self.configDVC(data)

        self.dvc.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED,
                      self.OnSelectionChange)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.dvc, 1, wx.EXPAND)

    def OnSelectionChange(self, e):
        page_wizard = self.GetParent()
        forward_btn = page_wizard.GetParent().FindWindowById(wx.ID_FORWARD)
        if forward_btn:
            if self.isSomeSelection():
                forward_btn.Enable(True)
            else:
                forward_btn.Disable()

    def isSomeSelection(self):
        for result in self.data:
            for itr in result.iterations:
                if itr.check:
                    return True
        return False

    def configDVC(self, files):
        filedatas = files.items()
        filedatas.sort()

        # our data structure will be a collection of Genres, each of which is a
        # collection of Songs
        data = dict()
        for key, val in filedatas:
            itr = Iteration(key, val)
            result_file = data.get(itr.result_file)
            if result_file is None:
                result_file = ResultFile(val[1])
                data[itr.result_file] = result_file
            result_file.iterations.append(itr)
        data = data.values()

        # Create an instance of our model...
        self.model = MyTreeListModel(data)

        self.data = data
        # Tel the DVC to use the model
        self.dvc.AssociateModel(self.model)

        # Define the columns that we want in the view.  Notice the
        # parameter which tells the view which col in the data model to pull
        # values from for each view column.
        self.tr = tr = dv.DataViewTextRenderer()
        tr.EnableEllipsize()
        tr.SetAlignment(0)
        c0 = dv.DataViewColumn("File",   # title
                               tr,        # renderer
                               0,         # data model column
                               width=200)
        self.dvc.AppendColumn(c0)

        c1 = self.dvc.AppendTextColumn("Iteration",   1, width=200)
        c1.Alignment = wx.ALIGN_CENTRE

        self.dvc.AppendToggleColumn("Select",   2, width=20,
                                    mode=dv.DATAVIEW_CELL_ACTIVATABLE)

        # Set some additional attributes for all the columns
        for c in self.dvc.Columns:
            c.Sortable = True
            c.Reorderable = True

        for node in self.model.getParentItem():
            self.dvc.Expand(node)
